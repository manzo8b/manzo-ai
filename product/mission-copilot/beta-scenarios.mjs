/**
 * P4 Mission Copilot beta: SERVER-OWNED, synthetic-only scenario allowlist.
 * The browser supplies ONLY a scenarioId. No arbitrary lesson text, names,
 * student data, teacher contacts, URLs or profile fields can reach Workers AI.
 * This source is intended for limited first-inference evaluation after a
 * separate owner-approved Cloudflare Free + privacy check; NOT live yet.
 */
export const BETA_SCENARIOS = Object.freeze({
  water_cycle: Object.freeze({
    tema: "Le fasi del ciclo dell'acqua",
    destinatari: "secondaria_primo_grado",
    durataMinuti: 30,
    tipoRisorsa: "immagini",
    obiettivo: "Distinguere evaporazione, condensazione e precipitazione con una rappresentazione semplice"
  }),
  historical_source: Object.freeze({
    tema: "Fonti storiche primarie e interpretazioni",
    destinatari: "secondaria_secondo_grado",
    durataMinuti: 45,
    tipoRisorsa: "verifica",
    obiettivo: "Confrontare due testimonianze immaginarie e distinguere fatti, ipotesi e opinioni"
  }),
  sound_and_transcript: Object.freeze({
    tema: "Ascolto attivo e descrizione di un paesaggio sonoro inventato",
    destinatari: "primaria",
    durataMinuti: 15,
    tipoRisorsa: "voce",
    obiettivo: "Riconoscere tre suoni simulati e descriverli in modo comprensibile"
  }),
  workplace_check: Object.freeze({
    tema: "Comunicazione chiara durante una simulazione di lavoro di squadra",
    destinatari: "adulti",
    durataMinuti: 30,
    tipoRisorsa: "video",
    obiettivo: "Individuare due comportamenti collaborativi e proporre un miglioramento motivato"
  })
});

export function scenarioInput(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) return null;
  const keys = Object.keys(payload);
  if (keys.length !== 1 || keys[0] !== "scenarioId") return null;
  const id = payload.scenarioId;
  if (typeof id !== "string" || !Object.hasOwn(BETA_SCENARIOS, id)) return null;
  return { ...BETA_SCENARIOS[id] };
}
export const BETA_CASE_IDS = Object.freeze(Object.keys(BETA_SCENARIOS));
