/**
 * Mission Studio <> Mission Copilot schema adapter · P1
 * Pure functions; zero fetch, zero storage, zero API keys.
 * Maps the existing local brief to the private Worker schema.
 */
export const COPILOT_SCHEMA = "mission-copilot-v0.1";
export const MISSION_SCHEMA = "ai-teaching-lab-mission-v0.1";
const AUDIENCE = Object.freeze({
  "Scuola primaria": "primaria",
  "Secondaria di primo grado": "secondaria_primo_grado",
  "Secondaria di secondo grado": "secondaria_secondo_grado",
  "Formazione adulti": "adulti"
});
const RESOURCE = Object.freeze({
  image: "immagini", voice: "voce", video: "video", verify: "verifica"
});
function nonempty(value, min, max) {
  return typeof value === "string" && value.trim().length >= min &&
    value.trim().length <= max && !/[\u0000-\u001f]/.test(value);
}
export function possiblyIdentifying(value) {
  if (typeof value !== "string") return true;
  return /[^\s@]+@[^\s@]+\.[^\s@]+/.test(value) ||
    /(?:\+39[\s.-]?)?(?:\d[\s.-]?){10,}/.test(value) ||
    /(?:codice\s*fiscale|matricola\s*studente|numero\s*di\s*registro)\s*[:=]/i.test(value);
}
export function toCopilotRequest(brief) {
  if (!brief || typeof brief !== "object" || Array.isArray(brief) ||
      brief.schema !== MISSION_SCHEMA || brief.approval !== false)
    throw new Error("Il brief non è una bozza Mission Studio valida.");
  const { topic, audience, minutes, mission, objective } = brief;
  if (!nonempty(topic, 3, 110) || !Object.hasOwn(AUDIENCE, audience) ||
      ![15, 30, 45].includes(minutes) || !Object.hasOwn(RESOURCE, mission) ||
      !nonempty(objective, 12, 350))
    throw new Error("Completa tema, destinatari e obiettivo (massimo 350 caratteri).");
  if (possiblyIdentifying(topic + " " + objective))
    throw new Error("Non inserire contatti o altri dati identificabili di studenti.");
  return {
    tema: topic.trim(),
    destinatari: AUDIENCE[audience],
    durataMinuti: minutes,
    tipoRisorsa: RESOURCE[mission],
    obiettivo: objective.trim()
  };
}
const within = (s, min, max) => nonempty(s, min, max);
export function validateCopilotProposal(data, expectedStatus = "bozza_non_approvata") {
  if (!data || typeof data !== "object" || Array.isArray(data) ||
      data.schema !== COPILOT_SCHEMA || data.status !== expectedStatus ||
      data.teacherApproval !== false ||
      !within(data.obiettivo, 20, 350) ||
      !Array.isArray(data.attivita) || data.attivita.length < 2 ||
      data.attivita.length > 4 ||
      !data.attivita.every(s => within(s, 12, 260)) ||
      !within(data.criteriDiVerifica, 20, 360) ||
      !within(data.adattamenti, 15, 350))
    throw new Error("La proposta non soddisfa il formato o richiede revisione.");
  return {
    obiettivo: data.obiettivo.trim(),
    attivita: data.attivita.map(x => x.trim()),
    criteriDiVerifica: data.criteriDiVerifica.trim(),
    adattamenti: data.adattamenti.trim(),
    teacherApproval: false,
    status: expectedStatus
  };
}
/**
 * Deterministic offline preview. No model inference or learning outcome claim.
 * Does not write into the user's brief or mark anything as approved.
 */
export function makeLocalSimulation(brief) {
  const request = toCopilotRequest(brief);
  const topic = request.tema;
  const activity = {
    immagini: [
      "Mostra una rappresentazione esemplificativa del tema «" + topic + "» e chiedi quali elementi notano gli studenti.",
      "Invita il gruppo a indicare almeno due relazioni, distinguendo osservazioni e interpretazioni."
    ],
    voce: [
      "Prepara una spiegazione ascoltabile sul tema «" + topic + "», accompagnata dalla trascrizione.",
      "Chiedi di riformulare un concetto e produrre un esempio usando parole proprie."
    ],
    video: [
      "Presenta tre brevi scene collegate al tema «" + topic + "», anticipando la domanda da risolvere.",
      "Fai riordinare le scene e motivare il collegamento fra il primo e l'ultimo passaggio."
    ],
    verifica: [
      "Presenta un'affermazione controllabile sul tema «" + topic + "», evitando fatti non documentati.",
      "Fai cercare una fonte originale e chiedi una conclusione proporzionata alle prove raccolte."
    ]
  }[request.tipoRisorsa];
  return {
    schema: COPILOT_SCHEMA,
    status: "simulazione_locale",
    teacherApproval: false,
    modelUsed: false,
    obiettivo: "Riconoscere e spiegare almeno una relazione pertinente al tema «" + topic + "» attraverso un'attività guidata.",
    attivita: activity,
    criteriDiVerifica:
      "Ogni partecipante produce una breve evidenza osservabile e motiva almeno una scelta con esempi controllabili.",
    adattamenti:
      "Offri istruzioni brevi, un esempio svolto, alternative testuali e tempo aggiuntivo quando necessario."
  };
}
