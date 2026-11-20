# Compliance dinámica y gobernanza continua — EU AI Act, ISO/IEC 42001 y deriva de modelos

*Convertir las obligaciones normativas y el seguimiento del ciclo de vida en una capacidad operativa, más allá de los documentos estáticos*

MANZO AI · AI Academy · Curso profesional · Seis lecturas de profundización, laboratorio y herramientas reutilizables

---

## Ficha del curso

| Aspecto | Descripción |
| --- | --- |
| **Duración** | 2,5–3 horas, incluido un taller de 60 minutos |
| **Nivel** | Intermedio y operativo |
| **Destinatarios** | Dirección, compliance, DPO, profesionales jurídicos, IT, seguridad y responsables de procesos |
| **Requisitos recomendados** | Modelos mentales y fiabilidad de la IA; Gobernar la autonomía |
| **Producto final** | Registro de IA, ficha por sistema, matriz de responsabilidades, plan contra la deriva y condiciones de STOP |
| **Normativa** | Comprobada con fuentes primarias europeas en noviembre de 2026; revisar siempre el texto consolidado vigente |

### ¿Por qué es importante?

Muchas organizaciones abordan la gobernanza de la IA redactando una política, completando un registro inicial y archivándolo tras la aprobación del comité. Esa documentación puede estar impecable y dejar de describir la realidad al poco tiempo.

El proveedor puede actualizar el modelo sin modificar la interfaz; pueden cambiar los datos y las preguntas de los usuarios; un departamento puede emplear el asistente para otra finalidad; una aplicación que ya estaba contratada puede incorporar una función de IA sin pasar por un nuevo proceso de compras.

El riesgo no es solo técnico. Una modificación puede alterar la clasificación de un sistema, las condiciones contractuales, las medidas de seguridad y las obligaciones aplicables. Por ello debemos pasar de una fotografía normativa a **un sistema continuo de evidencias, decisiones y controles**.

**Objetivos.** Al terminar podrás localizar IA dentro de aplicaciones SaaS, documentar finalidades autorizadas y prohibidas, distinguir responsabilidades de proveedor y responsable del despliegue, determinar cuándo se necesita una nueva evaluación y diseñar métricas y acciones para contener una deriva.

**Misión.** Sustituir el archivo inerte por un registro de IA vivo, con propietarios claros, controles verificables, fechas y eventos que obligan a revisar cada autorización.

### Marco normativo de noviembre de 2026

El punto de partida es el Reglamento (UE) **2024/1689** (AI Act), modificado por el Reglamento (UE) **2026/1744**, conocido como Digital Omnibus on AI y vigente desde el 27 de julio de 2026. Consulta el [texto oficial en EUR-Lex](https://eur-lex.europa.eu/eli/reg/2026/1744/oj) y las [orientaciones de la Comisión Europea](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act).

| Fecha | Hito | Precaución |
| --- | --- | --- |
| 2 de febrero de 2025 | Prácticas prohibidas y medidas de alfabetización en IA | Ya están en aplicación, con disposiciones y excepciones específicas |
| 2 de agosto de 2025 | Obligaciones para modelos de propósito general (GPAI) | Existen disposiciones transitorias para algunos modelos anteriores |
| 2 de agosto de 2026 | Obligaciones del artículo 50 sobre transparencia | La transición del artículo 50(2) llega al 2 de diciembre de 2026 para determinados sistemas ya comercializados |
| 2 de diciembre de 2027 | Sistemas de alto riesgo independientes del anexo III | Fecha modificada por el Omnibus |
| 2 de agosto de 2028 | Sistemas de alto riesgo vinculados a productos del anexo I | Fecha modificada por el Omnibus |

**Retrasar la aplicación de una obligación no significa suprimirla.** El RGPD, la legislación laboral, la confidencialidad, la seguridad, los contratos y las prohibiciones aplicables no esperan a las nuevas fechas. El artículo 4, modificado, exige a proveedores y responsables del despliegue **adoptar medidas que apoyen la alfabetización en IA**; no establece un certificado obligatorio para cada trabajador. Conservar pruebas de acciones formativas adecuadas es una práctica recomendable.

Estos ejemplos son educativos. No constituyen un dictamen jurídico ni una clasificación automática de sistemas reales.

## Lectura 1 · El registro que nadie actualiza

Elena coordina los procesos de una empresa de servicios con 220 empleados. Después de estudiar la autonomía de los agentes de IA, la dirección le encarga una misión: comprobar si los sistemas de inteligencia artificial cumplen las normas.

Encuentra un registro preparado en enero y aprobado por el comité. Contiene tres herramientas: el chatbot público, un asistente para escribir correos y una aplicación de resúmenes de reuniones. Todo parece ordenado, con fecha, responsables y firmas.

Elena consulta el portal del proveedor de CRM y descubre una función de **puntuación automática de prioridad de clientes**, activada dos meses atrás. Nadie la había solicitado expresamente ni incluido en el registro. Después encuentra otra nota de actualización: el proveedor del chatbot sustituyó su modelo por una versión diferente. Los resultados nuevos no tienen por qué coincidir con los de enero.

### El registro es una fotografía; la operación es una película

El inventario podía ser correcto en enero. El problema no es necesariamente la mala fe, sino el paso del tiempo. La gobernanza basada solo en documentos falla cuando las funciones cambian antes de una revisión, cuando los proveedores alteran el comportamiento, cuando una persona da al servicio un nuevo uso o cuando no existe una responsabilidad asignada para detectar esas modificaciones.

Elena reformula la pregunta de auditoría. No basta «¿Tenemos un registro aprobado?». Hay que preguntar: **«¿Qué cambió desde la última autorización, cómo lo sabemos y quién debe actuar?»**

### Tres propiedades de un registro vivo

**Actualización mediante eventos y calendario.** Nuevas compras, notas de versión, cambios contractuales, incidencias y solicitudes de uso diferente generan una revisión. Los controles periódicos siguen siendo útiles, pero no sustituyen la detección de eventos.

**Responsable por sistema.** Cada entrada identifica un *System Owner* con función organizativa concreta, sustituto y vía de escalamiento. El responsable sabe para qué fue aprobado el sistema, cuáles son sus límites y cuándo deben revisarse.

**Relación con evidencias.** La ficha debe enlazar pruebas, resultados, aprobaciones, métricas, incidencias y mecanismos de suspensión. Un estado «aprobado» sin fecha ni test reciente es una declaración insuficiente.

Elena añade una distinción esencial: **descubrir una función no equivale a autorizarla**. Una fila del registro puede indicar «Detectada; pendiente de evaluación», y la función puede quedar desactivada mientras se estudia.

### La responsabilidad no puede quedarse en una columna vacía

La persona propietaria del sistema debe saber dónde consultar los cambios de su proveedor, qué usuarios lo emplean, cuándo se hizo la última prueba y qué situación obliga a detenerlo. La dirección debe apoyar esa función con tiempo, acceso y capacidad de intervención, no limitarse a asignar un nombre.

**Microejercicio.** Elige una lista de aplicaciones que no contenga datos sensibles. Indica la última revisión, el responsable y tres eventos que provocarían una nueva. Si no dispones de lista, utiliza el inventario ficticio de la lectura 6.

**Reflexión.** Si mañana tu proveedor cambiara el modelo sin anunciarlo, ¿quién lo detectaría y con qué evidencias?

*[ ] He leído y comprendido esta sección*

## Lectura 2 · Inventario dinámico e IA escondida en los proveedores

Elena entiende que no se puede gobernar lo que no se ve. Deja de preguntar «¿Qué chatbots tenemos?» y comienza a buscar **«¿Dónde interviene la IA en nuestros procesos?»**

Un asistente integrado en una suite de oficina puede leer documentos. Un CRM puede asignar prioridad a clientes. Un gestor de personal puede sugerir ordenaciones de candidaturas. No siempre se trata de productos comprados expresamente como inteligencia artificial.

### Tres familias de sistemas

| Familia | Ejemplos | Riesgo que suele pasar desapercibido |
| --- | --- | --- |
| Desarrollados o configurados internamente | Chatbot propio, agente, flujos automatizados, prompts compartidos | Diseño de permisos, datos y controles |
| Comprados como producto de IA | Asistente de escritura, transcripción, selección de personal | Condiciones contractuales, proveedor, retención y versiones |
| IA integrada en software existente | CRM, correo, hojas de cálculo, recursos humanos, helpdesk, contabilidad | Nueva capacidad incorporada con una actualización, quizá activada por defecto |

La última familia es especialmente difícil de detectar. No hubo una compra nueva que activara los controles habituales; una actualización de software modificó las capacidades disponibles.

### Qué registrar de extremo a extremo

Elena empieza por definir **qué hace** cada sistema, en **qué proceso**, para **qué usuarios** y con qué **finalidad autorizada**. Escribe además los usos expresamente excluidos. Después documenta categorías de entrada y salida: datos públicos, personales, confidenciales, financieros o de empleados. Anota procedencia, destino, país de procesamiento cuando sea relevante y servicios terceros.

Comprueba el acuerdo de tratamiento de datos, el uso para entrenamiento, los plazos de conservación, los subencargados, las cláusulas de modificación y la notificación de incidentes. Cuando el proveedor no permite fijar una versión del modelo, el registro debe documentar **cómo detectar cambios de comportamiento** mediante pruebas de regresión, comunicaciones y registros.

Una ficha útil también contiene roles, permisos técnicos reales, personal afectado, controles humanos y vínculos a evidencias. Una hoja de cálculo puede ser suficiente si existe una rutina fiable de actualización; comprar una plataforma sofisticada no resuelve por sí solo la gobernanza.

### Cómo descubrir IA no inventariada

Elena examina licencias y contratos con compras e IT; revisa notas de actualización y paneles de configuración buscando expresiones como «assistant», «copilot», «insights», «resumen» y «predicción»; solicita apoyo de seguridad para comprobar registros de acceso autorizados y entrevista a distintos departamentos.

No utiliza un enfoque persecutorio. Si las personas temen sanciones por comunicar herramientas personales, es más probable que oculten su uso. El propósito es conocer la realidad, crear alternativas aprobadas y mejorar la seguridad.

### Preguntas para el proveedor

¿Qué funciones de IA contiene el producto y cuáles están activadas por defecto? ¿Se pueden desactivar? ¿Qué modelos y subproveedores participan? ¿Es posible fijar la versión? ¿Cómo se avisan los cambios? ¿Se usan nuestros datos para entrenar? ¿Durante cuánto tiempo se conservan? ¿Dónde se tratan? ¿Qué evidencia de pruebas e incidencias facilita el proveedor? ¿Qué derechos de revisión y revocación existen?

Elena incorpora respuestas, fecha, interlocutor, versión contractual y enlaces. No acepta «El proveedor dice que está todo bien» como evidencia suficiente.

### La presencia de IA no demuestra incumplimiento

Una funcionalidad puede estar desactivada, autorizada, pendiente de evaluación o ser de bajo o alto impacto. La palabra «IA» en el nombre del producto no determina una categoría jurídica. El registro distingue **hechos conocidos, incertidumbres y decisiones pendientes**.

**Microejercicio.** Elige una aplicación de trabajo o una ficticia. Localiza una función de IA y escribe su finalidad, datos tratados, proveedor y responsable. Marca expresamente qué información falta confirmar.

**Reflexión.** ¿Qué aplicación de tu trabajo adquirió una función de IA después de la compra y quién decidió activarla?

*[ ] He leído y comprendido esta sección*

## Lectura 3 · Roles y riesgo: cuándo puedes asumir obligaciones de proveedor

Elena descubre que recursos humanos ha configurado un asistente de escritura genérico para **ordenar currículums** según su adecuación a ofertas de empleo. No se compró como plataforma de selección, pero ahora se emplea en un proceso que afecta a personas y que puede entrar en el ámbito de alto riesgo del AI Act.

El problema no es solo tecnológico. **Cambiar la finalidad puede alterar la evaluación normativa y las responsabilidades** aunque el software siga siendo el mismo.

### Proveedor y responsable del despliegue

En términos generales, el **proveedor** (*provider*) desarrolla o encarga desarrollar un sistema y lo introduce en el mercado o lo pone en servicio con su nombre o marca, según las condiciones del reglamento. El **responsable del despliegue** (*deployer*) utiliza un sistema bajo su autoridad en un contexto profesional.

Las obligaciones no son idénticas. Un proveedor de alto riesgo puede afrontar exigencias de gestión de riesgos, calidad de datos, documentación, sistemas de calidad y evaluación de conformidad, según los artículos aplicables y sus fechas. Un deployer debe atender sus propias obligaciones sobre uso, supervisión, seguimiento y otros aspectos conforme al caso.

Una organización puede ser proveedor de un sistema y deployer de otro. El tamaño o el carácter «interno» de una herramienta no resuelven automáticamente la cuestión.

### Artículo 25: la relevancia del cambio de finalidad

El artículo 25 contempla supuestos en que otro operador puede quedar sujeto a **obligaciones de proveedor**, por ejemplo al comercializar un sistema de alto riesgo con su propia marca, realizar determinadas modificaciones sustanciales o modificar la finalidad de un sistema no clasificado como alto riesgo para que pase a serlo.

**No ocurre automáticamente por escribir un prompt diferente.** Es necesario examinar el sistema real, su finalidad, las actuaciones de la organización y las condiciones de los artículos aplicables, incluidos el artículo 6 y el anexo III. Elena detiene un uso no evaluado y solicita la revisión correspondiente en vez de declarar por su cuenta una nueva categoría jurídica.

### Documentar la finalidad autorizada

Una descripción útil dice: «Resumir reuniones internas para consulta del equipo. No utilizar para valorar desempeño de empleados». Si otro departamento pretende usar los resúmenes para puntuar a trabajadores, se necesita una evaluación previa.

No basta que esta frase exista en una hoja. Elena compara finalidad aprobada, procesos reales, usuarios y decisiones tomadas a partir de los resultados. Un cambio de contexto puede hacer necesarias nuevas condiciones aunque la interfaz permanezca igual.

### Preguntas para una primera clasificación

**1. ¿Existe una práctica prohibida?** El artículo 5 establece prohibiciones concretas, con excepciones aplicables a ciertos supuestos. Entre los temas relevantes figuran usos restringidos de reconocimiento de emociones en trabajo y educación.

**2. ¿Puede tratarse de un sistema de alto riesgo de los anexos III o I?** El anexo III incluye ciertos usos en empleo, educación y acceso a servicios esenciales. La evaluación de solvencia de **personas físicas** puede entrar en el anexo, con las excepciones y condiciones expresas. Analizar el crédito de una sociedad no es automáticamente el mismo supuesto.

**3. ¿Hay deberes específicos de transparencia?** El artículo 50 incluye obligaciones distintas para interacción con personas y determinados contenidos sintéticos o manipulados. **No exige etiquetar universalmente toda frase asistida por IA**.

**4. ¿Qué otras normas intervienen?** RGPD (incluido el artículo 22 cuando se cumplen sus condiciones), derecho laboral, confidencialidad, contratos, no discriminación y legislación sectorial pueden aplicarse independientemente del calendario del alto riesgo.

Las excepciones del artículo 6(3) para determinados sistemas del anexo III requieren interpretación y justificación específicas. Las categorías del semáforo pedagógico sirven para orientar preguntas, **no sustituyen una clasificación legal documentada**.

### Cuatro situaciones ficticias

**A — Ranking de CV.** Es una finalidad relacionada con empleo del anexo III. Debe suspenderse el ranking no evaluado y revisarse el caso con especialistas, considerando riesgos de discriminación, datos personales y posible artículo 25, sin presumir consecuencias automáticas.

**B — Chatbot público de soporte.** Elena verifica los avisos del artículo 50 cuando correspondan, el alcance de las respuestas, los datos y la posibilidad de escalar a una persona. Debe determinar si el chatbot realiza o influye en decisiones con consecuencias sobre derechos.

**C — Resúmenes de reuniones internas.** Puede tratarse de un uso distinto de la evaluación de trabajadores. Hay que comprobar grabaciones, información a participantes, retención, acceso y riesgo de reutilización para valorar personas.

**D — Análisis de fiabilidad financiera.** Primero hay que aclarar si el cliente es persona física, autónomo o sociedad, qué variables se usan y qué decisiones resultan. No basta clasificar «finanzas = alto riesgo».

**Microejercicio.** Escribe una finalidad aprobada de un sistema y otra que un departamento podría introducir por comodidad. Enumera los hechos que necesitarías antes de aprobar el nuevo uso.

**Reflexión.** ¿Quién compara en tu organización lo que se autorizó con lo que las personas hacen realmente?

*[ ] He leído y comprendido esta sección*

## Lectura 4 · EU AI Act, ISO/IEC 42001 y normas europeas: funciones diferentes

El asesor jurídico pregunta a Elena: «¿Necesitamos certificarnos en ISO 42001 para cumplir el AI Act?». La respuesta no es simplemente sí o no: **son instrumentos diferentes**, y una certificación de sistema de gestión no equivale a conformidad automática de todos los sistemas utilizados.

### Tres instrumentos y tres funciones

| Instrumento | Naturaleza | Para qué sirve | Límite |
| --- | --- | --- | --- |
| EU AI Act, Reglamento 2024/1689 modificado por 2026/1744 | Legislación europea vinculante dentro de su ámbito | Establece roles, prohibiciones, transparencia, alto riesgo y otras exigencias | Se aplica por fases y exige analizar el contexto |
| ISO/IEC 42001:2023 | Norma internacional voluntaria para un sistema de gestión de IA (AIMS) | Organiza políticas, responsables, evaluación de riesgos e impactos, auditorías y mejora continua | Certificarse no demuestra automáticamente conformidad con el AI Act |
| EN 18286:2026 | Norma armonizada europea voluntaria sobre gestión de la calidad | Referencia para el sistema de gestión de calidad del artículo 17 de proveedores de alto riesgo | No sustituye todos los requisitos técnicos de un producto |

En octubre de 2026 la Comisión Europea publicó la referencia a **EN 18286:2026** en el Diario Oficial. La presunción de conformidad que puede derivarse de una norma armonizada se limita a los requisitos y el alcance de la referencia correspondiente. No implica «todo nuestro sistema cumple». [Comisión Europea](https://digital-strategy.ec.europa.eu/en/library/first-harmonised-standard-supporting-ai-act-published-official-journal).

### ISO 42001: gobierno a escala organizativa

Un sistema de gestión de IA permite definir política, funciones, revisión de proveedores, controles, seguimiento, auditorías y mejora continua. Puede integrarse con ISO 27001, calidad o protección de datos para evitar estructuras paralelas.

El significado de un certificado depende de su **alcance, fecha y organismo emisor**. Una certificación de la organización o de un proveedor no garantiza la conformidad legal de cualquier uso concreto. [ISO/IEC 42001](https://www.iso.org/standard/42001).

### EN 18286 no es una evaluación técnica completa

La norma se refiere a un **Quality Management System**, QMS, vinculado al artículo 17. Los aspectos técnicos de un sistema de alto riesgo—robustez, precisión, ciberseguridad, calidad de datos o documentación—requieren revisar los artículos y normas pertinentes. No deben confundirse gestión organizativa, QMS del proveedor y evaluación técnica de un producto.

Para Elena, cuya empresa actúa principalmente como usuaria profesional, ISO 42001 puede ser una referencia útil. EN 18286 resulta especialmente relevante si desarrolla o comercializa un sistema en calidad de proveedor bajo las condiciones pertinentes.

### Una sola matriz de evidencias

Elena construye una matriz con referencia legal, objetivo del control, responsable, prueba realizada, fecha, resultado y documentos. Conecta un mismo registro de incidentes con los marcos de IA, seguridad y privacidad, sin duplicarlo en carpetas que luego se contradigan.

La organización puede aprovechar procedimientos existentes. Un comité formal sin evidencias no es mejor que una pequeña estructura con controles reales. Lo importante es que las funciones de negocio, legal, DPO, IT y seguridad compartan hechos y decisiones.

### Contexto italiano y europeo

En Italia está vigente la Ley **132/2025** sobre inteligencia artificial, que convive con el marco europeo. La organización debe comprobar qué obligaciones nacionales y sectoriales le afectan; una plantilla genérica no reemplaza el análisis correspondiente. [Normattiva](https://www.normattiva.it/eli/stato/LEGGE/2025/09/23/132).

**Microejercicio.** Dibuja tres columnas: AI Act, ISO 42001 y RGPD. Escribe una pregunta por columna para un mismo servicio de IA y explica por qué las respuestas no son intercambiables.

**Reflexión.** ¿Tu departamento jurídico, IT, privacidad y calidad trabajan con un registro común o con documentos contradictorios?

*[ ] He leído y comprendido esta sección*

## Lectura 5 · La deriva silenciosa: métricas, umbrales y acciones

Elena recibe un informe inesperado: el porcentaje de conversaciones que el chatbot transfiere a un operador pasó del 12% al 21%. No se cambió el prompt. El proveedor había actualizado el modelo dos semanas antes, y las respuestas a preguntas sobre nuevos productos son ahora más largas y menos precisas.

La sucesión temporal **no demuestra causalidad**. El problema también podría estar en la base documental, las preguntas de los clientes o las llamadas a herramientas. El equipo debe investigar antes de atribuir culpas.

### Diferentes tipos de deriva

**Deriva de modelo o servicio.** El proveedor sustituye el modelo, modifica el enrutamiento o cambia las instrucciones del sistema. Un alias puede apuntar a otra versión.

**Deriva de datos.** Cambian las consultas de los usuarios, productos, idiomas o periodos del año. Un conjunto de prueba anterior puede dejar de representar la situación.

**Deriva de conectores y fuentes.** Se actualiza la base de conocimiento, una API devuelve información distinta o cambian permisos. El modelo puede ser igual y el resultado cambiar.

**Deriva de finalidad y cumplimiento.** Otro departamento utiliza el servicio para decisiones no aprobadas, cambian contratos o entran en aplicación nuevas normas.

Hay que determinar **qué cambió, cómo afecta al riesgo y qué control lo detectará**, sin llamar «deriva del modelo» a todos los problemas.

### Cuatro componentes del seguimiento continuo

1. **Baseline o referencia inicial.** Conjunto fijo y documentado de casos, respuestas esperadas y resultados evaluados. Debe incluir preguntas ambiguas y datos ausentes.
2. **Métricas.** Indicadores concretos con unidad, frecuencia, responsable y umbral.
3. **Triggers o disparadores.** Eventos que obligan a investigar, limitar, probar, detener o aprobar de nuevo.
4. **Responsabilidad.** Persona que mide, recibe el aviso, toma la decisión y autoriza reanudar.

Entre las métricas figuran la tasa de escalamiento humano, la precisión del conjunto de pruebas, respuestas sin fuente, errores de herramientas, acciones duplicadas, reclamaciones y fallos que afecten de manera desigual a grupos de personas. También deben definirse denominadores y criterios de muestreo, para no confundir un cambio de medida con un cambio del servicio.

### Un umbral debe producir una respuesta

Un equipo puede definir que una subida superior a su umbral durante dos evaluaciones consecutivas desencadene una investigación. Esa cifra es un ejemplo **contextual**, no un nivel universal de seguridad. Un incidente grave podría justificar STOP con una sola observación.

Un cambio de versión, términos contractuales, finalidad, población afectada o normativa debe generar una acción asociada. Las respuestas posibles son **suspender, reducir el alcance, repetir pruebas, revisar los riesgos o aprobar de nuevo**.

Elena exige que cada trigger incluya destinatario del aviso, plazo para actuar y evidencia necesaria para levantar la restricción. Una alerta sin responsable ni acción es solo una notificación.

### Si el daño ya ocurrió

El seguimiento no puede impedir todos los fallos. Es necesario registrar incidentes, identificar sistemas y personas afectadas, corregir el proceso y conservar el aprendizaje. Las normas de alto riesgo prevén obligaciones específicas cuando entren en aplicación; las obligaciones actuales de privacidad, seguridad o sectoriales siguen vigentes.

### Prueba de regresión

Elena prepara veinte consultas ficticias con respuestas de referencia. Tras la actualización del proveedor, vuelve a ejecutarlas y compara respuestas no sustentadas, escalamiento y exclusiones omitidas. Añade también casos de nuevos productos. Si el resultado se degrada, puede restringir temporalmente funciones y solicitar al propietario del sistema un plan de mejora.

**Microejercicio.** Define tres métricas con umbral y frecuencia y tres triggers con acción, responsable y condición de reactivación. Incluye un caso de prueba donde el sistema deba reconocer que le faltan datos.

**Reflexión.** Si el proveedor cambiara el modelo sin aviso, ¿qué verificación lo descubriría?

*[ ] He leído y comprendido esta sección*

## Lectura 6 · Laboratorio: auditoría exprés del ecosistema de IA

**Duración:** 60 minutos. **Modalidad:** individual o grupos de tres o cuatro. **Datos:** exclusivamente ficticios; no cargar contratos reales, expedientes de personal, información de clientes ni credenciales.

Elena construye un registro de gobernanza para una empresa inventada de servicios. El laboratorio relaciona el inventario, el análisis normativo y la vigilancia posterior. La finalidad es producir una decisión explicable, no solamente completar casillas.

### Fase 1 · Caza de IA oculta (15 minutos)

Analiza estos ocho servicios. Identifica si contienen funciones de IA, qué clases de datos pueden tratar, si podrían enviar información a modelos externos y quién debería ser el *System Owner*.

| # | Herramienta | Nota del inventario |
| --- | --- | --- |
| 1 | Gestión de RR. HH. | «Recomendaciones de candidatos» activadas tras la última actualización |
| 2 | CRM comercial | Puntuación de prioridad de clientes y resúmenes de correos |
| 3 | Suite de correo y calendario | Asistente de escritura incluido en la licencia |
| 4 | Helpdesk | Chatbot público conectado a una base de conocimiento |
| 5 | Transcripción de reuniones | Graba, transcribe y resume |
| 6 | Hoja de cálculo compartida | Consultas y análisis en lenguaje natural |
| 7 | Contabilidad | Clasificación automática de facturas |
| 8 | Plataforma de productividad | Asistente de tareas y notas que puede activar cada usuario |

**Clave didáctica.** Según las descripciones, los ocho contienen capacidades de IA. No significa que todas estén activas, que todos los proveedores traten datos fuera de la organización o que tengan el mismo riesgo. RR. HH. y CRM pueden afectar a personas; el chatbot interactúa con terceros; las reuniones incluyen conversaciones; una hoja de cálculo puede contener información reservada.

**Producto de la fase:** ocho filas del registro, cada una con finalidad aprobada y dudas pendientes.

### Fase 2 · Semáforo del AI Act y posible cambio de rol (20 minutos)

Considera cuatro situaciones ficticias. Para cada una indica categoría potencial, obligaciones ya relevantes, circunstancias que exigen estudiar el artículo 25 y primera acción.

**A — Ranking automático de CV.** La selección de personal es un ámbito del anexo III. No debería mantenerse un ranking no evaluado; se necesita un examen jurídico y de protección de datos, además de valorar posibles consecuencias sobre el rol de proveedor.

**B — Chatbot externo de soporte.** Comprobar transparencia del artículo 50 en los supuestos aplicables, tratamiento de datos, límites de la respuesta y paso a un empleado. Determinar si toma decisiones de impacto.

**C — Resúmenes internos de reuniones.** Verificar información a participantes, grabaciones, acceso, retención y posibles usos no autorizados para evaluar personas. Resumir una conversación no es lo mismo que perfilar empleados.

**D — Evaluación de fiabilidad financiera.** Aclarar si se trata de personas físicas, autónomos o sociedades y qué decisiones se producen. No basta suponer que todo análisis financiero es alto riesgo.

**Corrección responsable.** Si dos revisores competentes discrepan, registran la duda y la elevan. La tabla es una orientación educativa, no un dictamen aplicable a una empresa identificada.

### Fase 3 · Plan antideriva y condiciones de bloqueo (25 minutos)

Elige el sistema ficticio más delicado y completa **tres métricas** con definición, umbral, frecuencia y responsable de medición. Añade **tres eventos trigger** con acción inmediata, autoridad para decidir y evidencia necesaria para reactivar.

Documenta también una **baseline**: casos de prueba, criterios de corrección, evaluador y periodicidad. Por último, determina qué evidencias guardar: comunicaciones del proveedor, resultados, aprobaciones, incidencias y logs mínimos pertinentes.

Ejemplo: el propietario del chatbot mide escalamiento, respuestas sin fundamento y errores de herramientas. Una actualización del modelo provoca repetir la batería de pruebas. Una filtración grave de información exige aplicar el plan de incidentes y, en su caso, suspender el servicio.

### Rúbrica y condición STOP

Evalúa cinco criterios de 0 a 2: **(A)** inventario completo y propietario; **(B)** clasificación de finalidad, rol y dudas; **(C)** baseline y métricas; **(D)** triggers, acciones y condiciones de reactivación; **(E)** evidencias verificables.

**STOP independientemente del resultado** si un sistema de producción carece de responsable, se utiliza una finalidad potencialmente prohibida o de alto riesgo sin la evaluación exigible, o nadie dispone de una manera efectiva de suspenderlo. En el laboratorio STOP es una decisión del diseño simulado, no una declaración jurídica sobre un sistema real.

**Pregunta final.** ¿Podrías mostrar ante una auditoría qué sistemas de IA existen, por qué se utilizan, quién responde de ellos y qué obligaría a detenerlos?

*[ ] He leído y comprendido esta sección*

---

## Herramientas operativas

### 1. Registro vivo de IA — una fila por sistema

| Campo | Contenido o evidencia |
| --- | --- |
| ID y nombre | Identificador único |
| Proveedor, producto, plan y versión | Cuando se conoce; en otro caso, método para detectar cambios |
| Familia | Interno / producto AI / IA integrada en SaaS |
| Finalidad autorizada | Frase precisa; incluir usos prohibidos |
| Usuarios y proceso | Personas y departamentos afectados |
| Entradas y salidas | Categorías de datos, orígenes y transferencias |
| Rol de la organización | Deployer / proveedor / pendiente de análisis |
| Clasificación AI Act y argumento | Prohibido / alto riesgo / transparencia / otro / duda |
| Garantías contractuales | Entrenamiento, retención, subencargados, cambios |
| Supervisión humana | Persona, autoridad y punto de control |
| Propietario y sustituto | Roles y escalamiento |
| Métricas, baseline y triggers | Enlace al plan |
| Revisiones | Última, próxima y por eventos |
| Evidencias | Pruebas, logs, decisiones e incidencias |

### 2. Matriz RACI orientativa

**R = Responsable de ejecutar; A = responsable final; C = consultado; I = informado.** Asigna una responsabilidad final clara a cada decisión; adapta esta matriz a tu organización.

| Actividad | Negocio | System Owner | IT/Seguridad | DPO/Privacidad | Legal/Compliance |
| --- | --- | --- | --- | --- | --- |
| Inventariar nueva función | R | A | C | C | I |
| Aprobar finalidad | A | R | C | C | C |
| Clasificar legalmente | C | C | I | C | A/R |
| Medir resultados | I | A/R | R | I | I |
| Suspender servicio | A | R | R | I | I |
| Aprobar de nuevo | A | R | C | C | C |

### 3. Calendario y plan a 30, 60 y 90 días

**Por evento:** compra, función nueva, actualización del modelo, modificación contractual, incidente y nueva finalidad. **Trimestral:** indicadores y controles de sistemas importantes. **Semestral:** inventario y roles. **Anual:** políticas y alfabetización. Son frecuencias orientativas según contexto y riesgo.

**Primeros 30 días:** registrar herramientas y responsables, localizar IA integrada y detener usos claramente no evaluados. **Hasta 60 días:** analizar finalidades, contratos, datos y avisos; identificar responsables. **Hasta 90 días:** establecer pruebas de referencia, triggers y procedimientos de suspensión; revisar los resultados con los responsables.

### Glosario esencial

**Registro de IA:** inventario vivo con finalidades, riesgos, propietarios, controles y evidencias.  
**System Owner:** responsable de mantener y revisar un sistema.  
**Provider / proveedor:** figura jurídica según las condiciones del AI Act.  
**Deployer / responsable del despliegue:** quien usa profesionalmente un sistema bajo su autoridad.  
**Finalidad prevista:** uso autorizado que puede requerir una nueva evaluación si cambia.  
**Alto riesgo:** categoría determinada por artículos y hechos concretos, no por la etiqueta comercial.  
**Modificación sustancial:** cambio relevante conforme a los criterios normativos aplicables.  
**AIMS:** sistema de gestión de IA, relacionado con ISO/IEC 42001.  
**QMS:** sistema de gestión de calidad, artículo 17 y EN 18286 en sus respectivos ámbitos.  
**Norma armonizada:** norma europea citada por la Comisión con un alcance de presunción de conformidad definido.  
**Deriva del modelo:** cambio de comportamiento o rendimiento.  
**Deriva de datos:** modificación de la distribución de entradas.  
**Deriva de finalidad:** uso real distinto del autorizado.  
**Trigger:** acontecimiento que obliga a una revisión o acción definida.  
**Baseline:** conjunto inicial de pruebas y resultados evaluados.  
**RACI:** matriz de responsabilidades, rendición de cuentas, consultas e información.

### Fuentes primarias y materiales complementarios

- EU AI Act, Reglamento (UE) 2024/1689: https://eur-lex.europa.eu/eli/reg/2024/1689
- Reglamento (UE) 2026/1744, Digital Omnibus on AI: https://eur-lex.europa.eu/eli/reg/2026/1744/oj
- Comisión Europea, guía y calendario: https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act
- Comisión Europea, EN 18286:2026: https://digital-strategy.ec.europa.eu/en/library/first-harmonised-standard-supporting-ai-act-published-official-journal
- ISO/IEC 42001:2023: https://www.iso.org/standard/42001
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
- Ley italiana 132/2025: https://www.normattiva.it/eli/stato/LEGGE/2025/09/23/132

*Revisión editorial: noviembre de 2026. Ejemplos ficticios. Las puntuaciones del curso no constituyen auditoría, certificación, dictamen jurídico ni autorización para utilizar sistemas con datos reales.*