"""Fully translated, manually written 10-item knowledge checks for both courses.

Answers are zero-based indices. Feedback explains why, instead of rewarding
guesswork or implying that a quiz score grants legal certification.
"""
QUIZ={
"compliance":{
"it":[
("Il CRM introduce un punteggio AI con un aggiornamento. Che cosa devi fare?",["Ignorarlo perché non è stato acquistato separatamente","Censirlo, verificare se è attivo e valutare scopo, dati e rischi","Considerarlo automaticamente vietato"],1,"Un aggiornamento del fornitore può aggiungere AI integrata senza passare da una nuova procedura di acquisto."),
("Che cosa rende «vivo» il Registro AI?",["Solo una firma annuale","Un elenco di marchi famosi","Owner, aggiornamenti per evento, test e decisioni documentate"],2,"Il registro deve cambiare quando cambiano servizi, scopi o condizioni."),
("Un assistente di scrittura viene usato per ordinare CV. Che cosa è corretto?",["La destinazione d'uso richiede nuova valutazione, e l'art. 25 può rilevare secondo le condizioni","Chi usa un prompt HR diventa sempre fornitore","I sistemi generici non hanno obblighi"],0,"Il cambio di ruolo non è automatico e dipende dai presupposti legali."),
("La certificazione ISO/IEC 42001 del fornitore...",["Certifica automaticamente ogni sistema AI","Non sostituisce la valutazione di conformità all'AI Act per l'uso concreto","Elimina tutti gli obblighi GDPR"],1,"È uno standard di sistema di gestione, non un lasciapassare per ogni prodotto."),
("EN 18286:2026 riguarda principalmente...",["La qualità della grafica di una app","I benchmark di un singolo modello","Il QMS di cui all'art. 17 per il relativo ambito"],2,"La norma armonizzata riguarda il sistema di gestione della qualità entro il suo campo."),
("Secondo la modifica UE del 2026, la scadenza generale dell'allegato III è...",["2 dicembre 2027","2 febbraio 2025","2 agosto 2028"],0,"Il Regolamento 2026/1744 ha modificato la fase di applicazione dell'alto rischio."),
("L'art. 4 riformulato obbliga generalmente a...",["Rilasciare un attestato identico a ogni lavoratore","Adottare misure per sostenere l'AI literacy in base al contesto","Comprare almeno una licenza AI"],1,"Le misure vanno calibrate; documentare formazione e apprendimento aiuta a dimostrarle."),
("L'aumento di escalation dal 12% al 21% prova che il nuovo modello è la causa?",["Sì, le date bastano","No: possono esserci cambi di dati, fonti e connettori","Sì, se le risposte sono lunghe"],1,"La correlazione temporale richiede indagine e baseline di riferimento."),
("Un trigger di revisione senza owner e azione è...",["Una notifica senza risposta operativa definita","Un sistema di monitoraggio completo","Un certificato di conformità"],0,"Servono evento, risposta, responsabile e condizione di reattivazione."),
("Un punteggio pieno in Audit Express significa...",["Conformità legale certificata","Che non serve il DPO","Solo un'autovalutazione didattica su dati sintetici"],2,"L'audit reale dipende dal sistema, dalla legge applicabile e da prove verificabili.")
],
"en":[
("A CRM adds an AI scoring feature through an update. What should happen?",["Ignore it; no separate product was bought","Inventory it, check activation and review purpose, data and risk","Automatically declare it prohibited"],1,"Embedded AI can appear after a supplier update without new procurement."),
("What makes the AI Register 'living'?",["An annual signature only","A list of popular vendors","Ownership, event-based updates, tests and recorded decisions"],2,"The inventory must evolve as services, purposes and risks change."),
("A generic writer is repurposed for CV ranking. What is correct?",["Purpose needs reassessment and Article 25 may matter if legal conditions apply","Any HR prompt automatically creates provider status","General tools cannot incur duties"],0,"Provider-role consequences are conditional, not automatic."),
("Supplier ISO/IEC 42001 certification...",["Certifies every AI product automatically","Does not replace AI Act assessment of the actual deployment","Removes all GDPR obligations"],1,"Management-system certification is not blanket compliance."),
("EN 18286:2026 mainly addresses...",["Application colours","A single model's performance leaderboard","Article 17 QMS within the relevant scope"],2,"The harmonised reference relates to a quality management system."),
("Under the 2026 EU amendment, Annex III high-risk rules generally start...",["2 December 2027","2 February 2025","2 August 2028"],0,"Regulation 2026/1744 modified the application timeline."),
("Amended Article 4 generally requires...",["The same certificate for every employee","Measures supporting context-appropriate AI literacy","At least one paid AI subscription"],1,"Literacy measures must reflect roles, knowledge and context."),
("Escalation climbs from 12% to 21%. Does that prove a model upgrade caused it?",["Yes, chronology is proof","No: data, retrieval and connectors may also have changed","Yes, if answers are longer"],1,"A temporal association is not sufficient causal evidence."),
("A trigger without an owner or response is...",["A notification without a defined operational action","Complete monitoring","A compliance certificate"],0,"Name the event, action, owner and restart criteria."),
("A perfect Express Audit score means...",["Certified compliance","The DPO is unnecessary","A synthetic learning self-assessment only"],2,"Real audits need system-specific law, facts, evidence and professional review.")
],
"es":[
("El CRM añade una función IA al actualizarse. ¿Qué debes hacer?",["Ignorarla porque no se compró por separado","Inventariarla, comprobar si está activa y evaluar finalidad, datos y riesgo","Declararla prohibida automáticamente"],1,"La IA integrada puede aparecer sin una compra nueva."),
("¿Qué convierte el Registro AI en un sistema vivo?",["Una firma anual","Una lista de marcas conocidas","Responsable, actualizaciones por eventos, pruebas y decisiones"],2,"El registro debe evolucionar con los sistemas y las finalidades."),
("Un asistente genérico se usa para ordenar CV. ¿Qué procede?",["Revisar finalidad y posible artículo 25 si se cumplen sus condiciones","Todo prompt de RR. HH. crea un proveedor automáticamente","Las herramientas genéricas no tienen obligaciones"],0,"El cambio de rol depende de los requisitos legales."),
("La certificación ISO/IEC 42001 del proveedor...",["Certifica cualquier producto de IA","No sustituye evaluar la aplicación concreta del AI Act","Elimina el RGPD"],1,"La gestión certificada no equivale a conformidad legal automática."),
("EN 18286:2026 se refiere principalmente a...",["Colores de la interfaz","Ranking de un modelo individual","QMS del artículo 17 dentro de su alcance"],2,"La norma armonizada cubre requisitos del sistema de calidad."),
("Las obligaciones del anexo III se aplican generalmente desde...",["2 de diciembre de 2027","2 de febrero de 2025","2 de agosto de 2028"],0,"El Reglamento 2026/1744 modificó el calendario."),
("El artículo 4 modificado exige en general...",["Certificados idénticos para cada persona","Medidas para apoyar la alfabetización IA según el contexto","Comprar una licencia profesional"],1,"Las medidas deben ajustarse a roles y conocimientos."),
("La escalada de tickets pasa de 12% a 21%. ¿Prueba que la culpa es del modelo?",["Sí, por el orden temporal","No: pueden cambiar datos, fuentes y conectores","Sí, si las respuestas son largas"],1,"La coincidencia temporal no demuestra causalidad."),
("Un trigger sin responsable ni acción es...",["Una alerta sin respuesta definida","Gobernanza completa","Una certificación"],0,"Cada evento necesita acción, responsable y condiciones de retorno."),
("Un resultado perfecto en el laboratorio significa...",["Conformidad legal certificada","Que no hace falta DPO","Solo autoevaluación educativa con datos sintéticos"],2,"La auditoría real requiere análisis específico y evidencias.")
]},
"augmented":{
"it":[
("Che cos'è il workslop?",["Un errore tipografico","Contenuto AI rifinito che sembra utile ma non fa avanzare il compito","Una tecnologia per riassumere"],1,"La forma convincente può trasferire costi di correzione a chi riceve."),
("L'indagine BetterUp/Stanford sul workslop è...",["Un esperimento casuale globale","Una prova che l'AI causa danni cognitivi","Una survey auto-riferita su 1.150 lavoratori USA"],2,"I risultati sono descrittivi e non automaticamente trasferibili."),
("Il 30% di 1.200 ticket lascia...",["840 ticket","780 ticket","360 ticket"],0,"1.200 × 0,70 = 840."),
("Da 1.200 ticket a 780 la riduzione è...",["30%","35%","45%"],1,"420/1.200=35%."),
("Un fornitore ISO 42001 certificato rende l'utilizzatore automaticamente conforme?",["No","Sì","Solo se la bozza è lunga"],0,"Il campo di applicazione della norma non sostituisce obblighi AI Act e GDPR."),
("Lo studio CHI 2025 con 319 partecipanti e 936 esempi dimostra...",["Che tutti perdono intelligenza","Che AI impedisce la riflessione","Associazioni auto-riferite, non un inevitabile declino causale"],2,"Occorrono disegni longitudinali e sperimentali per asserzioni causali."),
("Per una decisione con elevato impatto e giudizio conviene...",["Definire criteri umani e poi confrontare l'AI","Delegare e firmare","Scegliere la risposta più lunga"],0,"La persona mantiene la decisione e verifica fonti."),
("La revisione dell'AI da parte del modello stesso è...",["Una verifica indipendente","Un aiuto possibile, non sostituisce fonti esterne","Sempre sufficiente"],1,"Obiezioni plausibili possono essere anch'esse errate."),
("Il livello D2 del protocollo suggerisce...",["Nessun controllo","Pubblicare in automatico","Dichiarare bozza sostanziale e revisione umana"],2,"Il protocollo è interno e deve adattarsi agli obblighi reali."),
("Quale metrica misura meglio il valore operativo?",["Solo numero di prompt","Tempo complessivo, rilavorazione ed errori a valle","Numero di parole"],1,"La velocità iniziale può nascondere lavoro trasferito ai colleghi.")
],
"en":[
("What is workslop?",["A spelling error","Polished AI content that appears useful but does not advance the task","A summary tool"],1,"Convincing presentation can transfer repair work to the recipient."),
("The BetterUp/Stanford workslop study was...",["A worldwide randomised experiment","Proof AI inevitably damages cognition","A self-reported survey of 1,150 US workers"],2,"Descriptive findings cannot automatically generalise."),
("A 30% reduction from 1,200 tickets leaves...",["840 tickets","780 tickets","360 tickets"],0,"1,200 × 0.70 = 840."),
("From 1,200 to 780 tickets is a reduction of...",["30%","35%","45%"],1,"420/1,200 = 35%."),
("Does supplier ISO 42001 certification automatically make a deployer compliant?",["No","Yes","Only if the report is long"],0,"Management-system certification is not a blanket AI Act assessment."),
("The CHI 2025 study with 319 workers and 936 examples shows...",["Everyone loses intelligence","AI prevents reasoning","Self-reported associations, not inevitable causal decline"],2,"The survey does not prove long-term cognitive damage."),
("For a high-impact and judgment-heavy decision, start by...",["Writing independent human criteria before consulting AI","Delegating and signing","Choosing the longest model output"],0,"Responsibility and source review remain human."),
("An AI system's self-criticism is...",["Independent validation","Potentially useful, but no substitute for external sources","Always enough"],1,"Counterarguments can also be plausible and wrong."),
("D2 of the course's internal protocol recommends...",["No review","Automatic publication","Disclosure of substantial AI drafting and human review"],2,"A local governance model must fit actual law and contracts."),
("Which metric better indicates operational value?",["Prompts written","Total time, rework and downstream errors","Words generated"],1,"Early speed can conceal downstream costs.")
],
"es":[
("¿Qué es workslop?",["Un fallo ortográfico","Contenido IA elegante pero sin sustancia para avanzar el trabajo","Una función de resumen"],1,"La redacción convincente puede trasladar el coste de corrección."),
("La investigación BetterUp/Stanford fue...",["Experimento aleatorio mundial","Prueba de daños cognitivos inevitables","Encuesta autodeclarada de 1.150 trabajadores de EE. UU."],2,"Los resultados descriptivos no se extrapolan automáticamente."),
("Una reducción del 30% de 1.200 deja...",["840 tickets","780 tickets","360 tickets"],0,"1.200 × 0,70 = 840."),
("Pasar de 1.200 a 780 supone una reducción del...",["30%","35%","45%"],1,"420/1.200 = 35%."),
("¿La certificación ISO 42001 garantiza conformidad automática al deployer?",["No","Sí","Solo si el informe es largo"],0,"Una certificación de gestión no elimina obligaciones legales."),
("El estudio CHI 2025 de 319 trabajadores y 936 casos muestra...",["Que todos pierden inteligencia","Que IA impide razonar","Asociaciones autodeclaradas, no deterioro causal inevitable"],2,"La encuesta no demuestra daño cognitivo permanente."),
("Para una decisión de alto impacto y mucho juicio conviene...",["Definir criterios propios antes de consultar la IA","Delegar y firmar","Elegir la respuesta más extensa"],0,"El criterio y la revisión siguen siendo humanos."),
("La autocrítica del modelo es...",["Verificación independiente","Posible ayuda, pero no sustituye fuentes externas","Siempre suficiente"],1,"Las objeciones también pueden ser plausibles y falsas."),
("El nivel D2 del protocolo interno recomienda...",["Ninguna revisión","Publicar automáticamente","Declarar borrador sustancial y revisión humana"],2,"Debe adaptarse a contratos y obligaciones reales."),
("¿Qué indicador mide mejor valor operativo?",["Cantidad de prompts","Tiempo total, retrabajo y errores posteriores","Número de palabras"],1,"La rapidez de generación puede ocultar trabajo ajeno.")
]}
}
