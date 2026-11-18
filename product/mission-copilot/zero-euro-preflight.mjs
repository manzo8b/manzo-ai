/**
 * MANZO AI · P3 zero-euro / privacy preflight (offline only).
 * Do not query Cloudflare or generate account-specific claims.
 *
 * Static rates sourced from Cloudflare Workers AI pricing on 2026-11-18:
 * @cf/google/gemma-4-26b-a4b-it: 9,091 Neurons/1M input tokens
 * and 27,273 Neurons/1M output tokens. Subject to change.
 *
 * The estimate is NOT a billing meter: only the Cloudflare account
 * dashboard can confirm actual Neurons, plan, quotas and payments.
 */
import fs from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, resolve } from "node:path";
import { MODEL, QUOTA_POLICY } from "./worker.mjs";

export const BUDGET_BASELINE = Object.freeze({
  model: "@cf/google/gemma-4-26b-a4b-it",
  verifiedOn: "2026-11-18",
  freeNeuronsPerDay: 10_000,
  inputNeuronsPerMillion: 9_091,
  outputNeuronsPerMillion: 27_273,
  assumedInputTokensPerCall: 6_000,
  cappedOutputTokensPerCall: 650,
  planningMargin: 4,
  internalDailyRequests: 20,
  planningCeilingNeurons: 8_000
});

function whole(value, minimum, maximum) {
  if (!Number.isInteger(value) || value < minimum || value > maximum) {
    throw new RangeError("Invalid planning bound");
  }
  return value;
}
export function estimateNeurons(inputTokens, outputTokens, requests, options = BUDGET_BASELINE) {
  whole(inputTokens, 0, 1_000_000);
  whole(outputTokens, 0, 1_000_000);
  whole(requests, 0, 1_000_000);
  return Math.ceil(
    requests * (
      inputTokens * options.inputNeuronsPerMillion / 1_000_000 +
      outputTokens * options.outputNeuronsPerMillion / 1_000_000
    )
  );
}
export function projectDailyBudget(policy = BUDGET_BASELINE) {
  const estimate = estimateNeurons(
    policy.assumedInputTokensPerCall,
    policy.cappedOutputTokensPerCall,
    policy.internalDailyRequests,
    policy
  );
  return {
    model: policy.model,
    sourceDate: policy.verifiedOn,
    modelOutputTokenCap: policy.cappedOutputTokensPerCall,
    assumedInputTokenCount: policy.assumedInputTokensPerCall,
    dailyReservationCap: policy.internalDailyRequests,
    estimatedNeuronsAtCap: estimate,
    marginFactor: policy.planningMargin,
    withPlanningMargin: estimate * policy.planningMargin,
    providerFreeDailyNeurons: policy.freeNeuronsPerDay,
    conservativeInternalThreshold: policy.planningCeilingNeurons,
    projectedWithinPlanningThreshold:
      estimate * policy.planningMargin < policy.planningCeilingNeurons,
    // A cost estimate can never prove the real account balance or usage.
    actualNeuronsVerified: false,
    billingPlanVerified: false
  };
}
const assignment = (text, name) => {
  const matches = [...text.matchAll(new RegExp(
    "^\\s*" + name + "\\s*=\\s*\"([^\"]*)\"\\s*$", "gm"
  ))];
  return matches.length === 1 ? matches[0][1] : null;
};
function protectedConfig(wrangler, worker) {
  const requiredFalse = [
    "COPILOT_ENABLED", "FREE_PLAN_CONFIRMED",
    "MODEL_FREE_CONFIRMED", "DATA_PROTECTION_CONFIRMED"
  ];
  const checks = {
    flagsDefaultOff: requiredFalse.every(k => assignment(wrangler, k) === "false"),
    syntheticBetaOnly: assignment(wrangler, "BETA_SYNTHETIC_ONLY") === "true" &&
      worker.includes('env?.BETA_SYNTHETIC_ONLY !== "true"') &&
      worker.includes("scenarioInput(JSON.parse(raw))") &&
      worker.includes('"SYNTHETIC_CASE_REQUIRED"'),
    workersDevOff: assignment(wrangler, "workers_dev") === null &&
      /^\s*workers_dev\s*=\s*false\s*$/m.test(wrangler),
    noPublicRoute: !/^\s*(?:route|routes)\s*=/m.test(wrangler),
    noBillingSecrets: !/^\s*(?:ACCESS_AUD|QUOTA_HASH_SALT|PREVIEW_ACCESS_TOKEN|CLOUDFLARE_API_TOKEN|SUPABASE_PUBLISHABLE_KEY|SUPABASE_ALLOWED_TESTER_IDS)\s*=/m.test(wrangler),
    loggingDisabled: /^\s*\[observability\]\s*$/m.test(wrangler) &&
      /^\s*enabled\s*=\s*false\s*$/m.test(wrangler) &&
      /^\s*\[observability\.logs\]\s*$/m.test(wrangler) &&
      /^\s*invocation_logs\s*=\s*false\s*$/m.test(wrangler),
    sqliteQuotaBinding: /name\s*=\s*"GLOBAL_QUOTA"/.test(wrangler) &&
      /class_name\s*=\s*"CopilotQuota"/.test(wrangler) &&
      /new_sqlite_classes\s*=\s*\["CopilotQuota"\]/.test(wrangler),
    separatePrivacyGate: /DATA_PROTECTION_CONFIRMED\s*!==\s*"true"/.test(worker),
    gemmaThinkingDisabled: /chat_template_kwargs:\s*\{\s*enable_thinking:\s*false\s*\}/.test(worker),
    supabaseAuthDefaultOff: assignment(wrangler, "AUTH_PROVIDER") === "access" &&
      assignment(wrangler, "SUPABASE_AUTH_CONFIRMED") === "false" &&
      worker.includes('env?.AUTH_PROVIDER || "access"') &&
      worker.includes('env?.SUPABASE_AUTH_CONFIRMED !== "true"') &&
      worker.includes("authenticatedSupabasePrincipal(request, env)"),
    quotaExpiryAlarm: worker.includes("await tx.setAlarm(") &&
      worker.includes("async alarm()") &&
      worker.includes("await this.ctx.storage.deleteAll()"),
    usageReservationBeforeAI: worker.indexOf("reserveGlobalQuota(env, principal)") >= 0 &&
      worker.indexOf("reserveGlobalQuota(env, principal)") <
        worker.indexOf("await env.AI.run(MODEL,"),
    noCustomContentLogging: !/\bconsole\.(?:log|warn|info|error|debug)\s*\(/.test(worker),
    noPublicAIProxy: !/[\x22\x27]access-control-allow-origin[\x22\x27]\s*:/i.test(worker) &&
      !/headers\.set\s*\(\s*[\x22\x27]access-control-allow-origin/i.test(worker)
  };
  return checks;
}
export function inspectOfflineConfiguration(wrangler, worker, policy = BUDGET_BASELINE) {
  if (typeof wrangler !== "string" || typeof worker !== "string") {
    throw new TypeError("Preflight needs explicit source strings");
  }
  const checks = protectedConfig(wrangler, worker);
  const budget = projectDailyBudget(policy);
  checks.modelAndDailyCapMatch =
    MODEL === policy.model &&
    QUOTA_POLICY.globalDaily === policy.internalDailyRequests &&
    worker.includes("max_completion_tokens: " + policy.cappedOutputTokensPerCall);
  checks.projectedWithinThreshold = budget.projectedWithinPlanningThreshold;
  const configSafe = Object.values(checks).every(Boolean);
  return {
    status: "BLOCKED_NOT_CONNECTED",
    zeroEuroBudget: "0 EUR (no Cloudflare inference or deployment performed)",
    configSafe,
    checks,
    budget,
    manualChecksRequired: [
      "Verify Cloudflare account is Workers Free and no paid billing is enabled",
      "Verify Zero Trust Free onboarding and payment-method requirement with owner",
      "Verify Access sign-in with a real restricted tester account",
      "Reconfirm chosen model remains Free in the day of activation",
      "Inspect Cloudflare Workers AI dashboard for actual Neurons usage",
      "Review processor terms, transfers, privacy notices and school use with responsible parties",
      "Verify account-level logs, gateway logs, and observability are configured for no prompt/response retention",
      "Verify accessibility and consent notice before transmitting any real brief"
    ],
    externalAccountChecked: false,
    actualNeuronsChecked: false,
    realModelCalled: false,
    safeToEnablePublicInference: false
  };
}

const invoked = process.argv[1] &&
  import.meta.url === pathToFileURL(resolve(process.argv[1])).href;
if (invoked) {
  const folder = dirname(fileURLToPath(import.meta.url));
  const wrangler = fs.readFileSync(resolve(folder, "wrangler.toml"), "utf8");
  const worker = fs.readFileSync(resolve(folder, "worker.mjs"), "utf8");
  const result = inspectOfflineConfiguration(wrangler, worker);
  console.log(JSON.stringify(result, null, 2));
  // Safe source-only is a success; activation stays blocked.
  if (!result.configSafe) process.exitCode = 1;
}
