# Prompt vs Skill — From the request to the method

A MANZO AI course for anyone who studies, works, teaches, builds digital projects or wants to organise activities with generative artificial intelligence.

**Learning objective.** By the end of the course you will be able to design a clear and testable prompt, distinguish a prompt template from an Agent Skill, understand SKILL.md and Markdown, explain the roles of plugins, connectors and tools, and apply the same reasoning method in a situation where AI is not available.

**About the examples.** Giulia, the other fictional characters and the family of six are narrative learning cases. Technical definitions refer to primary documentation and are explained alongside their sources.

## When a request becomes a problem worth understanding

It is 10:14 p.m. Giulia is in her first year at university, preparing for an economics exam. Three sets of lecture notes and a notebook cover the table. She is tired and hopes to finish studying before midnight. She opens a generative AI assistant and types: “Help me study economics.”

The answer comes immediately. It is orderly, with an introduction, a few explanations and several examples. Yet Giulia senses that something is wrong. The problem is not necessarily that the text is badly written: **the task has not been defined**. The assistant does not know the examination topic, Giulia's existing knowledge, which sources she is authorised to use or which kind of exercise would help.

So she tries again: “I am preparing for a first-year microeconomics exam. I will share my notes on supply and demand. Explain the concepts in a logical sequence, distinguish definitions from examples, flag unclear parts and create five questions so I can check my understanding. Do not attribute statements to the notes that they do not contain.”

The response may now be more relevant, not because Giulia has discovered magical words, but because she has transformed a vague wish into an observable assignment. She has defined a desired result, a source and an initial quality standard.

### A prompt is not a secret formula

A **prompt** is an input that guides a generative model's response or behaviour. It may include a question, instructions, examples, documents, context and constraints. **Prompt engineering** is the practice of designing, testing and refining these inputs for a specific objective. There is no mandatory list of headings suitable for every model and task. OpenAI's technical documentation recommends clear instructions and systematic evaluation while recognising that the right structure depends on the task. [Source: OpenAI Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering).

The components of Giulia's second request have different functions. “I am a first-year student” provides **context**. “Create five questions” gives an **instruction**. “Do not invent sources” establishes a **constraint**, not a technical guarantee. “Present a comparison table” would define an **output format**. The word **description**, which will become important when we study skills, means a statement of a resource's purpose or intended use.

For an elementary question, such as asking for the definition of a term, a brief prompt may be enough. A complex task can require sources, acceptance criteria and constraints. Longer is not necessarily better: complexity is justified only when it makes the assignment clearer or its result more verifiable.

### When a plausible answer is not reliable

Giulia notices a confident explanation of a concept which her notes barely mention. The assistant may have supplemented the material with general information; it may also have misunderstood or fabricated something. The fluent style cannot establish which is true. She returns to the documents and checks the disputed statement.

The same difficulty affects professional use. A freelancer needs verified specifications to prepare an estimate. A manager should confirm quantities and prices rather than trusting a nicely written summary. A teacher must separate what is documented from illustrative explanations. **Good prompting is not a substitute for evidence.**

### A practical first exercise

Take a vague request: “Prepare a plan.” Write a revised version identifying only four elements: who will use the result, the desired outcome, the available material and how correctness will be checked. Then ask what remains unknown. If the deadline is missing, the system should ask or mark it as unknown, not invent one.

**Reflection.** Have you understood what problem you are trying to solve, or are you merely expecting the model to give an impressive answer?

## The architecture of a prompt we can actually verify

The next morning Giulia compares three versions. One is short and ambiguous, one is long and contradictory, and one is structured but concise. Their lengths do not tell her which will work best. She needs an architecture that helps her make assumptions and requirements visible.

For teaching purposes, MANZO AI proposes **eight elements**. This is a learning framework, not an official syntax that OpenAI, Google or Anthropic require. You can remove or combine elements when the task is simple.

**1. Objective.** Why do we need the answer? What problem should it solve?  
**2. Context.** Who is the user and under what circumstances?  
**3. Materials.** Which documents, observations or data may be used?  
**4. Task.** What operation should the model carry out?  
**5. Procedure.** Which steps matter for a complicated assignment?  
**6. Constraints.** Which limits and exclusions must be respected?  
**7. Output.** How should the result be presented?  
**8. Verification.** How will we judge whether the result is acceptable?

The point is not to paste eight headings into every conversation. It is to make hidden assumptions discussable. If the audience is unknown, clarify it. If the source is incomplete, record the limitation. If there is a calculation, determine who checks it.

### From the short request to the designed request

Giulia originally wrote “Organise my notes.” She now prepares a reusable prompt for a single exam:

~~~text
OBJECTIVE
Produce a study sheet for an introductory examination.

CONTEXT
First-year university student. Use clear, technically
accurate language and a progressive explanation.

MATERIALS
Use the lecture notes attached to this request.

TASK
Identify the principal concepts and their relationships.

PROCEDURE
1. Examine the notes.
2. Distinguish definitions from examples.
3. Organise the information.
4. Prepare a glossary and five questions.

CONSTRAINTS
Do not fabricate references or quotations.
Mark information that is ambiguous or absent.

OUTPUT
Overview, explanatory sections, glossary and quiz.

VERIFICATION
Check the statements against the supplied materials.
Identify anything that still requires human review.
~~~

The architecture does not make the model infallible. It makes a human assessment easier. A prompt may obey a rule in one instance and fail in another. Testing must therefore include different kinds of input, especially incomplete or conflicting materials.

### Never confuse instructions with data

Giulia reads a web page supplied as study material. Imagine that the page contains a sentence instructing the assistant to ignore the user's request, reveal private information or change the subject. That instruction is part of **external content**, not automatically an authorised command. Attempts by lower-trust material to take over the model's behaviour are known as **prompt injection**. [Source: OWASP Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).

Applications can use several levels of instructions, and the user does not necessarily control them all. The exact hierarchy varies by system and platform. The essential rule for learning is to separate what the user has legitimately asked the model to do from material the model has merely been asked to read.

### Design the quality check before the response

Giulia prepares two controlled trials. In the first, the notes are complete. In the second, one key definition is absent. She expects the assistant to provide a grounded explanation for the first case and to identify the missing information for the second. If the tool invents a definition, she records a failure instead of praising its fluency.

In a commercial setting, a similar experiment could use a completely invented client and price list so that no private customer details are exposed. Measurable checks might include accurate calculations, correct identification of missing data and compliance with the requested output format.

**Exercise.** Identify the eight elements of the example prompt. Remove one and consider whether the task is still clear. A well-designed prompt should not be longer than it needs to be.

**Reflection.** Do you know which facts must be verified before a model's answer can become a decision?

## From repetition to a reusable method

Weeks later Giulia is revising statistics. Different subject, same activity: review notes, identify key concepts, separate definitions from examples, assemble a summary, create questions and check them. At her third examination she notices that she is rewriting essentially the same procedure.

Some information changes for every examination: the subject, notes, deadlines and difficulty. The **method** stays relatively stable. That difference is more important than any particular choice of AI model. It suggests an opportunity to save work without losing understanding.

### A skill is not always the right answer

For a request used only once, a structured prompt may be the simplest solution. If a task recurs with a handful of variables, a **prompt template** may suffice. It can be saved in a text document, with fields such as SUBJECT, STUDENT LEVEL, SOURCES and OUTPUT TYPE.

For activities involving several people, decisions and systems, a **workflow** may be more appropriate. A workflow is a sequence of steps, inputs, responsibilities and quality gates, not necessarily an AI-specific product.

An **Agent Skill** can encode a stable method and supporting resources so a compatible agent knows when and how to apply them. This is a different level of reuse, but it introduces maintenance, technical constraints and a need to test how the agent behaves. [Source: Agent Skills specification](https://agentskills.io/specification).

| Situation | Likely first solution | Reason |
| --- | --- | --- |
| A one-off question | Short or structured prompt | Very little setup |
| Recurring task, few variables | Prompt template | Simple reuse |
| Multiple actors and steps | Documented workflow | Makes responsibilities visible |
| Stable method with reference files | Agent Skill | Reusable process in compatible agents |
| Need to access another service | Connector or tool | Provides specific capabilities and access |

### A second story outside education

Elena is a freelance consultant preparing product descriptions for different businesses. Every client has a different audience, tone and product, but her process involves identifying requirements, gathering evidence, drafting, checking claims and obtaining approval.

She could keep a prompt template for that process. She might eventually create a skill containing standard checks, reference materials and reusable document structures. But if she completes only two such assignments per year, a maintained skill could take more time than it saves.

There is no universal point such as “after five prompts you must create a skill.” The real criteria are frequency, stability, complexity, repeatability, compatibility, risk and maintenance costs.

### The leap requires reasoning

Moving from a prompt to a skill is not simply changing the extension of a file. You must **separate stable instructions from changing information**, define activation conditions, identify exceptions and set measurable checks.

“What subject am I studying today?” belongs in today's prompt. “How should I structure a study guide when I have notes to analyse?” belongs in a reusable method.

A skill is not a guarantee of quality. If it contains flawed assumptions, those mistakes can be repeated across many tasks. A reusable error may actually have greater impact than an error made once.

**Exercise.** List three tasks you repeat. For each, identify variable inputs, stable steps, likely errors and how often it recurs. Choose the simplest method that meets the need.

**Reflection.** Would your skill solve a recurring problem, or merely make a very long prompt look more technical?

## Inside a skill: Markdown, metadata and controls

Giulia now wants to inspect an actual Agent Skill format. She encounters a file called **SKILL.md**. At first it seems like specialist vocabulary, but the basic idea is accessible: a method is written down in a structured text file so that a compatible agent can consult it.

**Markdown** is a lightweight way to format text. A document ending in **.md** may use headings, lists, emphasis, links and code examples. A line beginning with a single hash mark introduces a top-level heading; two hash marks create a subordinate heading. [Source: GitHub basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

In the Agent Skills format, a directory contains a central **SKILL.md** file. It begins with **YAML frontmatter**, metadata between two lines of three dashes, and continues with instructions written in Markdown. The specification requires a name and description; those fields help identify and select the skill. Other resources are optional. Not every vendor feature called a “skill” implements the Agent Skills specification. [Source: Agent Skills specification](https://agentskills.io/specification).

### How the files fit together

~~~text
guided-revision/
  SKILL.md
  references/
    checking-rules.md
  assets/
    study-sheet-template.md
~~~

The central SKILL.md contains instructions. The references folder can hold more detailed guidance. The assets folder can contain templates. Scripts, if added, may execute code and therefore require additional security review.

Here is a deliberately small learning example:

~~~markdown
---
name: guided-revision
description: >-
  Create progressive revision sheets, glossaries and
  study questions from provided course notes.
---

# Guided revision

## Objective
Transform supplied notes into a checkable study sheet.

## Inputs
- Subject and learner level
- Notes and documents supplied for this assignment

## Procedure
1. Read the supplied material.
2. Identify concepts and unclear passages.
3. Explain concepts in a suitable sequence.
4. Distinguish definitions and illustrations.
5. Prepare a glossary and five review questions.

## Constraints and checks
- Do not fabricate sources.
- Mark missing information.
- Compare the final claims with the documents.

## Output
One revision sheet, glossary and short quiz.
~~~

This example demonstrates the **architecture** of a skill. It does not mean that a compatible agent has installed it or that it has passed actual tests. Markdown is text; the presence of instructions in a file does not itself execute a program.

### Optimisation means removing ambiguity

A vague description such as “help with learning” may not tell an agent when to apply the skill. A useful description names the task, intended materials and expected context. A good procedure also distinguishes instructions that are always relevant from information that changes with each assignment.

Temporary details should not be fixed inside a permanent skill. “My exam begins tomorrow morning” is not a reusable rule. Conversely, “Do not invent citations from absent notes” is a recurring quality expectation.

Adding dozens of pages does not automatically improve a skill. More material can make activation or operation unclear. Use reference files when they are genuinely necessary. If those files contain content supplied by third parties, treat them as data that may require verification.

### Can the AI help build a skill?

Yes. Giulia can ask the assistant to help identify stable steps, draft a SKILL.md and design test cases. But a human must verify syntax, compatibility, input boundaries and results. The first test might use complete notes, the second incomplete notes and the third a request unrelated to the skill.

The important comparison is with an appropriate simpler solution. If a prompt template performs equally well with lower maintenance, creating a skill may not offer an advantage.

**Exercise.** Write down which instructions in the example should stay stable and which variables should be provided for the current examination. Then propose three tests.

**Reflection.** Have you built a repeatable and testable method, or simply saved a detailed document?

## Skills, plugins, connectors, tools and agents: naming the functions

Giulia now wants her study assistant to access notes stored in a connected workspace. Instead of uploading a document manually each time, she encounters a confusing collection of terms: tool, connector, plugin, automation, agent and MCP.

These concepts are related, but they do not describe exactly the same thing. It helps to ask what practical function each one serves.

A **skill** answers “Which reusable procedure should the assistant follow?”. A **tool** answers “Which operation can be performed?”, such as reading a file or formatting a spreadsheet. A **connector** connects a system to external data or actions, subject to permissions. A **plugin**, where a product uses that term, may package installable capabilities, including workflows or connections. An **agent** coordinates a model, information and tools to pursue a goal within defined limits.

An **automation** starts a task according to a schedule or trigger. A **workflow** is the organised sequence of steps, which may be fully manual, partly automated or automated. **MCP**, the Model Context Protocol, is an open standard for connecting AI applications with tools and resources; it is neither a universal plugin nor automatic authorisation to access anything. [Source: Model Context Protocol](https://modelcontextprotocol.io/introduction).

### One assignment, different components

Consider an association preparing a weekly information report. A **prompt** asks for Friday's report. A **skill** records how reports are prepared. A **connector** may read an authorised information source. A **tool** may create a document. An **automation** may launch the process at a scheduled time. A human reviewer remains accountable for publishing information.

These components can work together, but they are not interchangeable. A skill cannot grant permissions that the connector does not have. A plugin installation does not imply unlimited rights to read files or send messages. An agent cannot reliably determine the truth of a claim merely because it can access a web page.

### Why terminology changes across platforms

Product names and packaging can change. In ChatGPT, skills and plugins describe related but distinguishable capabilities: a plugin can package specialised workflows and connected services, rather than every skill simply becoming a plugin overnight. [Source: OpenAI Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).

Google documentation describes a transition from **Gems to skills** for eligible Gemini users, with different product and account arrangements. This is a product evolution, not a universal definition of a skill. [Source: Google Gemini Help](https://support.google.com/gemini/answer/18560919).

Anthropic documents the management of **plugins, skills and connectors** in Claude, with different functions under a shared interface. [Source: Anthropic Help](https://support.claude.com/en/articles/17740565-manage-plugins-skills-and-connectors-from-one-plugins-page).

Therefore the lasting competence is to understand the **function, authority and limitations** of each capability, rather than memorising a temporary menu label.

### Permissions before convenience

Before connecting Giulia's private notes, check which folders the assistant may read, whether it can write or delete files, whether other people's personal information is involved and how access can be revoked. Integration is not the same as permission to use everything.

**Exercise.** A client asks for “one plugin that does everything.” Separate the requirements for obtaining data, following a report method, creating a result, sending it and scheduling the next run. Assign a permission check to each.

**Reflection.** Could you explain what a product does without relying on the vendor's marketing terminology?

## What if artificial intelligence went offline tomorrow?

The last lesson does not involve a new prompt or a file. It begins with a thought experiment: **if generative AI were unavailable tomorrow, what would you still know how to do?**

Imagine a family with two parents and four children. The children attend different schools and have different schedules. One parent works shifts, while the other has limited flexibility. On Monday evening they spread school messages, healthcare appointments, transport details, household bills and holiday plans across the kitchen table.

The family has several overlapping needs. There are school deadlines, medical visits, money to manage, work commitments and opportunities for rest. Nobody can simply ask for “the optimal life” without discussing the family's circumstances and values.

They begin by identifying the **objective**: organise responsibilities and avoid collisions without neglecting the people involved. The **context** includes the six family members, their commitments, their energy and their resources. The **inputs** include confirmed timetables, appointment details and bills. The **constraints** involve finances, travel, health and realistic availability.

Already these sound like concepts from prompt architecture. Yet no AI is needed to ask which facts are known, which assumptions are being made and which decisions require discussion.

### A framework must not replace human values

The family cannot treat every relationship like a scheduling optimisation problem. A younger child's anxiety, a parent's fatigue or a teenager's need for independence are not just values to enter into a calculation. A method helps people see choices clearly; it does not determine what matters to them.

On Tuesday one of the children becomes ill. The plan that looked efficient the previous evening is now inadequate. An appointment may need to change, another person may offer help and priorities must be reconsidered. The ability to recognise the exception and **revise the plan** is more important than the plan's original neatness.

A skill used by an AI system should have a similar capacity for detecting missing information, exceptions and the need for human decisions. It should not force every case into a predetermined answer.

### Better reasoning is a learning objective, not an automatic outcome

It would be misleading to conclude that everyone who learns prompting automatically becomes more rational or gains general intelligence. The ability to transfer a method from one domain to another must be taught, practised and assessed.

UNESCO's AI Competency Framework for Students supports critical thinking and human-centred use of AI. The OECD Learning Compass 2030 addresses learner agency and reflective action. These frameworks provide educational direction; they do not establish that writing prompts alone improves general cognitive ability. [Source: UNESCO](https://www.unesco.org/en/articles/ai-competency-framework-students) · [Source: OECD](https://www.oecd.org/en/data/tools/oecd-learning-compass-2030.html).

### The exercise without AI

Choose the fictional family or a non-sensitive everyday situation. Without opening any assistant, write the desired result, confirmed facts, unanswered questions, people affected, constraints, alternatives, first decision and review criteria.

Next, add an unexpected event: an illness, a cancelled train, an unexpected expense or a changed work shift. Revise your plan and explain why. Only afterwards, if you wish, let a model propose alternatives. Compare both approaches based on evidence, not who sounds more confident.

The objective is not to demonstrate that humans or machines always win. It is to preserve the capacity to **understand, question, decide and revise** when technology is unavailable.

**Final reflection.** Can you explain the reasoning behind a decision without showing someone the prompt that produced it?

---

### Essential glossary

**Agent:** a system coordinating models, information and tools toward a goal.  
**Automation:** execution triggered by time or another condition.  
**Connector:** an integration with an external service, subject to permissions.  
**Constraint:** a condition or limit for the task or output.  
**Context:** information necessary to understand the situation.  
**Description:** a statement of a resource's purpose and use; helps select skills.  
**Instruction:** guidance to perform a task or behave in a specific way.  
**Markdown (.md):** a lightweight format for structured text.  
**MCP:** Model Context Protocol, a standard for connecting AI applications to tools and resources.  
**Output:** the result delivered by a system.  
**Plugin:** an installable package of capabilities as defined by a specific platform.  
**Prompt:** input that guides a generative model.  
**Prompt engineering:** designing and evaluating prompts for specific outcomes.  
**Prompt injection:** adversarial instructions embedded in lower-trust content.  
**Prompt template:** reusable prompt with fields that change across assignments.  
**Skill:** a reusable method containing instructions and possibly resources.  
**SKILL.md:** the central instruction file in the Agent Skills format.  
**Tool:** a function that carries out a defined operation.  
**Workflow:** an organised sequence of tasks and checks.  
**YAML frontmatter:** structured metadata at the start of a file.

### Primary sources and further reading

- OpenAI, Prompt Engineering: https://developers.openai.com/api/docs/guides/prompt-engineering
- Agent Skills specification: https://agentskills.io/specification
- OpenAI, Plugins in ChatGPT: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt
- GitHub, Markdown syntax: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
- Anthropic, Plugins, skills and connectors: https://support.claude.com/en/articles/17740565-manage-plugins-skills-and-connectors-from-one-plugins-page
- Google, Gems to skills: https://support.google.com/gemini/answer/18560919
- Model Context Protocol: https://modelcontextprotocol.io/introduction
- OWASP, Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- UNESCO, AI Competency Framework for Students: https://www.unesco.org/en/articles/ai-competency-framework-students
- OECD, Learning Compass 2030: https://www.oecd.org/en/data/tools/oecd-learning-compass-2030.html

*Editorial version: November 2026. Fictional narratives are teaching examples. Product capabilities, interfaces and legal requirements may evolve.*
