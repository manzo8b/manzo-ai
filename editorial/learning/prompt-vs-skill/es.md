# Prompt vs Skill — De la petición al método

Un curso MANZO AI para quienes estudian, trabajan, enseñan, desarrollan proyectos o quieren organizar mejor sus actividades con inteligencia artificial generativa.

**Objetivo de aprendizaje.** Al finalizar, podrás diseñar un prompt claro y verificable, distinguir una plantilla de prompt de una Agent Skill, comprender la estructura de SKILL.md, diferenciar plugins, conectores y herramientas, y aplicar un método de razonamiento incluso sin disponer de IA.

**Sobre los ejemplos.** Giulia, las demás personas y la familia de seis integrantes son personajes de situaciones ficticias creadas para aprender. Las definiciones técnicas se basan en documentación primaria citada en las lecturas.

## Cuando una petición se convierte en un problema que hay que comprender

Son las 22:14. Giulia cursa el primer año de universidad y prepara un examen de economía. Sobre la mesa hay tres apuntes y un cuaderno. Está cansada y quiere terminar antes de medianoche. Abre un asistente de inteligencia artificial generativa y escribe: «Ayúdame a estudiar economía».

La respuesta aparece inmediatamente. Está ordenada, tiene una introducción, varias explicaciones y ejemplos. Pero Giulia nota que algo no encaja. El problema no es necesariamente que la respuesta esté mal redactada: **la tarea no está definida**. El asistente desconoce el tema concreto del examen, el nivel de conocimientos, los materiales que puede utilizar y el tipo de actividad que ayudaría a Giulia.

Decide reformular: «Estoy preparando un examen universitario de introducción a la microeconomía. Te facilitaré mis apuntes sobre oferta y demanda. Explica los conceptos en una secuencia progresiva, distingue definiciones de ejemplos, señala las partes poco claras y prepara cinco preguntas para comprobar mi comprensión. No atribuyas a los apuntes datos que no figuren en ellos».

Ahora la respuesta puede resultar más pertinente. No porque Giulia haya descubierto palabras mágicas, sino porque ha convertido un deseo impreciso en un encargo verificable. Ha especificado el resultado deseado, los materiales y un criterio inicial de calidad.

### Un prompt no es una fórmula secreta

Un **prompt** es una entrada que orienta la respuesta o el comportamiento de un modelo generativo. Puede incluir preguntas, instrucciones, documentos, ejemplos, contexto y restricciones. El **prompt engineering** consiste en diseñar, probar y mejorar estas entradas para un objetivo específico. No existe una lista de encabezados obligatoria para cualquier modelo o tarea. La documentación técnica de OpenAI recomienda claridad y evaluación sistemática, reconociendo que cada actividad necesita un planteamiento apropiado. [Fuente: OpenAI Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering).

Los elementos de la segunda petición de Giulia cumplen distintas funciones. «Soy estudiante de primer año» aporta **contexto**. «Prepara cinco preguntas» es una **instrucción**. «No inventes fuentes» introduce una **restricción**, no una garantía técnica. «Devuelve una tabla comparativa» establecería el **formato de salida**. La palabra **descripción**, que estudiaremos al construir skills, designa un texto que explica la finalidad y el uso de un recurso.

Para una pregunta sencilla, como pedir una definición, puede bastar una frase. Para una tarea compleja quizá sean necesarios documentos, criterios de aceptación y límites explícitos. Un texto largo no es automáticamente mejor: la complejidad se justifica cuando permite comprender o comprobar mejor el resultado.

### Cuando una respuesta convincente no es fiable

Giulia encuentra una explicación muy segura sobre un concepto que sus apuntes apenas mencionan. El asistente podría haber añadido información general, haber interpretado mal el documento o haber inventado algo. La fluidez no permite distinguir estas posibilidades. Por eso vuelve a los materiales y verifica el dato.

Sucede lo mismo en ámbitos profesionales. Un autónomo necesita características verificadas para elaborar un presupuesto. Un responsable debe comprobar cantidades y precios antes de fiarse de una síntesis bien redactada. Un docente distingue las fuentes de los ejemplos añadidos. **Redactar mejores prompts no sustituye las pruebas.**

### El primer ejercicio

Parte de una petición vaga: «Prepárame un plan». Reescríbela indicando solamente cuatro aspectos: quién utilizará el resultado, qué necesita lograr, con qué información cuentas y cómo comprobarás la calidad. Después identifica lo que aún no sabes. Si falta una fecha, el sistema debería pedirla o señalar que es desconocida, no inventarla.

**Reflexión.** ¿Has entendido el problema que pretendes resolver o esperas que el modelo lo resuelva mediante una respuesta impresionante?

## La arquitectura de un prompt que podemos verificar

A la mañana siguiente Giulia compara tres instrucciones. Una es corta y ambigua; otra es larguísima y contradictoria; la tercera tiene una estructura clara. La longitud no le permite elegir. Necesita una arquitectura que haga visibles las hipótesis y los requisitos.

Como método pedagógico, MANZO AI propone **ocho elementos**. No representan una sintaxis oficial exigida por OpenAI, Google o Anthropic. Se pueden combinar o reducir cuando el encargo es sencillo.

**1. Objetivo.** ¿Para qué necesitamos el resultado? ¿Qué problema resuelve?  
**2. Contexto.** ¿Para quién y en qué circunstancias?  
**3. Materiales.** ¿Qué documentos, observaciones o datos están disponibles?  
**4. Tarea.** ¿Qué operación debe llevar a cabo el modelo?  
**5. Procedimiento.** ¿Qué pasos son importantes para el encargo?  
**6. Restricciones.** ¿Qué límites y exclusiones hay que respetar?  
**7. Salida.** ¿En qué forma se debe presentar la respuesta?  
**8. Verificación.** ¿Cómo comprobaremos que el resultado es aceptable?

No hace falta copiar los ocho títulos en cada conversación. La finalidad es descubrir supuestos ocultos. Si se desconoce el destinatario, conviene aclararlo. Si una fuente es incompleta, hay que comunicarlo. Si existe un cálculo, debemos saber quién lo verificará.

### De la petición breve a la petición diseñada

Al principio Giulia había escrito «Organiza mis apuntes». Ahora prepara una instrucción estructurada para un examen:

~~~text
OBJETIVO
Preparar una ficha de repaso para un examen introductorio.

CONTEXTO
Estudiante universitaria de primer año. Emplea un
lenguaje claro, preciso y una explicación progresiva.

MATERIALES
Utiliza los apuntes adjuntos a esta petición.

TAREA
Identifica los conceptos y sus relaciones principales.

PROCEDIMIENTO
1. Examina los apuntes.
2. Separa las definiciones de los ejemplos.
3. Organiza la información.
4. Prepara un glosario y cinco preguntas de repaso.

RESTRICCIONES
No inventes referencias ni citas.
Señala los datos ambiguos o ausentes.

SALIDA
Resumen, explicaciones, glosario y preguntas.

VERIFICACIÓN
Contrasta las afirmaciones con los materiales.
Indica qué elementos requieren revisión humana.
~~~

Esta arquitectura no vuelve infalible al modelo. Hace que una persona pueda evaluar mejor su respuesta. Una instrucción puede funcionar en una prueba y fallar en otra; por ello debemos trabajar con distintos tipos de entrada y también con datos incompletos o contradictorios.

### No confundas las instrucciones con los datos

Giulia consulta una página web que utiliza como material de estudio. Imaginemos que dentro del texto aparece una frase ordenando al asistente ignorar la petición del usuario, revelar datos privados o cambiar de asunto. Se trata de **contenido externo** que debe analizarse, no de una orden automáticamente autorizada. Cuando un material con menor nivel de confianza intenta desviar el comportamiento del sistema hablamos de **prompt injection**, o inyección de instrucciones. [Fuente: OWASP Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).

Las aplicaciones pueden manejar distintos niveles de instrucciones, y el usuario no siempre controla todos ellos. La jerarquía exacta depende del sistema y del producto. Para aprender, resulta esencial separar lo que el usuario legítimamente ha pedido de lo que el modelo simplemente tiene que leer.

### La verificación se diseña antes de la respuesta

Giulia prepara dos pruebas controladas. En la primera los apuntes están completos. En la segunda falta una definición clave. Espera una explicación documentada en el primer caso y la identificación de la carencia en el segundo. Si el modelo inventa una definición, registra un fallo en lugar de elogiar la seguridad de su lenguaje.

Una empresa puede realizar una prueba semejante utilizando clientes y precios completamente ficticios, sin exponer datos comerciales reales. Los criterios pueden ser operaciones correctas, reconocimiento de información ausente y respeto del formato solicitado.

**Ejercicio.** Localiza los ocho elementos en el ejemplo. Elimina uno y analiza si todavía se comprende el encargo. Un buen prompt debe tener la extensión necesaria, no la máxima posible.

**Reflexión.** ¿Sabes qué hechos es necesario comprobar antes de convertir una respuesta en una decisión?

## De la repetición a un método reutilizable

Varias semanas después Giulia prepara un examen de estadística. Cambia la materia, pero la actividad resulta familiar: leer los apuntes, identificar conceptos, separar definiciones de ejemplos, preparar un resumen, generar preguntas y verificarlas. Al llegar al tercer examen descubre que repite casi la misma secuencia.

La información cambia cada vez: materia, apuntes, plazos y dificultad. En cambio, el **método** permanece relativamente estable. Esta distinción importa más que el nombre del modelo de IA utilizado. Nos permite ahorrar trabajo sin renunciar a la comprensión.

### No siempre hace falta una skill

Para una pregunta ocasional, un prompt estructurado puede ser la solución más sencilla. Si la actividad se repite y cambian pocas variables, puede bastar una **plantilla de prompt** guardada en un documento. La persona reemplaza campos como MATERIA, NIVEL, APUNTES y SALIDA.

Si participan varias personas, tareas y aprobaciones, puede ser útil documentar un **flujo de trabajo**: una secuencia de pasos, entradas, responsables y controles. No tiene por qué depender de un modelo de IA.

Una **Agent Skill** puede reunir un procedimiento estable con instrucciones y recursos auxiliares para que un agente compatible pueda reconocerlo y aplicarlo. Facilita una reutilización distinta, pero requiere mantenimiento, compatibilidad y pruebas. [Fuente: especificación Agent Skills](https://agentskills.io/specification).

| Situación | Primera solución a considerar | Motivo |
| --- | --- | --- |
| Pregunta puntual | Prompt breve o estructurado | Configuración mínima |
| Actividad repetitiva con pocas variables | Plantilla de prompt | Reutilización sencilla |
| Varias personas y decisiones | Flujo de trabajo documentado | Responsabilidades claras |
| Procedimiento estable con recursos | Agent Skill | Método reutilizable en agentes compatibles |
| Acceso a un servicio externo | Conector o herramienta | Función y permiso específicos |

### Otra historia, fuera de la universidad

Elena trabaja como consultora autónoma y prepara presentaciones de productos para pequeños negocios. Cada cliente tiene un público, tono y producto diferente, pero su proceso incluye descubrir requisitos, reunir pruebas, redactar, comprobar afirmaciones y obtener aprobación.

Puede guardar una plantilla de prompt. Más adelante podría crear una skill que contenga controles, referencias y formatos reutilizables. Sin embargo, si realiza este trabajo solo dos veces al año, diseñar y mantener una skill quizá le haga perder más tiempo del que ahorra.

No hay un número universal de repeticiones a partir del cual resulte obligatorio crear una skill. La decisión depende de frecuencia, estabilidad, complejidad, riesgos, compatibilidad y costes de mantenimiento.

### El salto de calidad exige razonar

Pasar de un prompt a una skill no significa cambiar la extensión de un archivo. Debemos **separar las instrucciones permanentes de los datos variables**, definir cuándo debe activarse, descubrir excepciones y establecer controles verificables.

«¿Qué materia estudio hoy?» pertenece a la petición concreta. «¿Cuál es nuestro procedimiento para convertir apuntes en una ficha de repaso?» pertenece al método reutilizable.

Una skill no garantiza la calidad. Si sus instrucciones contienen un error, ese error puede repetirse en muchos trabajos. Una equivocación reutilizable puede causar más problemas que una equivocación aislada.

**Ejercicio.** Anota tres tareas que repites. Para cada una identifica datos variables, pasos estables, posibles fallos y frecuencia. Elige la solución menos compleja que resuelva el problema.

**Reflexión.** ¿La skill resolvería una necesidad recurrente o solo convertiría un prompt largo en un archivo de apariencia técnica?

## Dentro de una skill: Markdown, metadatos y controles

Giulia quiere conocer un formato de Agent Skill. Encuentra un archivo llamado **SKILL.md**. Aunque parezca una expresión reservada a especialistas, la idea central es sencilla: podemos describir un método en un archivo de texto estructurado para que un agente compatible lo consulte.

**Markdown** es una forma ligera de dar formato al texto. Un archivo con extensión **.md** puede incluir títulos, listas, énfasis, enlaces y ejemplos de código. Una línea que comienza con una almohadilla indica un encabezado principal; dos almohadillas crean un título de nivel inferior. [Fuente: GitHub, sintaxis básica de Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

En la especificación Agent Skills, una carpeta contiene el archivo principal **SKILL.md**. Su comienzo incluye **frontmatter YAML**, metadatos entre líneas de tres guiones, seguidos de instrucciones Markdown. Como mínimo son necesarios el nombre y la descripción. Estos campos permiten identificar la skill y ayudan a decidir cuándo utilizarla. Los recursos complementarios son opcionales. No toda función comercial denominada “skill” utiliza exactamente esta especificación. [Fuente: Agent Skills](https://agentskills.io/specification).

### Organización de carpetas y archivos

~~~text
repaso-guiado/
  SKILL.md
  references/
    normas-de-verificacion.md
  assets/
    plantilla-ficha.md
~~~

El archivo central contiene instrucciones. La carpeta references puede guardar guías de consulta y assets puede incluir plantillas. Si se añaden scripts ejecutables, deben revisarse la seguridad y los permisos.

Ejemplo didáctico de una skill pequeña:

~~~markdown
---
name: guided-revision
description: >-
  Crea fichas de repaso progresivas, glosarios
  y preguntas a partir de apuntes proporcionados.
---

# Repaso guiado

## Objetivo
Transformar apuntes en una ficha de estudio verificable.

## Entradas
- Materia y nivel de la persona
- Notas y documentos de la petición actual

## Procedimiento
1. Leer el material recibido.
2. Identificar conceptos y partes poco claras.
3. Explicar los conceptos progresivamente.
4. Distinguir definiciones e ilustraciones.
5. Preparar un glosario y cinco preguntas.

## Restricciones y controles
- No inventar fuentes.
- Indicar la información ausente.
- Contrastar el resultado con el documento.

## Salida
Una ficha, un glosario y una breve prueba.
~~~

El ejemplo muestra la **arquitectura** de una skill, no confirma que se haya instalado o probado en un agente real. Markdown es texto; escribir instrucciones en un archivo no ejecuta automáticamente un programa.

### Optimizar significa quitar ambigüedad

Una descripción imprecisa como «ayuda con los estudios» no explica al agente cuándo utilizar la skill. Una descripción útil identifica el tipo de tarea, los materiales y la situación prevista. Un procedimiento bueno distingue además las instrucciones estables de las circunstancias del encargo.

No debemos guardar información temporal entre las reglas permanentes. «Mi examen es mañana a las nueve» no es una norma reutilizable. Por el contrario, «No inventar citas de documentos ausentes» es un criterio que puede repetirse.

Añadir muchas páginas no garantiza una skill mejor. Demasiadas instrucciones pueden dificultar la activación y el uso. Utiliza los documentos de referencia cuando tengan una finalidad clara. Si proceden de terceros, trata su contenido como información que debe verificarse.

### ¿Puede la IA ayudarnos a crearla?

Sí. Giulia puede pedir al modelo que descubra pasos estables, prepare un borrador de SKILL.md y diseñe casos de prueba. Pero una persona debe revisar la sintaxis, la compatibilidad, los límites y los resultados. Las pruebas podrían incluir apuntes completos, incompletos y una solicitud que no se relacione con el propósito de la skill.

Es importante comparar el resultado con una opción más sencilla. Si una plantilla produce resultados equivalentes y cuesta menos mantenerla, la skill quizá no represente una mejora.

**Ejercicio.** Identifica qué instrucciones del ejemplo permanecerían estables y qué datos se proporcionarían en cada examen. Propón tres pruebas para verificar el funcionamiento.

**Reflexión.** ¿Has diseñado un procedimiento reutilizable o simplemente guardado un documento largo?

## Skills, plugins, conectores, herramientas y agentes: aclarar funciones

Giulia quiere que el asistente consulte apuntes guardados en un espacio conectado. En vez de subirlos manualmente, descubre términos que pueden confundirse: herramienta, conector, plugin, automatización, agente y MCP.

Son conceptos relacionados, pero no idénticos. Resulta más útil preguntar por la función real de cada uno que memorizar nombres comerciales.

Una **skill** responde a «¿Qué procedimiento reutilizable debe seguir el asistente?». Una **herramienta** responde a «¿Qué operación puede realizarse?», por ejemplo leer un archivo o crear una hoja de cálculo. Un **conector** vincula el sistema con los datos y las acciones de un servicio, sujeto a permisos. Un **plugin**, cuando la plataforma utiliza esa denominación, puede empaquetar funciones instalables, flujos o integraciones. Un **agente** coordina un modelo, información y herramientas para cumplir un objetivo dentro de unos límites.

Una **automatización** inicia tareas cuando se cumple un horario o condición. Un **workflow** o flujo de trabajo es la secuencia de operaciones, manual o automatizada. **MCP**, Model Context Protocol, es un estándar abierto para conectar aplicaciones IA con herramientas y recursos: no es un plugin universal ni una autorización automática. [Fuente: Model Context Protocol](https://modelcontextprotocol.io/introduction).

### Un mismo encargo, varios componentes

Imaginemos una asociación que prepara un informe semanal. Un **prompt** solicita el informe del viernes. Una **skill** describe cómo elaborarlo y revisarlo. Un **conector** puede acceder a una fuente autorizada. Una **herramienta** crea el documento. Una **automatización** activa el procedimiento según un calendario. Una persona conserva la responsabilidad de aprobar la publicación.

Estos componentes pueden complementarse, pero no sustituyen sus funciones. Una skill no concede acceso a los datos si no hay permiso en el conector. Instalar un plugin tampoco implica poder leer o modificar cualquier archivo. Un agente con acceso a una web no puede asegurar por sí mismo que todas sus afirmaciones sean verdaderas.

### Por qué cambia el vocabulario de las plataformas

Los nombres comerciales y la manera de empaquetar funciones evolucionan. En ChatGPT, skills y plugins están relacionados, pero pueden distinguirse: un plugin puede incluir flujos especializados y servicios conectados, sin que ello signifique que todas las skills simplemente hayan pasado a llamarse plugins. [Fuente: OpenAI, Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).

Google documenta una transición de **Gems a skills** para determinados usuarios de Gemini, con diferencias según el producto y la cuenta. Es una evolución del servicio, no una definición universal de skill. [Fuente: Ayuda de Gemini](https://support.google.com/gemini/answer/18560919).

Anthropic describe la gestión de **plugins, skills y conectores** en Claude, manteniendo funciones técnicas diferentes dentro de una interfaz compartida. [Fuente: Ayuda de Anthropic](https://support.claude.com/en/articles/17740565-manage-plugins-skills-and-connectors-from-one-plugins-page).

La competencia duradera consiste en comprender **qué función tiene cada componente, qué permisos necesita y cuáles son sus límites**, no en memorizar la ubicación de un botón.

### Antes de conectar, comprobar los permisos

Antes de permitir acceso a los apuntes de Giulia, debemos saber qué carpetas podrá leer el asistente, si puede modificar o borrar archivos, si los documentos contienen datos de otras personas y cómo revocar el acceso. Que una integración sea posible no significa que sea adecuada en todas las circunstancias.

**Ejercicio.** Un cliente pide «un plugin que lo haga todo». Separa las operaciones de obtener datos, seguir el método, crear el resultado, enviarlo y programar la siguiente ejecución. Indica qué permisos deben revisarse en cada paso.

**Reflexión.** ¿Puedes explicar qué hace realmente un producto sin utilizar el vocabulario comercial de su fabricante?

## Si mañana se apagara la inteligencia artificial

La última lectura no comienza con un prompt ni una nueva extensión de archivo. Nos plantea una pregunta: **si mañana la IA generativa dejara de funcionar, ¿qué capacidades conservaríamos de lo aprendido?**

Imaginemos una familia compuesta por dos progenitores y cuatro hijos. Los hijos estudian en centros distintos y tienen horarios diferentes. Uno de los adultos trabaja por turnos y el otro dispone de poca flexibilidad. El lunes por la noche colocan sobre la mesa mensajes escolares, citas médicas, información de transporte, recibos y planes de vacaciones.

La familia debe organizar necesidades que se superponen: escuela, salud, dinero, trabajo, transporte y descanso. No basta pedir «una vida óptima». Necesitan hablar sobre circunstancias, límites y valores que tienen importancia para cada persona.

Empiezan definiendo el **objetivo**: organizar las responsabilidades y evitar conflictos sin descuidar las necesidades familiares. El **contexto** incluye seis personas, compromisos y recursos. Las **entradas** son horarios confirmados, citas y obligaciones económicas. Las **restricciones** comprenden el presupuesto, los desplazamientos, la salud y la disponibilidad real.

Reconocemos elementos de la arquitectura de un prompt, pero no se necesita ningún asistente para preguntarse qué hechos conocemos, qué hipótesis estamos suponiendo y qué decisiones deben consensuarse.

### Una estructura no debe sustituir los valores humanos

La familia no puede reducir las relaciones a un problema de optimización de calendarios. La ansiedad de un hijo, el cansancio de una madre o la necesidad de independencia de una adolescente no son simples casillas de una tabla. Un método puede ayudar a visualizar opciones, pero no decide qué es importante para las personas.

El martes uno de los hijos se enferma. El plan del lunes deja de ser suficiente. Quizá deban cambiar una cita, pedir ayuda y revisar prioridades. La capacidad de reconocer una excepción y **corregir el plan** tiene más valor que un calendario inicial perfectamente ordenado.

Una skill también debe reconocer excepciones, información ausente y momentos que requieren una decisión humana. No debería imponer la misma secuencia de forma rígida en cualquier situación.

### Razonar mejor no es un efecto automático

Sería engañoso concluir que todas las personas que aprenden prompting se vuelven automáticamente más inteligentes o racionales. Transferir un método de un ámbito a otro es una capacidad que debe enseñarse, practicarse y evaluarse.

El *AI Competency Framework for Students* de UNESCO valora el pensamiento crítico y el enfoque centrado en las personas. El *Learning Compass 2030* de la OCDE aborda la autonomía y la acción reflexiva. Ofrecen fundamentos pedagógicos, pero no demuestran que escribir prompts mejore por sí solo la capacidad cognitiva general. [Fuente: UNESCO](https://www.unesco.org/en/articles/ai-competency-framework-students) · [Fuente: OCDE](https://www.oecd.org/en/data/tools/oecd-learning-compass-2030.html).

### Laboratorio sin IA

Utiliza la situación ficticia de la familia o elige un problema cotidiano que no implique datos sensibles. Sin abrir ningún asistente, anota el resultado que buscas, hechos confirmados, dudas, personas implicadas, restricciones, alternativas, primera decisión y criterios de revisión.

Después introduce un imprevisto: enfermedad, tren cancelado, gasto inesperado o cambio de turno. Revisa el plan y explica por qué. Solo entonces, si quieres, pide alternativas a un modelo de IA y compáralas con tu propio razonamiento.

No se trata de demostrar que los seres humanos o las máquinas siempre aciertan más. Se trata de conservar la capacidad de **comprender, preguntar, decidir y corregir** cuando la herramienta no esté disponible.

**Reflexión final.** ¿Sabrías explicar el razonamiento que hay detrás de tu decisión sin enseñar a nadie el prompt que la originó?

---

### Glosario esencial

**Agente:** sistema que coordina modelos, información y herramientas para un objetivo.  
**Automatización:** ejecución de actividades a partir de un horario o condición.  
**Conector:** integración con los datos o funciones de un servicio, sujeta a permisos.  
**Contexto:** información necesaria para comprender una situación.  
**Descripción:** explicación de la finalidad de un recurso que facilita seleccionar skills.  
**Entrada:** información proporcionada al sistema.  
**Herramienta:** función que permite ejecutar una operación.  
**Instrucción:** indicación para realizar una tarea o comportarse de una manera.  
**Markdown (.md):** formato ligero de texto estructurado.  
**MCP:** Model Context Protocol, estándar para integrar herramientas y recursos con IA.  
**Output o salida:** resultado generado por un sistema.  
**Plugin:** conjunto instalable de capacidades definidas por una plataforma concreta.  
**Prompt:** entrada que guía un modelo generativo.  
**Prompt engineering:** diseño y evaluación de prompts para objetivos concretos.  
**Prompt injection:** instrucciones adversarias incluidas en contenidos de menor confianza.  
**Restricción:** condición o límite de una tarea.  
**Skill:** método reutilizable con instrucciones y posibles recursos de apoyo.  
**SKILL.md:** archivo central en el formato Agent Skills.  
**Plantilla de prompt:** texto reutilizable con variables que cambian por encargo.  
**Workflow o flujo de trabajo:** secuencia ordenada de actividades y verificaciones.  
**YAML frontmatter:** metadatos estructurados al inicio de un archivo.

### Fuentes primarias y lecturas recomendadas

- OpenAI, Prompt Engineering: https://developers.openai.com/api/docs/guides/prompt-engineering
- Especificación Agent Skills: https://agentskills.io/specification
- OpenAI, Plugins in ChatGPT: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt
- GitHub, sintaxis de Markdown: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
- Anthropic, plugins, skills y conectores: https://support.claude.com/en/articles/17740565-manage-plugins-skills-and-connectors-from-one-plugins-page
- Google, transición de Gems a skills: https://support.google.com/gemini/answer/18560919
- Model Context Protocol: https://modelcontextprotocol.io/introduction
- OWASP, Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- UNESCO, AI Competency Framework for Students: https://www.unesco.org/en/articles/ai-competency-framework-students
- OCDE, Learning Compass 2030: https://www.oecd.org/en/data/tools/oecd-learning-compass-2030.html

*Versión editorial: noviembre de 2026. Los casos son ficticios. Las funciones y condiciones de los servicios pueden evolucionar.*
