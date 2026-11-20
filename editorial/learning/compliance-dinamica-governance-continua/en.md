# Dynamic Compliance and Continuous Governance — EU AI Act, ISO/IEC 42001 and Model Drift

*Turn regulatory duties and lifecycle monitoring into operational capabilities instead of letting governance become a stack of outdated documents*

MANZO AI · AI Academy · Professional course · Six in-depth readings, a practical laboratory and reusable templates

---

## Course overview

| Item | Description |
| --- | --- |
| **Duration** | 2.5–3 hours including a 60-minute workshop |
| **Level** | Intermediate, operational |
| **Audience** | Management, compliance, DPO and legal, IT and security, project leads and process owners |
| **Suggested prerequisites** | Mental Models and AI Reliability; Governing Autonomy |
| **Deliverables** | Living AI Register, system record, responsibility matrix, drift monitoring plan and STOP triggers |
| **Legal review** | Checked against EU primary sources in November 2026; always recheck the consolidated text and relevant sector rules |

### Why this matters

Many organisations take a document-first approach to AI governance. They draft a policy, fill in a spreadsheet, present it to a committee and archive it. In a system based on probabilistic models and continuously updated cloud services, this approach is fragile. Yesterday's inventory may be accurate in form but wrong in substance today.

Your provider might replace a model without changing the visible product; real input data may shift; a team may begin using an approved tool for another purpose; or a software update might introduce a new AI feature that nobody requested or reviewed. Regulatory classification and technical reliability can drift for different reasons, and both require detection.

**Learning outcome.** Map actual AI use, including functions embedded in SaaS products; distinguish provider and deployer obligations and circumstances requiring legal reassessment; establish evidence, monitoring metrics, triggers, owners and procedures for suspending or reauthorising systems. The mission is to move from a static compliance folder to **a living, verifiable AI governance process**.

### The law as of November 2026 — verify again when using it

The legal baseline is Regulation (EU) **2024/1689**, amended by Regulation (EU) **2026/1744** (Digital Omnibus on AI), in force since 27 July 2026. Check the official [EUR-Lex amending regulation](https://eur-lex.europa.eu/eli/reg/2026/1744/oj) and the [European Commission AI Act guidance](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act).

| Date | Main application milestone | Practical note |
| --- | --- | --- |
| 2 February 2025 | Prohibited practices and AI literacy measures | These obligations already apply, subject to specific legal provisions and exceptions |
| 2 August 2025 | General-purpose AI model duties | Some transitional rules concern previously marketed models |
| 2 August 2026 | Article 50 transparency duties | Article 50(2) has a specific transition to 2 December 2026 for systems placed on the market before 2 August 2026 |
| 2 December 2027 | Annex III stand-alone high-risk AI systems | Delayed by Regulation 2026/1744 |
| 2 August 2028 | Annex I product-related high-risk systems | Delayed by Regulation 2026/1744 |

Delays **do not erase** future duties. GDPR, employment law, security duties, contractual requirements and prohibitions that already apply still matter today. The amended Article 4 requires providers and deployers to **take measures to support AI literacy** appropriate to their circumstances; this is not a general duty to award a certificate to each employee. Documenting actual measures and practical evidence is good governance.

**Important distinction:** every scenario in this course is an exercise, not a legal classification, compliance certification or substitute for competent legal and data-protection advice.

## Reading 1 · The register nobody updates

Elena manages processes in a service company with 220 employees. After learning how to govern autonomous agents, management asks her to verify the organisation's AI compliance. She finds a register created in January and approved by a committee. It lists three services: a website chatbot, an email writing assistant and a meeting summariser.

The document looks tidy. It has dates, columns and signatures. But when Elena opens the CRM supplier's portal, she finds an unexpected feature: the service has been calculating a customer-priority score for two months. Procurement never purchased a separate scoring system; the capability arrived inside an existing product. She then reads a chatbot release note: the underlying language model was replaced.

### A register is a photograph; a service is a film

The January register might have been correct when it was signed. The weakness is that the organisation no longer has a complete view of what is operating. Document-based governance fails when products change faster than records, real use departs from approved use, suppliers silently alter behaviour or nobody is accountable for review.

Elena asks each department a different question. Not “Did you complete the AI checklist?” but “What changed since we last approved this process, and how would we detect it?” This produces useful information about the CRM update, a new spreadsheet assistant and an employee's use of a personal account.

### Three properties of a living register

**First, updates are event-driven as well as scheduled.** New subscriptions, release notes, revised contract terms, incidents and requests for a different purpose each generate a review. Scheduled reviews remain valuable, but are not a substitute for detecting relevant changes.

**Second, every system has an owner.** A named organisational role is accountable for knowing the authorised purpose, reviewing evidence and making sure the record is updated. The record should also identify a deputy and escalation path.

**Third, the record connects systems with controls.** The entry must lead to current tests, monitoring metrics, known limitations, decisions, previous incidents and an actual suspension mechanism, not merely a reassuring status label.

A register should show the date of the last review, the planned next review and a link to the approval decision. Without these, the organisation cannot explain **what it knew and when it knew it**.

### A useful distinction: register entry versus approval

Inventorying a feature does not authorise its use. If Elena discovers a hidden AI scoring capability, she records its existence, assesses whether it is active and may disable the feature pending a proper review. The record can legitimately contain “Detected — not approved” rather than falsely implying that everything in the list has passed compliance.

**Micro-exercise.** Look at a non-sensitive list of software. Write down when it was last reviewed, who owns it and which new event would force the next review. If you have no access to a real inventory, use the eight fictional tools in Reading 6.

**Reflection.** If your main provider changed its underlying model tomorrow, who would notice, how soon and through which evidence?

*[ ] I have read and understood this section*

## Reading 2 · Dynamic inventory and hidden AI in suppliers

Elena discovers that the real issue is not knowing how many chatbots the company uses. It is knowing **where AI touches an operational process**, including when it appears inside tools that do not describe themselves primarily as AI services.

### Three families to inventory

| Family | Illustrative systems | Main source of uncertainty |
| --- | --- | --- |
| Internally built or configured | Company chatbot, automated agent, shared prompts and workflows | Data, tools, permissions and responsibility |
| Purchased AI product | Writing assistant, meeting transcriber, recruitment platform | Provider, contracts, retention and model versions |
| AI embedded in existing software | CRM, office suite, HR system, helpdesk, accounting package | Capability enabled by an update, perhaps by default |

The third family is easy to miss because the traditional procurement review may not run again when an existing vendor deploys an additional function.

### What a complete system record should contain

Elena starts from **purpose**: what the system actually does, its approved intended use, prohibited uses and the people affected. She then maps categories of input and output data, where the data originates, where it is sent, possible sub-processors, retention, training uses and contractual safeguards. Some technical providers may not reveal a precise underlying model version; where the version cannot be fixed, the record should explain how provider changes will be detected through release notes or regression tests.

She also records user groups and business processes, owner and deputy, legal role to be assessed, applicable controls, effective technical permissions and evidence links. A useful inventory can evolve in an ordinary spreadsheet, database or governance product; the important feature is **controlled updates**, not the platform chosen.

### Finding features nobody registered

Elena obtains the software and licensing list from IT and procurement, including departmental subscriptions. She examines release notes and settings for terms such as “assistant”, “insights”, “copilot”, “summarise”, “prediction” and “AI.” Where appropriate and lawful, IT checks authorised access and network logs. She asks departments which tools they use to accelerate routine work, without treating every disclosure as misconduct.

The tone matters. Employees who fear punishment may hide unsanctioned AI use. The goal is to make the actual environment visible and create a safe path for migrating risky uses into approved workflows.

Finally Elena checks supplier contracts, data-processing agreements and product documentation. She looks for upstream model providers, sub-processors and situations in which features were added with a default-on setting.

### The questions suppliers should answer

Which AI capabilities exist, and which are enabled by default? Can the customer disable them? Which upstream models and service providers are used? Can a version be fixed, or will model changes be announced? How does the supplier use input data, and for how long? Where is data processed and stored? Which incident and audit evidence will be available? Does the contract address changes in subprocessors, terms and features?

These answers must be **dated and linked** to the affected system. “The vendor told us everything was fine” cannot function as a verifiable control.

### A discovery is not proof of noncompliance

A feature detected by inventory may be legitimate, harmless, high risk, or disabled. Its name alone does not prove a legal status. Elena records what is known, what is uncertain and what requires assessment. This protects the organisation against both unwarranted alarm and the opposite mistake of automatic approval.

**Micro-exercise.** Select an office, CRM or HR product, or a fictional equivalent. Find one embedded AI function and describe its purpose, data categories, provider and owner. Indicate what remains to be confirmed.

**Reflection.** Which system in your workplace gained an AI function after the original purchasing decision? Who authorised that change?

*[ ] I have read and understood this section*

## Reading 3 · Roles and risks: when a deployer may become a provider

Elena discovers that the HR department configured a general writing assistant to rank applications for vacancies. The software was not originally adopted as a hiring decision system. The department has changed its **purpose**, and that is legally significant even if the model name and user interface did not change.

### Know the roles before assigning obligations

Under the EU AI Act, a **provider** is generally the party developing, or having developed, an AI system and placing it on the market or putting it into service under its name or trademark. A **deployer** generally uses an AI system under its authority in a professional context. Their duties are not identical.

For systems within the high-risk framework, providers face obligations relating to risk management, data governance, documentation, conformity and quality management; deployers have their own operational obligations, including appropriate use, oversight, monitoring and other provisions according to the applicable articles and effective dates.

A company may be both provider for one system and deployer for another. Neither being a small organisation nor merely calling an AI tool “internal” resolves the question.

### Article 25 and a new intended purpose

Article 25 addresses situations in which a distributor, importer, deployer or another party may become subject to **provider obligations**. Relevant cases include placing a pre-existing high-risk system under its own name or trademark, making a substantial modification meeting the conditions in the law, and changing the intended purpose of a non-high-risk system so that it becomes high-risk.

The legal consequence is **conditional, not automatic**. It depends on the actual system, the intended purpose, the conduct of the organisation and the applicable provisions, including Article 6 and Annex III. Simply typing an HR prompt does not establish the whole legal analysis. Elena therefore suspends unassessed use while the appropriate internal specialists examine the deployment.

### A documented intended purpose is operationally useful

A concrete record might read: “Summarise internal meeting notes for team reference only. Do not use the output to assess employee performance.” Another department cannot silently change that to “rank employee competence” without prior reassessment.

The purpose must be monitored in the real process, not only written on an onboarding form. Elena compares the intended users, actual access patterns, logs and decisions made from outputs. She wants the business owner to report changed uses before they are operational.

### A preliminary risk classification sequence

**Question one: is a prohibited practice involved?** Article 5 establishes prohibited AI practices and specific exceptions, including relevant restrictions on emotion recognition in workplace and education contexts. A prohibited use requires a different response from an ordinary assessment.

**Question two: does the use fall into Annex III or a product case under Annex I?** Annex III includes certain employment, education and access-to-essential-services uses. Creditworthiness assessment of **natural persons** is an example, subject to the precise text and exceptions. A company-credit analysis is not automatically the same legal category.

**Question three: does a relevant transparency obligation arise?** Article 50 contains distinct obligations for systems interacting with individuals and for some kinds of synthetic or manipulated content, subject to conditions and exceptions. It does not mean “every AI-generated sentence needs a universal label.”

**Question four: what else applies?** GDPR, including Article 22 where its conditions are met, employment rules, contracts, intellectual property and sector legislation may apply independently of high-risk AI Act dates.

The Article 6(3) exceptions for certain Annex III systems are technical and legally conditional, with documentation and potentially registration consequences. The course's traffic-light classification is only a **teaching triage**, not a complete compliance decision.

### Four realistic fictional decisions

**A — CV ranking using a generic assistant.** Recruitment is an Annex III area; Elena marks it for urgent legal assessment, stops unassessed automated rankings, considers anti-discrimination and data protection, and evaluates possible Article 25 consequences without presuming them.

**B — Public customer-support chatbot.** Elena checks Article 50's transparency requirements, notice to users, data flows, escalation to a person and whether the chatbot actually makes decisions on rights or credit.

**C — Meeting summaries.** A general summariser may be less risky under the AI Act, but recordings, consent or information duties, retention, labour context and unauthorised employee evaluation remain relevant.

**D — Customer-credit scoring.** Elena must distinguish natural persons, sole traders and legal entities, and establish the actual purpose. She must not use a broad “finance equals high risk” shortcut.

**Micro-exercise.** Write one approved use and one proposed alternative use of the same tool. Determine what facts would be required before the alternative could be assessed and authorised.

**Reflection.** Who prevents a previously approved assistant from being repurposed for people-related decisions without review?

*[ ] I have read and understood this section*

## Reading 4 · EU AI Act, ISO/IEC 42001 and European standards: different functions

A legal adviser asks Elena: “Should we obtain ISO 42001 certification to comply with the AI Act?” Elena replies that **the relationship is not that simple**. A management-system standard and a binding EU regulation serve different purposes; certification in one framework is not blanket legal compliance with another.

### Three instruments

| Instrument | Nature | Practical role | Important limit |
| --- | --- | --- | --- |
| EU AI Act (Regulation 2024/1689 as amended by 2026/1744) | Binding European regulation within its scope | Roles, prohibited practices, high-risk systems, transparency, obligations and enforcement | Applies in stages; case-specific legal interpretation required |
| ISO/IEC 42001:2023 | Voluntary international AI Management System (AIMS) standard | Governance across an organisation: policy, impact and risk assessment, owners, audit and continual improvement | Certification does not automatically prove EU AI Act compliance |
| EN 18286:2026 | Voluntary European harmonised quality-management-system standard linked to the AI Act | Helps providers of high-risk systems implement Article 17 QMS requirements | Limited to relevant QMS requirements; not a complete technical product conformity standard |

The European Commission published the reference to EN 18286:2026 in the Official Journal in October 2026. That gives a pathway to a **presumption of conformity within the stated scope of the harmonised reference**, rather than a blanket presumption for every AI system and obligation. [European Commission on EN 18286](https://digital-strategy.ec.europa.eu/en/library/first-harmonised-standard-supporting-ai-act-published-official-journal).

### ISO 42001 is about managing AI in an organisation

An AIMS establishes governance structures, roles, controls, management reviews, improvement mechanisms and responsible practices. Organisations that already operate quality, information-security or privacy frameworks can align these arrangements rather than building isolated paperwork.

An ISO management-system certificate must be interpreted with its **scope, issuing body and assessment date**. It does not, by itself, certify every deployed AI system or satisfy all regulatory requirements. [ISO/IEC 42001](https://www.iso.org/standard/42001).

### EN 18286 is not the entire technical assessment

It specifically addresses a **quality management system** for EU AI Act regulatory purposes, linked to Article 17. Other technical system requirements—including robustness, accuracy, cybersecurity and particular documentation obligations—must be analysed using the applicable law, guidance and other relevant standards. Confusing organisational governance with product compliance can create a false sense of assurance.

This matters for Elena's company. Primarily acting as a deployer, it might use ISO/IEC 42001 as a helpful framework. If it becomes a provider, more product and quality-management obligations may need assessment. A provider certificate cannot exempt the deployer from its own duties.

### One system, one evidence map

Elena proposes a single control matrix linking business processes to legal provisions, security measures, data protection, internal policy and applicable standards. Each row names an owner, a control, supporting evidence, last test and due date.

Duplicating the same incident log in separate GDPR, AI and ISO folders creates inconsistencies. Centralised evidence can support multiple review frameworks, while each specific obligation remains identifiable.

### The Italian context and cross-border applicability

Italy's Law **132/2025** concerns artificial intelligence and sits alongside the European framework. National law and sector obligations must be checked for the organisation concerned. For multinational teams, local legal rules and the location of persons affected may change the analysis; do not assume that one generic checklist suffices. [Italian law on Normattiva](https://www.normattiva.it/eli/stato/LEGGE/2025/09/23/132).

**Micro-exercise.** Make a three-column table labelled AI Act, ISO 42001 and GDPR. For the same fictional AI assistant, write one concrete question under each column. Explain why one answer does not replace the others.

**Reflection.** Do your legal, IT, privacy and quality functions review one joined evidence set or several conflicting spreadsheets?

*[ ] I have read and understood this section*

## Reading 5 · Silent drift: baselines, metrics, triggers and action

One morning Elena notices that the customer-support bot's escalation rate has risen from 12% to 21%. Nobody changed the prompt. The provider introduced a new model two weeks earlier. Answers are now longer, but they are less accurate for recently added products.

The correlation deserves investigation; it does not yet prove that the provider's update caused the problem. Other changes may have occurred in customer questions, product information or a connected knowledge base.

### Drift has several possible causes

**Model or service drift.** A supplier switches the underlying model or changes routing, prompting or system settings. Even a provider-controlled alias can point to a different model over time.

**Data drift.** Customers ask different questions, a new product arrives or the seasonal distribution of inputs changes. A once-representative test set may no longer reflect real-world cases.

**Retrieval or connector drift.** The document collection, knowledge base, APIs or tool permissions change. The model may behave similarly while retrieving different evidence.

**Purpose or compliance drift.** Users apply a tool to tasks not covered by the original approval; contracts, processing terms or relevant legal obligations change.

Avoid describing all of these as “model drift.” The practical question is **what changed, how could it affect risk and what will trigger review**.

### Four parts of continuous monitoring

1. **Baseline.** Maintain a fixed, documented set of representative test cases and expected outcomes. Include some missing-data cases and failures, not only straightforward questions.
2. **Metrics.** Define measurements with frequency, units, an owner and decision threshold.
3. **Trigger rules.** Define events that require investigation, restriction, testing or stopping, independent of the regular calendar.
4. **Responsibility and reauthorisation.** Assign who can review, stop, approve changes and restart under written conditions.

Possible metrics include human escalation rate; accuracy on a reviewed test set; unsupported-answer rate; empty responses or tool-call failures; repeated tool execution; user complaints; and unequal error patterns affecting people. Metrics need carefully defined denominators and sampling procedures, otherwise apparent changes may be caused by the measurement process.

### A threshold should tell someone what to do

A team might decide that an escalation increase above an internally determined threshold for two consecutive reviews requires investigation. That example is **not a universal safe or unsafe threshold**. For a critical process, a single serious incident may already justify a pause.

Triggers may include a model version change, altered supplier terms, a new audience or purpose, an incident, new regulator guidance or measured degradation. For each event, the action must be written: **STOP, constrain, retest, reassess or reapprove**.

Elena records who receives the alert, the deadline for the decision and what evidence permits the service to resume. A trigger with no assigned response is only a note.

### Monitoring does not remove the need for incident response

Even rigorous controls cannot prevent every failure. The organisation needs to document incidents, identify affected systems and persons, correct the process and preserve lessons learned. High-risk systems may face specific monitoring and serious-incident duties when those provisions apply. The existence of this future timetable does not remove present privacy, security or sector obligations.

### An example of a regression test

Elena uses twenty fictional support questions with approved reference answers and labels. She repeats them after the supplier's update and compares unsupported statements, escalation and missed exclusions. She also examines new real-world categories using synthetic examples. If outcomes degrade, she temporarily reduces capabilities and asks the owner to approve a revised plan.

**Micro-exercise.** Define three metrics and three triggers for a fictional customer-service bot. Give each a threshold, frequency, owner, action and reactivation condition. Describe one test case the model must fail safely.

**Reflection.** Which monitoring mechanism would tell you if the provider changed the underlying model without warning?

*[ ] I have read and understood this section*

## Reading 6 · Workshop: Express Audit of an AI ecosystem

**Duration:** 60 minutes, individually or in teams of three or four. **Information:** fictional scenarios only; do not upload real contracts, employee files, customer information or access tokens.

Elena now builds a living governance record for an invented 220-person service business. The laboratory combines inventory, legal triage and continuous monitoring rather than repeating three disconnected exercises.

### Stage 1 · Hunt for hidden AI (15 minutes)

Examine eight tools. Identify whether AI features are present, the data categories, possible external processing, a proposed System Owner and the evidence needed.

| # | Service | Inventory note |
| --- | --- | --- |
| 1 | HR management | “Candidate recommendations” enabled in a recent update |
| 2 | Sales CRM | Customer-priority score and email summaries |
| 3 | Office email/calendar suite | Writing assistant included in the subscription |
| 4 | Customer helpdesk | Website chatbot connected to a knowledge base |
| 5 | Meeting-transcription tool | Records, transcribes and summarises calls |
| 6 | Shared spreadsheet | Natural-language analysis capability |
| 7 | Accounting package | Automatic invoice categorisation |
| 8 | Team productivity platform | Tasks-and-notes AI assistant enabled by individual users |

**Expected finding:** according to these descriptions, all eight include AI functionality. That does not mean all eight are equally risky or necessarily enabled for every user. Determine which handle personal information, interact externally or influence decisions about individuals. Check activation settings and supplier evidence rather than guessing.

**Deliverable:** one register entry per system, with an authorised use and an open-questions column.

### Stage 2 · AI Act triage and changing roles (20 minutes)

Consider four fictional cases and answer: potential category, duties already relevant, circumstances requiring an Article 25 provider-role review and immediate action.

**A — Automatic CV ranking.** A generic assistant scores and orders applicants. Employment is an Annex III area. The correct step is to prevent unassessed use, evaluate the exact legal classification and roles, review data protection and discrimination obligations and, as necessary, select appropriately assessed tools.

**B — External support chatbot.** Check whether user notices comply with Article 50 and other applicable requirements. Verify data protection, scope, human escalation and whether the bot actually makes consequential decisions.

**C — Internal meeting summaries.** Check recording and privacy rules, access to transcripts, retention and the prohibition of repurposing notes to unassessed people evaluations. An ordinary summary and employment-related profiling are different uses.

**D — Financial reliability of customers.** Ask first whether customers are natural persons, sole traders or legal entities, and whether scores affect decisions. Article 22 GDPR and Annex III assessment cannot be resolved from the word “financial” alone.

**Important:** if two competent reviewers disagree, document the question and escalate it; do not turn an indicative educational table into a binding legal opinion.

### Stage 3 · Anti-drift monitoring plan (25 minutes)

Choose the most sensitive fictional service. Complete a table of **three metrics** with definition, threshold, frequency and measurement owner. Then define **three triggers**, each with immediate response, decision owner and explicit reactivation test.

Record the baseline: which cases, which expected results, who evaluated them and when tests will be rerun. Finally identify evidence retained: supplier correspondence, tests, approval records, incident notes and minimally necessary logs.

For example, the helpdesk owner might track escalating cases and unsupported answers. A provider model version change triggers retesting. A serious data incident triggers immediate suspension under the organisation's incident procedure.

### Scoring and the hard STOP rule

Rate five dimensions 0, 1 or 2: (A) complete system inventory and owner; (B) defined purposes, legal roles and documented doubts; (C) measures and baseline; (D) triggers with real actions and reactivation; (E) verifiable supporting evidence.

**STOP regardless of total** if a live system has no responsible owner, a potentially prohibited or high-risk purpose is being used without necessary assessment, or nobody has authority and means to stop it. In this classroom, STOP is a **design decision within the simulation**, not a declaration that an actual organisation is legally noncompliant.

**Final question.** Can you show an auditor which AI systems exist, why each is used, who owns the risks and which event would make you stop each one?

*[ ] I have read and understood this section*

---

## Operational toolkit

### 1. Living AI Register — one row per system

| Field | Fill in / evidence |
| --- | --- |
| System ID and name | Unique identifier |
| Provider, service, plan, model/version | Where known; otherwise change-detection method |
| Family | Internal / dedicated AI product / AI embedded in SaaS |
| Approved purpose and excluded uses | One precise sentence each |
| Users and business process | Affected groups, staff roles |
| Inputs, outputs, data categories | Origin, flow, storage and external transfers |
| Organisation's AI Act role | Deployer / provider / requires assessment |
| Risk classification and reasoning | Prohibited / high risk / transparency / other / uncertain |
| Supplier assurances | Training, retention, subprocessors, notice and change controls |
| Human oversight | Owner, reviewer, authority and action limits |
| Owner and substitute | Roles, contacts and escalation |
| Metrics, baseline and triggers | Link to monitoring record |
| Last and next review | Date and event conditions |
| Evidence | Tests, logs, approvals, incident records |

### 2. Illustrative RACI matrix

**R = Responsible (does work); A = Accountable (owns result); C = Consulted; I = Informed.** Assign a single clearly accountable role for each governance decision; adapt to the organisation.

| Activity | Business | System Owner | IT/Security | DPO/Privacy | Legal/Compliance |
| --- | --- | --- | --- | --- | --- |
| Inventory new feature | R | A | C | C | I |
| Approve purpose | A | R | C | C | C |
| Analyse legal category | C | C | I | C | A/R |
| Monitor metrics | I | A/R | R | I | I |
| Suspend an AI service | A | R | R | I | I |
| Reapprove changed scope | A | R | C | C | C |

### 3. Review calendar and 30/60/90-day programme

**Event-driven:** procurement, new software feature, release note, contract update, incident and new intended use. **Quarterly:** review metrics and controls of key systems. **Twice yearly:** reassess the register and role classification. **Annually:** update policy, owner assignments and literacy measures. These intervals are illustrative and must change with risk.

**First 30 days:** gather inventories and owners, identify embedded AI and pause obviously unassessed uses. **By day 60:** review purposes, supplier data, contracts and necessary transparency; document who decides. **By day 90:** establish baseline tests, triggers, owners and a rehearsed suspension workflow; complete a first governance review.

### Essential glossary

**AI Register:** living list of systems, purposes, risks, controls, roles and evidence.  
**System Owner:** accountable person or role responsible for maintaining and reviewing a system.  
**Provider:** party with provider status under the relevant AI Act provisions.  
**Deployer:** party using an AI system under its authority in a professional context.  
**Intended purpose:** approved function and use context whose changes may affect risk and roles.  
**High risk:** AI Act category determined by specific legal provisions and factual circumstances.  
**Substantial modification:** legally relevant change affecting a system under defined conditions.  
**AIMS:** AI Management System, as addressed by ISO/IEC 42001.  
**QMS:** Quality Management System, linked to Article 17 and EN 18286 for relevant providers.  
**Harmonised standard:** European standard referenced by the Commission for applicable requirements and scope.  
**Model drift:** change of model behaviour or performance over time.  
**Data drift:** change in the distribution or characteristics of input data.  
**Purpose/compliance drift:** use or regulatory context departing from the approved boundary.  
**Trigger:** condition that generates an assigned review or suspension action.  
**Baseline:** recorded starting set of evaluated cases and outcomes.  
**RACI:** Responsibility/Accountability/Consultation/Information mapping.

### Primary sources and further reading

- EU AI Act, Regulation (EU) 2024/1689: https://eur-lex.europa.eu/eli/reg/2024/1689
- Digital Omnibus on AI, Regulation (EU) 2026/1744: https://eur-lex.europa.eu/eli/reg/2026/1744/oj
- European Commission, AI Act guidance: https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act
- European Commission, harmonised standard EN 18286: https://digital-strategy.ec.europa.eu/en/library/first-harmonised-standard-supporting-ai-act-published-official-journal
- ISO/IEC 42001:2023: https://www.iso.org/standard/42001
- NIST, AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- Italian Law 132/2025: https://www.normattiva.it/eli/stato/LEGGE/2025/09/23/132

*Editorial review: November 2026. Learning examples are fictional. A course score is not an audit, a legal opinion, a certification or an approval to deploy a system with real people or data.*