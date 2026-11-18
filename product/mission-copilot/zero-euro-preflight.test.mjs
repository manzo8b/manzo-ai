import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import {
  BUDGET_BASELINE, estimateNeurons, projectDailyBudget,
  inspectOfflineConfiguration
} from "./zero-euro-preflight.mjs";

const root = dirname(fileURLToPath(import.meta.url));
const wrangler = readFileSync(resolve(root, "wrangler.toml"), "utf8");
const worker = readFileSync(resolve(root, "worker.mjs"), "utf8");

test("P3 budget model agrees with Gemma 4 free quota and absolute local daily limit", () => {
  const model = projectDailyBudget();
  assert.equal(model.model, "@cf/google/gemma-4-26b-a4b-it");
  assert.equal(model.dailyReservationCap, 20);
  assert.equal(model.modelOutputTokenCap, 650);
  assert.equal(model.providerFreeDailyNeurons, 10_000);
  assert.ok(model.estimatedNeuronsAtCap > 0);
  assert.ok(model.withPlanningMargin < model.conservativeInternalThreshold);
  assert.equal(model.actualNeuronsVerified, false);
  assert.equal(model.billingPlanVerified, false);
});
test("P3 estimator is deterministic and rejects malformed forecast values", () => {
  assert.equal(estimateNeurons(1000, 500, 1),
    Math.ceil((1000 * 9091 + 500 * 27273) / 1_000_000));
  assert.equal(estimateNeurons(0, 0, 0), 0);
  for (const invalid of [-1, 1.2, Infinity, NaN, "100", 1_000_001])
    assert.throws(() => estimateNeurons(invalid, 650, 20), RangeError);
});
test("P3 configuration passes security audit BUT remains blocked until owner verification", () => {
  const report = inspectOfflineConfiguration(wrangler, worker);
  assert.equal(report.status, "BLOCKED_NOT_CONNECTED");
  assert.equal(report.configSafe, true, JSON.stringify(report.checks));
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.safeToEnablePublicInference, false);
  assert.equal(report.externalAccountChecked, false);
  assert.equal(report.actualNeuronsChecked, false);
  assert.equal(report.realModelCalled, false);
  assert.ok(report.manualChecksRequired.length >= 7);
});
test("P3 missing privacy gate or any activation OFF flag breaks security preflight", () => {
  const changed = [
    wrangler.replace('COPILOT_ENABLED = "false"', 'COPILOT_ENABLED = "true"'),
    wrangler.replace('FREE_PLAN_CONFIRMED = "false"', 'FREE_PLAN_CONFIRMED = "true"'),
    wrangler.replace('MODEL_FREE_CONFIRMED = "false"', 'MODEL_FREE_CONFIRMED = "true"'),
    wrangler.replace('DATA_PROTECTION_CONFIRMED = "false"', 'DATA_PROTECTION_CONFIRMED = "true"')
  ];
  for (const bad of changed) {
    const audit = inspectOfflineConfiguration(bad, worker);
    assert.equal(audit.configSafe, false);
    assert.equal(audit.checks.flagsDefaultOff, false);
  }
  const withoutGate = worker.replace(
    'env?.DATA_PROTECTION_CONFIRMED !== "true"', "false"
  );
  assert.equal(inspectOfflineConfiguration(wrangler, withoutGate).configSafe, false);
});
test("P4 first beta must be synthetic-only in both Worker source and Wrangler", () => {
  const normal = inspectOfflineConfiguration(wrangler, worker);
  assert.equal(normal.checks.syntheticBetaOnly, true);
  assert.equal(normal.safeToEnablePublicInference, false);
  for (const source of [
    wrangler.replace('BETA_SYNTHETIC_ONLY = "true"', 'BETA_SYNTHETIC_ONLY = "false"'),
    wrangler.replace('BETA_SYNTHETIC_ONLY = "true"', '')
  ]) {
    const result = inspectOfflineConfiguration(source, worker);
    assert.equal(result.configSafe, false);
    assert.equal(result.checks.syntheticBetaOnly, false);
  }
  assert.equal(inspectOfflineConfiguration(
    wrangler, worker.replace('scenarioInput(JSON.parse(raw))', 'JSON.parse(raw)')
  ).configSafe, false);
});
test("P4 private beta must automatically expire pseudonymous quota state", () => {
  const normal=inspectOfflineConfiguration(wrangler,worker);
  assert.equal(normal.checks.quotaExpiryAlarm,true);
  const noAlarm=worker.replace("await tx.setAlarm(", "await expired.setAlarm(");
  assert.equal(inspectOfflineConfiguration(wrangler,noAlarm).checks.quotaExpiryAlarm,false);
  const noDeletion=worker.replace("await this.ctx.storage.deleteAll()", "return");
  assert.equal(inspectOfflineConfiguration(wrangler,noDeletion).checks.quotaExpiryAlarm,false);
});
test("P3 fake public route, disabled quotas or logging on must fail preflight", () => {
  const broken = [
    wrangler + '\nroute = "example.com/*"',
    wrangler.replace('workers_dev = false', 'workers_dev = true'),
    wrangler.replace('enabled = false', 'enabled = true'),
    wrangler.replace('invocation_logs = false', 'invocation_logs = true'),
    wrangler.replace('new_sqlite_classes = ["CopilotQuota"]', 'new_sqlite_classes = []'),
    wrangler + '\nCLOUDFLARE_API_TOKEN = "never-do-this"'
  ];
  for (const bad of broken) {
    const report = inspectOfflineConfiguration(bad, worker);
    assert.equal(report.configSafe, false, JSON.stringify(report.checks));
  }
});
test("P3 model cost estimates cannot substitute for actual Cloudflare billing or usage", () => {
  const conservative = projectDailyBudget({
    ...BUDGET_BASELINE, assumedInputTokensPerCall: 1_000_000
  });
  assert.equal(conservative.projectedWithinPlanningThreshold, false);
  const audit = inspectOfflineConfiguration(wrangler, worker, {
    ...BUDGET_BASELINE, inputNeuronsPerMillion: 1_000_000
  });
  assert.equal(audit.configSafe, false);
  assert.equal(audit.safeToEnablePublicInference, false);
});
test("P3 no inference API or paid provider is contacted by offline preflight", () => {
  const source = readFileSync(resolve(root, "zero-euro-preflight.mjs"), "utf8");
  assert.doesNotMatch(source, /\bfetch\s*\(/);
  assert.doesNotMatch(source, /api\.cloudflare\.com/);
  assert.doesNotMatch(source, /CLOUDFLARE_API_TOKEN\s*=/);
  assert.doesNotMatch(wrangler, /^\s*(?:route|routes)\s*=/m);
});
