/**
 * Mission Studio P1 · optional, offline, non-generative integration preview.
 * Loaded ONLY when ?copilot=preview. No fetch, keys, tokens or storage.
 * Public Mission Studio remains the ordinary local teaching brief by default.
 */
import {
  toCopilotRequest, makeLocalSimulation, validateCopilotProposal
} from "./mission-adapter.mjs";

export function initializeCopilotPreview({ getBrief, document, window }) {
  if (typeof getBrief !== "function") throw new Error("Missing Mission Studio state");
  const el = id => document.getElementById(id);
  const area = el("copilot-preview");
  if (!area) return false;
  const simulate = el("copilot-simulate");
  const apply = el("copilot-apply");
  const status = el("copilot-status");
  const results = el("copilot-results");
  const goal = el("copilot-goal");
  const activities = el("copilot-activities");
  const evidence = el("copilot-criteria");
  const access = el("copilot-access");
  let pending = null;
  let fingerprint = null;
  if (![simulate,apply,status,results,goal,activities,evidence,access].every(Boolean))
    throw new Error("Incomplete Mission Copilot preview UI");

  const current = () => toCopilotRequest(getBrief());
  const signature = input => JSON.stringify(input);
  const clear = () => {
    pending = null; fingerprint = null;
    results.hidden = true; apply.disabled = true;
    status.textContent = "Le proposte precedenti sono state invalidate: aggiorna la simulazione dopo ogni modifica.";
  };
  area.hidden = false;
  // Module is purely editorial; show that the next stage requires safeguards.
  access.textContent = "Anteprima locale: nessuna chiamata IA e nessun dato inviato. Il servizio generativo è disattivato.";
  simulate.addEventListener("click", () => {
    try {
      const input = current(); // Validated using the same fields as private Worker
      const draft = validateCopilotProposal(
        makeLocalSimulation(getBrief()), "simulazione_locale"
      );
      pending = draft;
      fingerprint = signature(input);
      goal.textContent = draft.obiettivo;
      evidence.textContent = draft.criteriDiVerifica;
      activities.replaceChildren();
      draft.attivita.forEach(line => {
        const li = document.createElement("li");
        li.textContent = line; activities.append(li);
      });
      results.hidden = false;
      apply.disabled = false;
      status.textContent =
        "Simulazione editoriale pronta. Non è una risposta generata da un modello IA.";
    } catch (error) {
      clear();
      status.textContent = error?.message || "Non è possibile preparare la simulazione.";
    }
  });
  apply.addEventListener("click", () => {
    if (!pending || !fingerprint) return;
    let valid;
    try { valid = signature(current()) === fingerprint; }
    catch { valid = false; }
    if (!valid) { clear(); return; }
    if (!window.confirm(
      "Copiare soltanto l'obiettivo simulato nel tuo brief? Non approva il progetto, non modifica fonti né materiali."
    )) return;
    const objective = el("objective");
    objective.value = pending.obiettivo;
    // Existing Mission Studio controller handles re-render, unsaved state,
    // keyboard and export. No duplicate approval state is created.
    objective.dispatchEvent(new window.Event("input", { bubbles: true }));
    objective.focus();
    status.textContent =
      "Obiettivo copiato nel brief. La bozza resta non approvata: verifica e modifica prima dell'uso.";
  });
  ["topic","audience","objective"].forEach(id => {
    const input = el(id);
    for (const event of ["input","change"]) input.addEventListener(event, clear);
  });
  document.querySelectorAll("[data-kind],[data-minutes],[data-topic]").forEach(button => {
    button.addEventListener("click", clear);
  });
  for (const id of ["reset","restore"]) {
    el(id).addEventListener(id === "reset" ? "click" : "change", clear);
  }
  results.hidden = true;
  apply.disabled = true;
  status.textContent = "Seleziona «Prova la simulazione» dopo aver definito il brief.";
  return true;
}
