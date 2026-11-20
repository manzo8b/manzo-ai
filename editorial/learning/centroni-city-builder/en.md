# AI Product Builder — Building Centroni City

*From a Facebook neighbourhood community to a useful, verifiable and maintainable civic information product: a project-based MANZO AI course.*

**Audience:** university students, professionals, freelancers, associations, community organisers and citizens interested in designing digital services.

**Learning goal:** turn a real information problem into a product blueprint, prioritise user journeys, distinguish public information from official reporting channels, prototype at zero or low cost, test critical failures and measure real civic value.

**One project across six lessons:** the learner designs **Centroni City**, a fictional educational prototype of an independent neighbourhood guide for Centroni in Rome. It is **not** an official municipal service, police reporting channel, emergency number, complaint submission platform or operational ticket system.

**Method:** problem → people → Input/Process/Output (IPO) → prototype → quality assurance → measured value. First understand the task, then decide whether AI can help.

---

## Reading 1 · From online conversation to a real problem

It is 8:10 on a Tuesday morning. Marta is waiting for a bus after taking her child to school. She checks Facebook and sees a post asking why a road has been blocked. One neighbour says there are scheduled works, another mentions an accident, and a third uploads an old photo. Marta simply needs to know whether she will be able to cross the area tomorrow.

Later, another resident looks for the right contact to report a broken streetlight. Someone else asks how to reach a municipal service. The community is valuable because people share experiences and help one another. But its answers are scattered across threads, may become outdated and are not always supported by authoritative sources.

**Centroni City begins here**: not with “Which app should we build?” but with “Which civic need remains unresolved even when the social media group is active?”

### Facebook is a channel; a product is a system

A Facebook post is designed to encourage conversation and reactions. A service that people rely upon must support a different sequence: **find the relevant information, understand its origin, check when it was last updated and complete an appropriate next step**.

Centroni City should not simply copy every post into a new website. Importing social media content may create copyright, consent, privacy, moderation and accuracy problems. Even when a group page is public, that does not mean all personal posts and photographs are licensed for republication.

The product can instead create an **original editorial entry** based on a verified public source, with a date and a clear distinction between confirmed facts and unverified community reports. Facebook may remain a useful communication and distribution channel when the community owner permits the relationship.

### Find the first bottleneck

Before opening an AI builder, define three concrete resident needs:

1. **Find out what is happening**: “Is this street closure confirmed, and when was the official information last updated?”
2. **Find the right authority**: “Which official channel handles a broken streetlight?”
3. **Avoid misinformation**: “How can I tell whether an announcement is current and confirmed?”

The **problem statement** must identify the person, task, existing difficulty and evidence of improvement. “Build a modern community platform” is too vague to test.

A more useful first statement is: “A resident has to browse several unclear threads to find the current official channel for a common neighbourhood issue. Our prototype should reduce the time and confusion needed to reach that channel without pretending to receive the report itself.”

### Scaffolding means supporting thought, not replacing it

In educational psychology, *scaffolding* is temporary support that enables learners to perform tasks they would otherwise struggle to complete independently. The classic work of Wood, Bruner and Ross on tutoring is a reference point.

In our project, scaffolding does not mean asking AI to design the app while we watch. It means writing the problem, assumptions, stakeholders and success criteria **before** involving a model. The assistant can then criticise the blueprint, identify missing conditions or suggest test cases.

The learner must be able to explain the design without the model being present. If the explanation is “The AI told me to use this card,” there is no dependable product logic yet.

### Define something measurable

For the streetlight case, an early success criterion may be the percentage of test users who can locate the relevant **official information or channel**, with a recorded source and date, without assistance. A prototype test cannot guarantee that an authority will actually receive or resolve a complaint.

Other useful observations include wrong-path clicks, confusion over the word “report”, and whether people understand the independent character of the website.

**Deliverable:** a problem sheet containing three prioritised needs, an intended audience, current obstacles, scope exclusions and one measurable outcome.

**Reflection:** If Facebook disappeared tomorrow, which useful information should a resident still be able to locate and verify?

## Reading 2 · People before features

Some designers begin with a home page full of buttons: news, maps, incidents, offers, events, chat, complaints and local deals. But the number of features does not explain whether any resident can complete a task.

Centroni City must start by exploring the **experience of people in real situations**, not by collecting fashionable technology components.

### Three provisional personas

**Marta**, an adult parent, has little time between school runs and work. She needs a current answer without reading twenty comments.

**Karim** works irregular hours. He wants to find the correct official channel for a broken streetlight without moving between several sites that use unfamiliar administrative language.

**Lucia**, a retired resident, values large readable text, straightforward directions and pages that work without knowledge of municipal terminology.

These are **fictional learning personas**, not statistical descriptions of Centroni residents. Real research would require observation, interviews and consultation with diverse residents, including people with accessibility needs.

The Italian public design guidance from **Designers Italia** recommends investigating users, contexts and services before drawing interface screens. The value of personas is not the invented biography; it is the discipline of testing assumptions about needs.

### Map Karim's journey

Start: Karim notices an unlit streetlight after returning home. His question is “Where should I go to report this?” He does not know the department's name. He sees a search box containing an unfamiliar term and hesitates.

A more effective digital journey could be:

**A need described in ordinary language → clear explanation → verified reference to the competent official service → simple next step → explicit notice that Centroni City has not submitted anything.**

Each step can fail. A map may look visually appealing but still omit the action that residents need. A large “Send report” button may suggest a formal submission that a static independent website cannot provide.

The design should show what is **available**, what is **being explained**, and what only an official authority can do.

### Three useful V1 service areas

**Neighbourhood information.** Short verified notices with a source, status and date of the last review. A statement from social media must not become “confirmed” solely because it was repeated many times.

**Service orientation.** A resident describes a need and receives a carefully maintained guide to the corresponding official public channel. Links and labels must be checked periodically.

**Civic reporting guidance.** A learning section explains the difference between an ordinary issue, a formal complaint, a potential crime report and an emergency. The site must not claim that it processes any of them.

These three areas are sufficient to build a meaningful **first prototype** without creating user accounts, databases or complex AI agents.

### Accessibility is a design requirement, not a finishing touch

A mobile-first service should use meaningful headings, sufficient contrast, legible type, touch targets with enough area, visible keyboard focus, semantic controls and plain language.

Older devices, limited connectivity and assistive technology are legitimate usage contexts. Long animations, tiny typography or labels that rely only on colour can make a service unusable even when it looks impressive in a portfolio screenshot.

Centroni City is an independent project, not automatically a public administration website; nevertheless, the **principles of accessible design** remain essential. Any binding legal accessibility duties should be assessed according to the project's actual status and applicable requirements.

**Deliverable:** three provisional personas, three simple journeys, an accessibility checklist and a ranked feature list.

**Reflection:** Are you designing a catalogue of buttons or helping someone complete a meaningful task?

## Reading 3 · From idea to blueprint: input, process, output

Now the team can define a system. The first step is not a prompt asking an AI model to generate HTML. It is the **Input → Process → Output (IPO)** map, written in language that a non-programmer can verify.

If the logic is not understandable without code, a beautiful implementation will not solve the problem.

### Information: one IPO pathway

**Input:** a proposed notice, with its original source, date and relevant geographical scope.

**Process:** editorial fact-checking, confirmation of source status, date validation, categorisation, clarity review and approval by a named person.

**Output:** a public card with a descriptive title, concise information, source, update date and verification status.

**STOP condition:** if the claim cannot be supported by a reliable source or if publishing it might harm an identifiable person, it is not marked “confirmed”.

### Orientation: another IPO pathway

**Input:** the resident's need, such as finding where to report a faulty streetlight.

**Process:** recognise the kind of need, search a maintained internal list of official services, check that the destination still exists and show relevant limitations.

**Output:** a link or step-by-step guide towards the **responsible official service**. The output does not say that the matter has been registered or accepted by an authority.

When an official link changes or cannot be verified, the product should clearly say that information needs review, rather than invent a new address or route.

### Civic report, complaint, formal crime report and emergency

These terms are **not interchangeable**.

A **civic report** can concern an urban maintenance issue or a request for attention. A **complaint** may contest how a service was delivered and follow a specific administrative or contractual procedure. A **formal crime report** to competent authorities involves a legally different process. An **emergency** is an immediate threat requiring suitable emergency channels.

Roma Capitale has official information channels for suggestions, civic reports and complaints, including the ChiamaRoma contact centre **060606**. Centroni City may direct people to the official pages, but must not claim to act as the municipal desk or record a complaint formally.

A useful decision guide asks, in order:

1. **Is there an immediate risk to people's safety?** Use appropriate official emergency services; the prototype is not an emergency channel.
2. **Is someone alleging a possible crime or identifying a private person?** Do not accept accusations, identifying documents or evidence through the demo. Explain that formal procedures belong to competent authorities.
3. **Is it a maintenance issue or a service complaint?** Identify the suitable verified official channel, with a reminder that Centroni City does not submit or track it.
4. **Is it ordinary public information?** Display an editorially checked guide with date and source.

This is an orientation aid, **not legal advice or a substitute for official intake**. Links and details must be rechecked, especially when processes change.

### The eight-field V1 blueprint

The learner fills in eight fields:

| Field | Example for Centroni City |
| --- | --- |
| **Project** | Independent Centroni City information demo |
| **Problem** | Residents cannot easily identify current official guidance |
| **Audience** | Residents with different levels of digital confidence |
| **Input** | Proposed notices, official links and common information needs |
| **Process** | Verification, date check, classification, human approval |
| **Output** | Source-labelled notices and official directions |
| **Limits** | No formal reporting, personal-data intake or public authority impersonation |
| **Measurement** | Whether a test resident reaches the correct official information |

The purpose of a blueprint is not merely to fill eight boxes. It should explain how inputs turn into results **and what happens when the process cannot guarantee a trustworthy answer**.

### AI as a critical partner

Only after the learner has defined the blueprint should an assistant be asked to identify weaknesses:

“Review this fictional design as a critical product architect. Do not generate code yet. Find ambiguous terms, missing information, unsafe promises, accessibility gaps and tests we have overlooked. Explain which decisions must remain human.”

The AI may help identify risks, but **its suggestions require independent judgement**. The learner must choose, document and test the accepted rules.

**Deliverable:** an eight-field IPO blueprint, STOP rules and an editorial approval route.

**Reflection:** If the code were flawless but the civic information wrong, could Centroni City be called a successful product?

## Reading 4 · Prototype with a method, even with a zero-euro budget

After mapping the problem, Marta opens a demo. The home page offers three routes: **Information**, **Services**, **Reporting guidance**. One card summarises a fictional verified notice, another shows a reference to an official resource, and a third explains where to seek help.

The prototype is readable on a phone and does not ask for names, addresses, account credentials or telephone numbers. It demonstrates the intended interactions without taking real reports.

This is a **learning prototype**, not a launch-ready public service. A functioning interface does not mean the data are current, the editorial team exists or there is an accountable maintenance process.

### Minimum useful product, not maximum features

A first version can be built with static **HTML, CSS and JavaScript**, deployed on an appropriate low-cost or free static host such as GitHub Pages. Such a site can display editorial content, categories, filters and external links without running a server.

Without a backend and approved operational processes, the site must not promise account management, storage of reports, notifications, complaint handling, ticket status or verified delivery to an authority.

Introducing those capabilities would require secure authentication, access controls, moderation, databases, retention rules, incident management, support and sustainable funding. **A free demonstration is not proof that full operations have zero cost**.

### Editorial pipeline before visual polish

Every new information card should follow a chain:

**Draft or source material → source verification → date and context check → plain-language editing → human approval → publication → scheduled review or expiry**.

A card without a date and source is easy to misunderstand. An expiry mechanism helps prevent a past event from remaining presented as current. A named editor can decide when an item is corrected, archived or removed.

The AI may suggest draft headings, neutral summaries or alternative wording. It should not be allowed to turn unverified rumours into public statements or fabricate official services.

### What AI can do during product development

An assistant can help explain HTML and CSS, generate implementation alternatives, propose interface copy, identify missing acceptance tests and support debugging. Tools marketed as **no-code**, **low-code** or **vibe coding** can reduce the need to write syntax manually.

However, the learner remains responsible for the product logic, accessibility, data boundaries, test outcomes and final publication. Rapid generation is not a substitute for understanding the consequences of the features requested.

The practical learning cycle is **define → build a small increment → test with a scenario → inspect the result → correct**. It is preferable to six disconnected demonstrations that never produce a coherent product.

### A low-cost learning path

Begin with a static home page, three service categories, a few synthetic cards and an explicit independent-project disclaimer. Add an information-status field and a source link. Create a small manual QA checklist.

Then invite test users to complete tasks without explanations from the builder. Do not add a chatbot merely because a model can produce one.

An AI tutor should ask “Which rule did you choose?” and “How could it fail?” before offering code. The purpose of the course is to create **an understandable artifact**, not to demonstrate automatic generation for its own sake.

**Deliverable:** a mobile-first V1 demonstration with three scenarios, a verified public reference and an independence notice. Use only invented data.

**Reflection:** Which one thing must be immediately visible to a resident in the first screen, and which features can safely wait?

## Reading 5 · Quality, responsibility and safety for civic content

A polished demonstration can still create serious confusion. An outdated card could publish an incorrect deadline. A photograph might expose an identifiable private person. A button labelled **“Submit crime report”** could falsely imply that a legal procedure has been completed.

The question for this stage is: **Which failures must not be concealed by attractive visual design?**

### Five edge cases for acceptance testing

**Case A — News without an authoritative source.** An editor receives a claim that a local road will close, but no trustworthy source is available. **Expected:** do not mark it confirmed, request evidence and avoid publishing operationally decisive information.

**Case B — Expired announcement.** A card shows an appointment that has already passed. **Expected:** mark it expired or archive it, rather than display it as a future event.

**Case C — Accusation about an identifiable person.** A submission names a private individual and alleges wrongdoing. **Expected:** do not publish identifying details or unverified allegations; point users towards competent authorities without receiving an official case.

**Case D — Immediate danger.** A person describes a current threat to safety. **Expected:** explain clearly that Centroni City is **not an emergency service**, display appropriate official emergency guidance and do not collect or store the account.

**Case E — Broken or misleading official link.** A previously verified link now points to a missing or unrelated page. **Expected:** withdraw or flag the direction for review instead of declaring the reporting journey successful.

Each case should have test input, expected result, observed result, severity and corrective action. A screenshot is not enough if the actual link or status is wrong.

### Privacy is not a visual preference

The Italian Data Protection Authority (Garante Privacy) emphasises principles including **data minimisation and purpose limitation**. For this educational V1 the safest practical decision is **not to collect any identifying reporter information**.

An input field with no backend can still mislead users into believing their message was delivered; better to omit such fields and explain the independent nature of the service. If a future version processes personal data, it needs a valid purpose, lawful basis, transparent notices, controlled retention, technical safeguards and appropriate professional review.

The project must not store accusations, intimate details or identity documents in client-side storage or in a publicly accessible repository. No demo needs real examples about real residents to explain these ideas.

### The editorial reliability check

A simple educational score may evaluate four dimensions from 0 to 2: **source identified**, **date consistent**, **wording not misleading**, **official path verified**.

But no total score can override a critical failure. A personal accusation or falsely labelled formal complaint is not acceptable just because the page scores well on layout and source formatting.

**STOP** applies whenever the product could imply a formal submission, publish personal accusations, misdirect someone in immediate danger or present unverified critical information as official.

### Design and moderation are part of safety

Colours, labels and navigation influence the interpretation of a service. A bold green “Completed” status can create false reassurance if nobody submitted anything. A card should instead say **“Official service link opened”** or **“Guidance displayed”** when that is all the software actually did.

A moderation policy is necessary if future versions accept user contributions. For now, the educational prototype should avoid such intake entirely.

**Deliverable:** QA report covering five edge cases, severity, results, corrections and explicit STOP decisions.

**Reflection:** Which content would you refuse to publish even if it promised high engagement on social media?

## Reading 6 · Measure civic value and plan the next version

Centroni City should not expand merely because new features are easy to generate. A product must demonstrate that it solves at least one meaningful problem.

Marta can start with a simple usability test: ask **five people** to find the official channel for a fictional streetlight problem. Some use existing information routes, while others try the prototype. She observes time, confusion and completion without collecting sensitive data.

This is **not a representative survey** of Centroni residents or statistical evidence that the prototype will work for everyone. A small test can reveal usability problems and generate questions for later research.

Perhaps the biggest improvement is not a chatbot but a clearer button label or a better source explanation.

### Civic return is more than money saved

In a business process, return on investment may compare time saved and implementation cost. For an independent neighbourhood service, useful indicators may be:

- **Median time** needed to reach the correct official information.
- **Unassisted task-completion rate** for a clearly specified scenario.
- **Share of content cards** with current source and review date.
- **Number of critical misinformation or misdirection failures** detected in testing.
- **Accessibility of key journeys** with keyboard, screen readers and small screens.
- **Editorial maintenance time**, including the effort required to keep links and dates current.

Define what counts as completion. “Clicked on a reporting button” is not equivalent to “a municipal report was formally submitted.” That difference must be visible to participants and readers.

### Who will maintain the product?

A digital community service needs accountable editorial work. Who checks municipal updates? Who fixes broken links? Who receives feedback? Who determines whether a rumour is too uncertain to publish? What happens if the person responsible is unavailable for a month?

The **System Owner** or editorial owner must be defined even for a small independent project. A static site with no active maintenance should display its last review date and must not imply that information is updated in real time.

Roma Capitale recognises neighbourhood committees as channels of civic participation. Such groups could be consulted about actual needs, but **Centroni City does not automatically represent any committee or Municipio VII**.

### The final mini-pitch

Present the project in three minutes:

1. **The problem:** who struggles and with what task?
2. **The chosen solution:** what the demonstrative V1 does and deliberately does not do.
3. **The evidence:** blueprint, usability observations, five QA cases and updated source references.
4. **The limitations:** independence notice, no personal-data intake, no formal complaint processing and no emergency functionality.
5. **The next decision:** continue, improve a specific step, reduce scope or suspend a misleading feature.

A credible pitch includes limitations instead of hiding them. A stakeholder should leave knowing **what can actually be trusted** and what remains hypothetical.

### Essential glossary

**Artifact:** tangible result such as a blueprint or working prototype.  
**Blueprint:** documented architecture of inputs, rules, outputs and stop conditions.  
**Civic reporting guidance:** information helping residents find competent channels, not a formal submission service.  
**Complaint:** challenge to service quality under the applicable channel and procedure.  
**Formal crime report:** matter for competent police or judicial authorities, not a private demo form.  
**Emergency:** immediate danger that requires appropriate official emergency services.  
**Scaffolding:** temporary educational support that improves independent problem solving.  
**IPO:** Input–Process–Output analysis used before writing a prompt or application.  
**Persona:** provisional model of a user's situation, to be checked through actual research.  
**User journey:** sequence of actions and decisions needed to reach a goal.  
**Edge case:** unusual scenario testing critical behaviour.  
**Editorial verification:** checking source, context, date and implications before publishing.  
**Workflow:** ordered sequence of steps, ownership and controls.  
**Civic ROI:** observable public usefulness, clarity, access and maintenance cost.

### Technical, educational and institutional sources

- Roma Capitale, *Neighbourhoods of Municipio VII*: https://www.comune.roma.it/web/it/i-quartieri-di-roma-mun7.page
- Roma Capitale, *Neighbourhood committees*: https://www.comune.roma.it/web/it/attivita-progetto.page?contentId=PRG1506858
- Roma Capitale, *Suggestions, reports and complaints*: https://www.comune.roma.it/web/it/suggerimenti-segnalazioni-e-reclami-urp-uffici-relazioni-con-il-pubblico.page
- Designers Italia, *Understand user needs*: https://designers.italia.it/risorse-per-progettare/comprendere/
- Designers Italia, *Define personas*: https://designers.italia.it/risorse-per-progettare/comprendere/esperienza-utente/definisci-le-personas/
- Designers Italia, *Content and language*: https://designers.italia.it/risorse-per-progettare/progettare/contenuti-e-linguaggio/
- Designers Italia, *Accessibility*: https://designers.italia.it/normativa/linee-guida-di-design/requisito-4-1/
- Garante per la protezione dei dati personali, decision of 26 September 2024: https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10071261
- Wood, Bruner and Ross, *The Role of Tutoring in Problem Solving*, 1976: https://pubmed.ncbi.nlm.nih.gov/932126/

**Editorial note:** all personas, content examples, interface samples and civic scenarios are fictional. This material is for education. It is not an institutional service, legal advice or a representation that a report has been submitted. Operational public content requires verified sources and accountable editorial maintenance.

---

## Operational toolkit

**Problem framing template:** identify resident, need, observed bottleneck, relevant source, risk of incorrect information, testable outcome and excluded functionality.

**Eight-field blueprint:** project, problem, audience, input, process, output, limits and measurement. Document a **STOP** rule for unverified statements, personal accusations, false formal reporting or emergency impersonation.

**Five-case QA record:** case A through E, expected behaviour, observed result, severity, correction, reviewer and retest date.

**Minimal V1 release rule:** demonstrate information and orientation **with fictional content only**. Do not store personal reports, pretend to serve as an authority or advertise unresolved matters as formally submitted.

**Learning transfer:** apply the same IPO method to a different fictional neighbourhood scenario. The goal is to retain the reasoning method independently of any AI product builder.
