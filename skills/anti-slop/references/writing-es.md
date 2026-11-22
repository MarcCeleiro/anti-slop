# Writing anti-patterns: Spanish

Load with `writing.md` when the text is in Spanish. The general rules (W-xx) still apply. This file adds Spanish examples for the most frequent ones and the patterns specific to Spanish (ES-xx).

Public lists of AI-writing tells exist mostly for English. The Spanish entries come from observed corrections and from standard usage references (RAE, Fundéu, the Diccionario panhispánico de dudas). Treat them as review prompts, not as proof.

## Frequent general patterns, with Spanish examples

| ID | Bad | Good |
|---|---|---|
| W-01 comma splice | «Ya enviamos las facturas por correo, nos gustaría añadir un enlace de pago.» | «Ya enviamos las facturas por correo y ahora querríamos añadir un enlace de pago.» |
| W-02 fragment | «Fines de semana, cerrado.» | «La oficina cierra los fines de semana.» |
| W-03 choppy chain | «La biblioteca abre a las nueve. Los sábados no. La cafetería sí.» | «La biblioteca abre a las nueve entre semana y cierra los sábados, pero la cafetería abre todos los días.» |
| W-10 semicolon | «Los lunes, planificación; los viernes, revisión.» | «Planificamos los lunes y revisamos los viernes.» |
| W-12 colon hinge | «Preparamos cada menú por encargo: no tenemos carta fija.» | «Como no tenemos carta fija, preparamos cada menú por encargo.» |
| W-13 negative parallelism | «No es solo una app, sino una nueva forma de cuidar tu huerto.» | «La app te avisa cuando tienes que regar cada planta.» |
| W-24 effect phrase | «Páginas realmente rápidas» · «un soplo de aire fresco» | «Páginas que cargan en menos de dos segundos» · say what changes |
| W-27 text about the text | «Dos métodos y un ejemplo, uno al lado del otro» · «sujetos a validación» | «Métodos» · remove the internal note |
| W-30 comma-tag heading | «El proyecto, fase a fase» · «Dos oficinas, un equipo» | «Fases del proyecto» · «Equipo» |
| W-31 slogan heading | «Todo lo que necesitas ya está aquí» · «Qué gana tu equipo con la nueva herramienta» | «Estado del proyecto» · «Beneficios» |
| W-40 calque | «Esto hace sentido» | «Esto tiene sentido» |

## Spanish-specific patterns

### ES-01 · Inflated vocabulary · medium

- What: «potenciar», «impulsar», «apostar por», «poner en valor», «sin fisuras», «fundamental», «crucial», «clave» as an adjective, «robusto», «integral», «holístico», «sinergia», «ecosistema», «transformador», «revolucionario», «innovador», «de vanguardia», «de primer nivel», «llevar al siguiente nivel», «experiencia inmersiva», «en la era digital», «en el panorama actual», «sumergirse», «adentrarse», «profundizar en», «un viaje» (figurative), «entramado», «testimonio de», «desempeñar un papel crucial», «cabe destacar», «sin lugar a dudas», «cautivador».
- Why: vague praise with no fact behind it.
- Bad → good: «Potenciamos tu presencia digital con soluciones innovadoras y sin fisuras.» → «Hacemos webs que cargan en menos de dos segundos y que tu equipo puede actualizar.»
- Detect: list in `detect.py` (`ES-01`).
- Exceptions: technical uses.

### ES-02 · Calques from English · high

- What:
  - «a nivel de» when no levels exist → «en cuanto a», «en», «respecto a».
  - «en base a» → «según», «a partir de», «con base en».
  - «jugar un rol / un papel» → «desempeñar un papel», «tener un papel».
  - «hacer sentido» → «tener sentido».
  - «asumir» meaning "suppose" → «suponer».
  - «aplicar a un puesto» → «solicitar», «presentarse a».
  - «eventualmente» meaning "finally" → «finalmente».
  - «remover» meaning "remove" → «quitar», «eliminar».
  - «en su lugar» / «en lugar» tacked on at the end, from "instead" → rewrite the sentence.
  - «Espero que este correo te encuentre bien» (from "I hope this email finds you well").
  - Periphrastic passive for actions («El formulario fue enviado por el usuario») → «El usuario envió el formulario», «Se ha enviado el formulario».
- Why: they read as machine translation.
- Detect: list in `detect.py` (`ES-02`).
- Exceptions: «a nivel del mar», levels of administration.

### ES-03 · Gerund of posteriority · medium

- What: a gerund for an action after the main verb («Se fundó en 2010, convirtiéndose en la primera…»).
- Why: the RAE considers it incorrect, and it often comes from English participle tails (W-43).
- Bad → good: «…, convirtiéndose en la primera…» → «…y se convirtió en la primera…».
- Detect: comma plus a gerund with an enclitic pronoun at the end of a sentence (`-ándose`, `-iéndose`).
- Exceptions: gerunds of manner or simultaneity.

### ES-04 · Punctuation conventions · medium

- What:
  - Opening marks «¿» and «¡» are required. Their absence in finished text looks careless.
  - Quotation marks: the RAE recommends angled quotes « » first, then “ ”, then ‘ ’. Straight quotes in finished prose look unedited.
  - The raya is correct for asides and dialogue, but a dash in every paragraph is W-11.
  - In letters the salutation takes a colon («Estimada Ana:»), not a comma.
- Detect: questions without «¿» (`ES-04`), straight double quotes in prose.
- Exceptions: informal chat.

### ES-05 · Capitals · medium

- What: Title Case in titles, menus and buttons, and capitals on months, days and languages.
- Why: Spanish uses sentence case.
- Bad → good: «Política De Privacidad» → «Política de privacidad».
- Detect: `W-32` in `detect.py`.
- Exceptions: proper nouns and official names.

### ES-06 · Register · medium

- What: mixing «tú» and «usted» in the same product, or «vosotros» and «ustedes» inconsistently, or voseo and tuteo for the same market.
- Why: it breaks the voice.
- Detect: verb forms and pronouns of both registers in the same project.
- Exceptions: quotations.

### ES-07 · Formulas and fillers · medium

- What: «Espero que te encuentres bien», «No dudes en contactarnos», «Quedo a tu disposición para cualquier duda», «Quedamos atentos», «Esperamos que todo esté bien», «En resumen», «En definitiva», «Cabe destacar que», «Es importante tener en cuenta que», «Vamos a ver», «Veamos», «A continuación te explicamos», «¡Claro!», «¡Por supuesto!».
- Why: W-21 and W-26 in Spanish.
- Detect: list in `detect.py`.
- Exceptions: one expected closing in a formal letter.

### ES-08 · Bureaucratic verbs and anaphoric «el mismo» · low

- What: «realizar» (→ «hacer»), «efectuar», «proceder a», «llevar a cabo», «contar con» (→ «tener»), «disponer de»; «el mismo», «la misma» used as a pronoun («Rellene el formulario y envíe el mismo» → «envíelo»).
- Why: heavier and vaguer than the plain form. Fundéu advises against the anaphoric «el mismo».
- Detect: list in `detect.py` (`ES-08`).
- Exceptions: legal texts.

### ES-09 · Generic headings · medium

- What: «Cosas a tener en cuenta», «Aspectos clave», «Puntos clave», «Conclusiones finales», «Consideraciones adicionales», «Información importante».
- Why: W-34 in Spanish.
- Detect: list in `detect.py` (`W-34`).
- Exceptions: report templates.

### ES-10 · One-letter words at the end of a line · low

- What: «y», «o», «a», «e», «u» left at the end of a line in headings and printed documents.
- Why: careful typography keeps them with the next word. It is optional.
- Bad → good: a non-breaking space after the one-letter word.
- Detect: review rendered output.
- Exceptions: projects whose style guide does not use it.
