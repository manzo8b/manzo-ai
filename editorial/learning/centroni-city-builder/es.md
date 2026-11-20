# AI Product Builder — Construir Centroni City

*De una comunidad de Facebook a un producto de información vecinal útil, comprobable y sostenible: un curso de aprendizaje por proyectos de MANZO AI.*

**Destinatarios:** estudiantes, profesionales, autónomos, asociaciones, responsables de comunidades y ciudadanía interesada en crear servicios digitales.

**Objetivo de aprendizaje:** convertir una necesidad real de información en un blueprint, diseñar recorridos de usuario, distinguir información pública de canales oficiales, construir un prototipo de bajo presupuesto, probar fallos críticos y medir el valor cívico.

**Un proyecto en seis lecturas:** construir **Centroni City**, una demostración educativa e independiente de guía vecinal del barrio de Centroni en Roma. **No es** una sede municipal, canal oficial de denuncias, sistema de emergencias, plataforma de reclamaciones ni servicio operativo de gestión de expedientes.

**Método:** problema → personas → Entrada/Proceso/Salida → prototipo → calidad → valor medible. La lógica se define antes del prompt.

---

## Lectura 1 · De la conversación digital al problema real

Son las 8:10 de un martes. Marta espera el autobús después de acompañar a su hijo al colegio. Abre Facebook y encuentra una publicación: alguien pregunta por qué una calle está cortada. Un vecino habla de obras, otro cree que hubo un accidente y una tercera persona muestra una fotografía antigua. Marta solo quiere saber si mañana podrá pasar por esa zona.

Más tarde otro residente busca el contacto apropiado para avisar sobre una farola averiada. En otra publicación preguntan dónde encontrar información de un servicio municipal. La comunidad sirve para compartir experiencias, preguntas y ayuda entre personas reales. Sin embargo, la información está dispersa, cambia rápidamente y no siempre queda claro qué datos se han comprobado.

**Centroni City surge de esta necesidad**, no de la pregunta «¿Qué aplicación interesante podríamos generar?». La pregunta productiva es: «¿Qué problema del ciudadano sigue sin resolverse, aunque la comunidad en Facebook sea muy activa?».

### Facebook es un canal; el producto es un sistema

Una publicación de Facebook está diseñada para provocar conversación y reacciones. Un servicio útil debe facilitar otro recorrido: **encontrar la información, entender su procedencia, saber cuándo se actualizó y descubrir el siguiente paso apropiado**.

No es buena idea copiar automáticamente todas las publicaciones a una web nueva. Compartir fotografías y textos de una red social plantea cuestiones de derechos, consentimiento, privacidad, moderación y veracidad. Que una publicación sea visible al público no significa que cualquiera tenga permiso para reutilizarla.

En cambio, Centroni City podría preparar **fichas editoriales originales** fundamentadas en fuentes oficiales, con fecha, estado y contexto. Facebook puede seguir siendo un canal de intercambio y difusión cuando exista autorización para relacionarlo con el nuevo producto.

### Identificar el cuello de botella

Antes de abrir un generador de aplicaciones, anotamos tres necesidades:

1. **Informarse:** «¿Está confirmado que esta calle cerrará y cuál es la fecha de la última revisión de la noticia?».
2. **Orientarse:** «¿Qué canal oficial debo consultar para una farola que no funciona?».
3. **Evitar información engañosa:** «¿Cómo puedo distinguir un aviso vigente de un comentario o una noticia antigua?».

Una declaración de problema debe identificar persona, objetivo, dificultad actual y manera de observar una mejora. «Crear una plataforma vecinal moderna» es demasiado general.

Una descripción más verificable sería: «Algunos vecinos necesitan recorrer varias páginas o hilos confusos para encontrar el canal oficial de un problema urbano. La demo debe facilitar esa búsqueda sin hacer creer que presenta la reclamación en nombre del ciudadano».

### Scaffolding: construir criterio propio

La idea de *scaffolding*, o andamiaje educativo, consiste en ofrecer apoyos temporales para que el estudiante pueda realizar tareas que aún no domina plenamente. La investigación clásica de Wood, Bruner y Ross sobre tutoría sirve como referencia.

En este proyecto no se trata de observar cómo una IA diseña todo. Primero escribimos problema, supuestos, público, condiciones y criterios de éxito. Después podemos pedir a un modelo que señale lagunas, proponga pruebas o critique la idea.

La prueba de aprendizaje es que una persona sepa explicar el producto **sin depender del asistente**. «Lo elegí porque la IA me lo sugirió» todavía no es una justificación funcional suficiente.

### Formular un resultado observable

Para el ejemplo de la farola, un indicador temprano puede ser qué proporción de usuarios de prueba consigue llegar a **la información o canal oficial adecuado** sin ayuda, y si comprende la procedencia del enlace.

Esto no demuestra que el organismo público haya recibido ni solucionado una incidencia. La diferencia entre **encontrar el canal** y **presentar formalmente una comunicación** debe quedar clara desde el primer diseño.

**Producto de la lectura:** ficha de problema con tres necesidades prioritarias, destinatarios, obstáculos, límites y un objetivo verificable.

**Reflexión:** si mañana desapareciera Facebook, ¿qué información seguirían necesitando encontrar y contrastar los vecinos?

## Lectura 2 · Primero las personas, después las funciones

Algunos diseñadores empiezan por una pantalla con muchos botones: noticias, mapa, reclamaciones, eventos, chat, ofertas, avisos, anuncios. Sin embargo, añadir funciones no garantiza que una persona complete la tarea que necesita.

Para Centroni City es mejor empezar por **los recorridos reales de uso**, no por una colección de tecnologías disponibles.

### Tres personas ficticias

**Marta** es una madre adulta con poco tiempo entre las actividades escolares y el trabajo. Necesita saber rápidamente si una noticia afecta su trayecto.

**Karim** trabaja con horarios variables y quiere localizar el canal correcto para avisar de una avería urbana sin tener que aprender terminología administrativa.

**Lucía** es una vecina jubilada que prefiere textos legibles, instrucciones claras y páginas accesibles aunque no conozca los nombres de los departamentos municipales.

Son **personas educativas provisionales** y no perfiles estadísticos de los habitantes del barrio. Deben validarse mediante conversaciones, entrevistas y observación con grupos diversos, incluidas personas con necesidades de accesibilidad.

Las guías oficiales de **Designers Italia** recomiendan comprender las necesidades y el contexto de uso antes de diseñar una interfaz. Las personas no son estereotipos, sino hipótesis que ayudan a preparar investigación y escenarios concretos.

### El recorrido de Karim

Situación inicial: Karim vuelve de noche y ve que una farola está apagada. Su objetivo no es enviar un mensaje a cualquier web; necesita averiguar **a qué organismo corresponde el problema**.

Los obstáculos son términos administrativos desconocidos, enlaces ambiguos y páginas que no explican si el mensaje será enviado realmente.

Un recorrido claro puede tener estas etapas:

**Descripción de una necesidad → explicación sencilla → referencia verificada a un servicio oficial → siguiente paso → aviso de que Centroni City no ha presentado la comunicación.**

Cada transición debe poder comprobarse. Un gran mapa interactivo no sirve de mucho si falta una dirección útil. Un botón «Enviar incidencia» puede resultar peligroso si lleva a una demostración que no tiene capacidad para registrar nada.

### Tres áreas para la primera versión

**Información del barrio.** Noticias breves con procedencia, fecha, estado editorial y actualización. Las publicaciones de la comunidad no se convierten automáticamente en hechos confirmados.

**Orientación hacia servicios.** Guías para encontrar portales y canales oficiales adecuados a preguntas frecuentes. Deben revisarse y mantenerse.

**Guía de comunicaciones cívicas.** Explicaciones claras de qué es una incidencia urbana, qué es una reclamación de servicio, qué puede constituir una denuncia formal y cuándo se debe acudir a emergencias.

Las tres áreas proporcionan una base útil sin necesitar bases de datos de ciudadanos ni agentes autónomos.

### Accesibilidad desde el principio

Una interfaz *mobile-first* necesita una jerarquía de títulos coherente, buen contraste, tipografía legible, objetivos táctiles cómodos, navegación por teclado, foco visible y lenguaje claro.

También deben contemplarse conexiones limitadas, teléfonos antiguos y tecnologías de asistencia. Una página con animaciones espectaculares puede ser menos útil que otra sencilla si sus botones resultan difíciles de encontrar.

Centroni City es un proyecto independiente; no debe atribuirse automáticamente el mismo régimen jurídico que a una administración pública. Pero **las prácticas de accesibilidad** siguen siendo fundamentales para el servicio.

**Producto de la lectura:** tres personas hipotéticas, tres recorridos de usuario, una checklist de accesibilidad y prioridades funcionales.

**Reflexión:** ¿estás diseñando un catálogo de botones o un recorrido que permita a una persona resolver una necesidad?

## Lectura 3 · Del proyecto al blueprint: entrada, proceso y salida

Llegamos a la arquitectura inicial. Antes de pedir a la IA que escriba código debemos definir qué debe ocurrir con la información y con las decisiones humanas.

El método **Entrada → Proceso → Salida (E-P-S / IPO)** ayuda a identificar las reglas de un servicio sin necesidad de saber programar.

### Informarse: primer flujo

**Entrada:** propuesta de aviso o noticia, con origen, fecha y ámbito geográfico.

**Proceso:** comprobación editorial, revisión de la fuente, validación de vigencia, clasificación, edición en lenguaje claro y aprobación.

**Salida:** una ficha pública con título, contenido, procedencia, fecha de revisión y estado.

**Condición STOP:** si la afirmación no dispone de respaldo suficientemente fiable o puede perjudicar a una persona identificable, no se publica como información confirmada.

### Orientarse: segundo flujo

**Entrada:** una necesidad vecinal, por ejemplo «Quiero informar de una farola averiada».

**Proceso:** identificar la categoría de necesidad, consultar una lista mantenida de canales oficiales, comprobar el enlace y explicar límites.

**Salida:** referencia o instrucciones hacia **el servicio público competente**, sin afirmar que la reclamación está presentada o aceptada.

Cuando una fuente ha caducado o el enlace ha dejado de funcionar, es preferible mostrar «Pendiente de revisión» que inventar un nuevo destino.

### Incidencia cívica, reclamación, denuncia y emergencia

Estas palabras no son sinónimos.

Una **comunicación o incidencia cívica** puede describir una avería o problema urbano. Una **reclamación** puede cuestionar la prestación de un servicio con procedimientos propios. Una **denuncia formal de posibles hechos delictivos** corresponde a las autoridades competentes. Una **emergencia** requiere canales inmediatos de asistencia y seguridad.

Roma Capitale dispone de vías oficiales para sugerencias, comunicaciones y reclamaciones, y del servicio **ChiamaRoma 060606**. Centroni City puede explicar cómo localizar esas vías, pero no debe presentarse como ventanilla pública que recibe o registra expedientes.

El árbol de orientación empieza con una pregunta prioritaria:

1. **¿Existe peligro inmediato para alguien?** No se utiliza la demo como canal de emergencia; hay que acudir a los servicios competentes.
2. **¿Se describe un posible delito o se acusa a una persona identificable?** No se recogen acusaciones ni documentos personales. Se explican los canales oficiales pertinentes.
3. **¿Se trata de mantenimiento urbano o reclamación de servicio?** Se ofrece una referencia verificada al canal correspondiente, sin prometer entrega ni seguimiento.
4. **¿Es una consulta informativa?** Se publica únicamente una ficha editorial con fuente, estado y fecha.

Este árbol es una herramienta educativa de orientación, **no asesoramiento jurídico ni sustituto del procedimiento formal**. Las referencias oficiales deben comprobarse periódicamente.

### El blueprint de ocho campos

| Campo | Ejemplo didáctico |
| --- | --- |
| **Proyecto** | Demostración independiente de Centroni City |
| **Problema** | Dificultad para encontrar información vecinal verificada |
| **Destinatarios** | Personas con distintas necesidades y competencias digitales |
| **Entrada** | Avisos, enlaces oficiales y preguntas frecuentes |
| **Proceso** | Control de procedencia, fecha, clasificación y aprobación humana |
| **Salida** | Fichas verificadas y orientación a canales oficiales |
| **Límites** | Sin denuncias, datos de usuarios ni representación institucional |
| **Medición** | Completar el recorrido hasta información pública apropiada |

Un buen blueprint describe no solo lo que hará el producto, sino **qué hará cuando no tenga evidencia suficiente**.

### La IA como contraparte crítica

Solo después de escribir los ocho campos utilizamos un asistente con una tarea concreta:

«Revisa este diseño como arquitecto de producto exigente. No generes código. Identifica afirmaciones engañosas, riesgos de privacidad, lenguaje confuso, promesas que no podemos cumplir y pruebas omitidas. Haz preguntas antes de proponer cambios».

El asistente puede encontrar problemas, pero el diseñador debe justificar por qué acepta o rechaza cada sugerencia. No todas las propuestas plausibles son correctas.

**Producto de la lectura:** blueprint de ocho campos, reglas STOP y procedimiento de verificación editorial.

**Reflexión:** si el código de la aplicación funcionara perfectamente pero mostrara información falsa, ¿habríamos construido un producto útil?

## Lectura 4 · Prototipar con método y presupuesto cero

Después de preparar el blueprint, Marta abre la demostración. La pantalla principal muestra tres opciones: **Información**, **Servicios**, **Orientación para incidencias**. Hay una noticia sintética revisada, un enlace a un recurso oficial y una guía que explica a qué organismo corresponde acudir.

El sitio funciona en el teléfono y no solicita nombre, dirección, número de teléfono ni documentación personal.

Estamos ante **un prototipo educativo**, no ante un servicio cívico operativo. Su buen aspecto no garantiza que los contenidos estén actualizados, que exista un equipo editorial o que las autoridades reciban ninguna solicitud.

### Producto mínimo útil, no acumulación de funciones

La V1 puede construirse con páginas estáticas de **HTML, CSS y JavaScript** publicadas en un servicio de alojamiento gratuito que permita ese uso, como GitHub Pages.

Esta arquitectura permite mostrar fichas, categorías, filtros y enlaces, pero sin un backend real no debe prometer cuentas, almacenamiento de incidencias, notificaciones, seguimiento o toma en carga de reclamaciones.

Una plataforma operativa más compleja requeriría autenticación, bases de datos, seguridad, moderación, gestión de incidentes, reglas de conservación y recursos continuados. **Que una demo cueste cero no significa que un servicio ciudadano completo pueda mantenerse sin presupuesto**.

### Una cadena editorial imprescindible

Cada contenido debe recorrer:

**Propuesta o fuente → comprobación de origen → revisión de fecha y contexto → redacción clara → aprobación humana → publicación → revisión o retirada.**

La información sin fecha y procedencia se interpreta con facilidad como confirmada y vigente. Las fichas deben poder archivarse cuando la situación cambie. Debe existir una persona responsable de corregir contenidos.

La IA puede ayudar a preparar títulos, resúmenes neutrales, variantes de textos o componentes visuales. No debe transformar rumores en avisos oficiales ni inventar competencias administrativas.

### Lo que la IA sí puede aportar al desarrollo

Un asistente puede explicar conceptos de programación, generar variantes de interfaz, proponer estructura HTML y CSS, buscar errores de código y formular casos de prueba.

Los entornos *no-code*, *low-code* y *vibe coding* pueden reducir la barrera de la sintaxis. Pero no eliminan la necesidad de comprender lógica, accesibilidad, privacidad, requisitos y riesgos del producto.

El ciclo de aprendizaje es **definir → construir un incremento pequeño → probar → observar → corregir**. Se aprende creando un único artefacto progresivo, no completando ejercicios inconexos.

### Un primer prototipo alcanzable

Comienza por una portada clara, tres áreas, varias tarjetas de información ficticia y una declaración de independencia. Añade una fecha de revisión editorial y enlaces a fuentes públicas verificadas. Prepara una checklist de calidad y úsala para probar cada nueva función.

Pide a personas de prueba que intenten completar una tarea sin la explicación del diseñador. No añadas un chatbot solo porque una herramienta pueda generarlo.

Un tutor socrático debe preguntar «¿Qué regla decidiste?» y «¿Qué resultado esperarías si el dato estuviera ausente?» antes de producir código. La meta es desarrollar **comprensión y capacidad de validación**.

**Producto de la lectura:** demo V1 *mobile-first* con tres funciones educativas, fuentes identificables y aviso de independencia.

**Reflexión:** ¿qué necesita ver una persona en los primeros segundos para orientarse y qué funciones pueden esperar?

## Lectura 5 · Calidad, responsabilidad y seguridad del contenido cívico

Una demostración visualmente excelente puede perjudicar a sus usuarios si presenta una fecha falsa, una fotografía invasiva o un botón de «Enviar denuncia» que realmente no produce ningún efecto institucional.

La pregunta de esta etapa es: **¿Qué fallos jamás debemos ocultar detrás de un diseño atractivo?**

### Cinco casos límite para comprobar la V1

**Caso A — Noticia sin fuente.** Llega un mensaje sobre el corte de una calle, pero no existe una referencia fiable. **Resultado esperado:** no identificarlo como confirmado, solicitar comprobación y no difundir información decisiva sin evidencia.

**Caso B — Aviso caducado.** Una tarjeta anuncia una cita cuya fecha ya pasó. **Resultado esperado:** mostrar estado «Caducado» o archivar la ficha, sin hacerla pasar por un evento futuro.

**Caso C — Acusación personal.** Un texto señala a un particular y le atribuye hechos ilícitos. **Resultado esperado:** no publicar acusaciones ni datos que permitan identificarle; remitir a los organismos competentes, sin presentar la demo como canal formal.

**Caso D — Emergencia.** Alguien describe un peligro inmediato. **Resultado esperado:** aclarar que Centroni City **no es un servicio de emergencias** y orientar hacia servicios oficiales sin recoger ni conservar la comunicación.

**Caso E — Enlace oficial roto.** El destino verificado hace meses ya no existe o ahora dirige a una página distinta. **Resultado esperado:** marcar el enlace para revisión y retirarlo si pudiera inducir a error.

Cada caso debe documentar entrada sintética, comportamiento esperado, resultado observado, gravedad, medida correctora y nueva prueba.

### La privacidad no es un detalle visual

El Garante italiano para la protección de datos personales recuerda principios como **minimización y limitación de la finalidad**. En la V1 educativa la mejor decisión es **no recopilar datos identificables** de personas que desean informar sobre algo.

Incluso un formulario sin backend puede confundir: la persona cree haber realizado una comunicación cuando nadie la recibió. Por tanto, conviene no incluirlo en el prototipo y explicar claramente los límites del servicio.

Una versión futura con datos reales necesitaría finalidad legítima, base jurídica, información transparente, medidas técnicas, retención limitada y revisión especializada. No deben incluirse acusaciones, documentos de identidad o datos sensibles en almacenamiento del navegador o repositorios públicos.

### Prueba de fiabilidad editorial

Una rúbrica simple puede evaluar cuatro aspectos con 0–2 puntos: **fuente comprobada**, **fecha coherente**, **lenguaje no engañoso**, **enlace oficial identificado y vigente**.

El total sirve para comentar el resultado, **no para anular condiciones STOP**. Una acusación personal, un aviso crítico sin fuente o una falsa promesa de denuncia formal siguen siendo inaceptables aunque las otras casillas puntúen bien.

### El diseño también comunica promesas

Un gran botón verde con la palabra «Enviado» podría sugerir que una autoridad ha registrado una comunicación. Si el sistema únicamente ha abierto un enlace, debe decir **«Enlace oficial abierto»** o **«Instrucciones mostradas»**, según lo que realmente haya ocurrido.

Si el producto llegara a aceptar contenido de usuarios, habría que incorporar moderación y recursos de gestión. La V1 educativa evita deliberadamente estas funciones.

**Producto de la lectura:** informe QA de cinco escenarios con gravedad, solución y reglas de bloqueo.

**Reflexión:** ¿qué contenido rechazarías publicar aunque pudiera provocar muchos clics y comentarios?

## Lectura 6 · Medir el valor y preparar una versión futura

Centroni City no debe crecer solamente porque es fácil crear funciones con IA. El producto debe demostrar que ayuda a resolver un problema concreto.

Marta comienza con una prueba simple: solicita a **cinco personas** que encuentren el canal oficial adecuado para un caso ficticio de farola averiada. Algunas utilizan los recorridos habituales de información y otras el prototipo. Se observan tiempos, dificultades y pasos, sin recopilar datos privados.

No se trata de una muestra representativa de Centroni. Es una **prueba exploratoria de usabilidad**, útil para descubrir errores y formular hipótesis para investigaciones posteriores.

La mejora más importante podría ser modificar el texto de un botón, no incorporar otra tecnología.

### Retorno cívico más allá del dinero

En una empresa puede calcularse un ROI hipotético mediante costes y tiempo ahorrado. En un servicio vecinal independiente es útil considerar también:

- **Tiempo mediano** para llegar a la fuente oficial correcta.
- **Porcentaje de tareas completadas sin ayuda**, con una definición clara del objetivo.
- **Proporción de fichas con fuente, fecha y revisión editorial**.
- **Errores graves** de desinformación o de redirección detectados.
- **Accesibilidad** de los recorridos principales en móvil, teclado y tecnologías asistivas.
- **Tiempo y recursos de mantenimiento** para conservar datos y enlaces correctos.

«La persona hizo clic en el botón» no equivale a «La administración recibió una solicitud». La prueba debe medir el resultado que el software realmente puede ofrecer.

### ¿Quién mantiene el producto?

Un servicio de información necesita responsabilidades: quién revisa anuncios municipales, comprueba enlaces, recibe comentarios de mejora, corrige errores y decide cuándo archivar contenido.

El responsable editorial debe estar identificado incluso si el sitio es gratuito. Una web abandonada puede volverse engañosa si mantiene expresiones como «actualizado» sin realizar comprobaciones.

Roma Capitale reconoce a los comités vecinales como espacios de participación. Podrían consultarse para comprender necesidades, pero **Centroni City no representa automáticamente a un comité ni al Municipio VII**.

### Presentación final en tres minutos

El mini-pitch debe explicar:

1. **Problema:** a qué persona ayudamos y qué dificultad intentamos reducir.
2. **Solución:** qué hace la V1, qué no hace y por qué.
3. **Evidencias:** blueprint, resultados exploratorios, cinco pruebas QA y fuentes.
4. **Límites:** proyecto independiente, sin recopilación de denuncias, datos personales ni emergencias.
5. **Decisión siguiente:** continuar, corregir un paso, reducir el alcance o detener una función engañosa.

Un producto profesional no oculta sus limitaciones. Debe conseguir que los interesados entiendan qué pueden esperar con fundamento y qué sigue siendo solo una hipótesis.

### Glosario esencial

**Artefacto:** resultado tangible, como un blueprint o un prototipo.  
**Blueprint:** descripción del flujo de entradas, reglas, salidas y bloqueos.  
**Orientación cívica:** ayuda para localizar canales competentes, no gestión formal de comunicaciones.  
**Reclamación:** manifestación sobre la prestación de un servicio según el procedimiento aplicable.  
**Denuncia formal:** comunicación de hechos a las autoridades competentes, no formulario privado de prueba.  
**Emergencia:** peligro inmediato que requiere los canales oficiales de asistencia.  
**Scaffolding:** apoyo didáctico temporal que facilita la resolución independiente de problemas.  
**IPO/EPS:** Entrada–Proceso–Salida, mapa lógico previo a programar.  
**Persona:** hipótesis provisional sobre necesidades que requiere investigación real.  
**User journey:** recorrido de decisiones y pasos para completar un objetivo.  
**Caso límite:** situación no habitual que pone a prueba la fiabilidad.  
**Verificación editorial:** comprobación de origen, contexto, fecha y efectos de publicar.  
**Workflow:** secuencia organizada de tareas, responsables y controles.  
**Retorno cívico:** valor medible en claridad, acceso, utilidad y sostenibilidad del servicio.

### Fuentes técnicas, educativas e institucionales

- Roma Capitale, *Barrios del Municipio VII*: https://www.comune.roma.it/web/it/i-quartieri-di-roma-mun7.page
- Roma Capitale, *Comités de barrio*: https://www.comune.roma.it/web/it/attivita-progetto.page?contentId=PRG1506858
- Roma Capitale, *Sugerencias, avisos y reclamaciones*: https://www.comune.roma.it/web/it/suggerimenti-segnalazioni-e-reclami-urp-uffici-relazioni-con-il-pubblico.page
- Designers Italia, *Comprender*: https://designers.italia.it/risorse-per-progettare/comprendere/
- Designers Italia, *Definir personas*: https://designers.italia.it/risorse-per-progettare/comprendere/esperienza-utente/definisci-le-personas/
- Designers Italia, *Contenidos y lenguaje*: https://designers.italia.it/risorse-per-progettare/progettare/contenuti-e-linguaggio/
- Designers Italia, *Accesibilidad*: https://designers.italia.it/normativa/linee-guida-di-design/requisito-4-1/
- Garante italiano para la protección de datos personales, decisión del 26 de septiembre de 2024: https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10071261
- Wood, Bruner y Ross, *The Role of Tutoring in Problem Solving*, 1976: https://pubmed.ncbi.nlm.nih.gov/932126/

**Nota editorial:** las personas, noticias, ejemplos y escenarios son ficticios. El curso no equivale a asesoramiento jurídico, ventanilla administrativa ni demostración de que se haya presentado una denuncia. Los contenidos dirigidos a residentes reales requieren fuentes contrastadas y responsables de mantenimiento.

---

## Herramientas operativas

**Ficha del problema:** persona, necesidad, obstáculo, fuente relevante, riesgos de información incorrecta, objetivo verificable y funciones excluidas.

**Blueprint de ocho campos:** proyecto, problema, destinatarios, entrada, proceso, salida, límites y medición. Incluir condiciones **STOP** para informaciones sin fuente, acusaciones personales, falsas promesas de presentación oficial y errores sobre emergencias.

**Informe QA de cinco casos:** caso A–E, entrada, comportamiento esperado, resultado observado, gravedad, corrección, responsable y fecha de nueva prueba.

**Condición para una V1 educativa:** mostrar información y orientación mediante datos ficticios. No guardar comunicaciones de residentes, no suplantar una autoridad ni mostrar asuntos como formalmente presentados.

**Transferencia de aprendizaje:** aplicar la misma arquitectura EPS a otra situación vecinal ficticia y explicar el proceso sin asistencia de un modelo.
