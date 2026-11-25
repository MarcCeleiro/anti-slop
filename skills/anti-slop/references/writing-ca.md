# Writing anti-patterns: Catalan

Load with `writing.md` when the text is in Catalan. The general rules (W-xx) still apply. This file adds Catalan examples for the most frequent ones and the patterns specific to Catalan (CA-xx).

Public lists of AI-writing tells exist mostly for English. The Catalan entries below come from observed corrections and from standard Catalan usage guides (IEC, Optimot, the ésAdir style guide). Treat them as review prompts, not as proof.

## Frequent general patterns, with Catalan examples

| ID | Bad | Good |
|---|---|---|
| W-01 comma splice | «Ja enviem les factures per correu, ens agradaria afegir-hi un enllaç de pagament.» | «Ja enviem les factures per correu i ara voldríem afegir-hi un enllaç de pagament.» |
| W-02 fragment | «Caps de setmana, tancat.» | «L'oficina tanca els caps de setmana.» |
| W-03 choppy chain | «La biblioteca obre a les nou. Els dissabtes no. El bar sí.» | «La biblioteca obre a les nou entre setmana i tanca els dissabtes, però el bar obre cada dia.» |
| W-05 compressed | «Devolucions 30 dies, 15 si rebaixat.» | «Pots tornar un article en 30 dies des de l'entrega. Els rebaixats tenen 15 dies.» |
| W-06 noun pile | «Incidències del mes i contactes de cada àrea» | «Consulta les incidències d'aquest mes» o «Cada àrea té els seus contactes» |
| W-10 semicolon | «La pujada va fallar dues vegades; el fitxer era massa gran.» | «La pujada va fallar dues vegades perquè el fitxer era massa gran.» |
| W-16 triad | «Idees. Ofici. Cura.» | Una frase que digui què fas: «Dissenyem etiquetes per a cellers petits.» |
| W-18 caveat tail | «Espera mitjana a cada centre. Estimada, no mesurada.» · «Preu de botiga, no de majorista.» | L'advertiment, un sol cop i on calgui: a la nota de mètode. |
| W-13 negative parallelism | «No és només una app, és una nova manera de cuidar l'hort.» | «L'app t'avisa quan has de regar cada planta.» |
| W-21 empty opener | «Espero que estiguis molt bé.» | Directament el que cal: «Ens pots enviar la factura de març?» |
| W-23 negation | «Les proves no es deixen per al final.» | «Provem cada pàgina tan bon punt està feta.» |
| W-24 unverifiable warmth | «…la nostra porta sempre és oberta.» | «…escriu-nos a hola@exemple.cat i et responem en un dia feiner.» |
| W-30 comma-tag heading | «El projecte, fase a fase» · «La carta, plat per plat» | «Fases del projecte» · «Carta» |
| W-30 count formula | «12 receptes, un ingredient cadascuna» · «40 cursos, cadascun amb el seu professor» | «Receptes» · «Cursos» |
| W-31 slogan heading | «Tot el que necessites ja és aquí» | «Estat del projecte» |
| W-31 role split | «Tu ho somies. Nosaltres ho fem.» | «Reformes de cuines i banys, amb pressupost tancat» (diu què s'ofereix) |
| W-32 title case | «Preguntes Freqüents» | «Preguntes freqüents» |
| W-33 numeral count | «2 coses a saber abans de la visita» | «El museu tanca abans els divendres» (diu quina és la cosa) |
| W-40 calque | «Això fa sentit» | «Això té sentit» |

## Catalan-specific patterns

### CA-01 · Inflated vocabulary · medium

- What: words that generated Catalan over-uses, often translated from the English list: «potenciar», «impulsar», «apostar per», «posar en valor», «sense fissures», «fonamental», «crucial», «clau» as an adjective («un aspecte clau»), «robust», «integral», «holístic», «sinergia», «ecosistema», «transformador», «revolucionari», «innovador», «d'avantguarda», «de primer nivell», «portar a un altre nivell», «experiència immersiva», «en l'era digital», «en el panorama actual», «endinsar-se», «teixit» (figurative), «un viatge» (figurative), «testimoni de», «tenir un paper clau».
- Why: vague praise with no fact behind it.
- Bad → good: «Potenciem la vostra presència digital amb solucions innovadores i sense fissures.» → «Fem webs que carreguen en menys de dos segons i que l'equip pot actualitzar sense ajuda.»
- Detect: list in `detect.py` (`CA-01`).
- Exceptions: technical uses («una estructura robusta» in engineering).

### CA-02 · Calques from English · high

- What: structures translated word by word.
  - «a nivell de» when no levels exist → «pel que fa a», «en», «quant a».
  - «en base a» → «a partir de», «segons», «d'acord amb».
  - «jugar un rol / un paper» → «tenir un paper», «fer un paper».
  - «fer sentit» → «tenir sentit».
  - «assumir» meaning "suppose" → «suposar».
  - «aplicar a una feina» → «presentar-se a», «optar a».
  - «eventualment» meaning "finally" → «finalment», «al final».
  - «remarcable» → «notable», «destacable».
  - «…en lloc» at the end of the sentence (from "instead") → «…en comptes de X» or rewrite: «Paga amb targeta en lloc» → «Paga amb targeta».
  - Passive with «ser» for actions («El formulari ha estat enviat per l'usuari») → pronominal or active («S'ha enviat el formulari», «Hem rebut el formulari»).
- Why: they read as machine translation.
- Detect: list in `detect.py` (`CA-02`).
- Exceptions: «a nivell del mar», «a nivell europeu» when it really means a level of administration.

### CA-03 · Calques from Spanish · medium

- What: «tenir que» → «haver de». «en quant a» → «quant a». «a l'igual que» → «igual que». «apart de» → «a part de». «al + infinitiu» temporal («Al arribar») → «en arribar». «lo + adjectiu» («lo important») → «el que és important», «allò important». «doncs» with causal meaning («No vinc, doncs estic malalt») → «ja que», «perquè». «degut a» → «a causa de» is preferred in careful writing. «el mateix» as an anaphoric pronoun («Ompliu el formulari i envieu el mateix») → a clitic («envieu-lo»).
- Why: they mark text as translated or careless, and some are normative errors.
- Detect: list in `detect.py` (`CA-03`).
- Exceptions: quotations.

### CA-04 · Gerund of posteriority · medium

- What: a gerund that expresses an action after the main verb («Es va inaugurar el 2024, convertint-se en el primer…»).
- Why: it is incorrect in Catalan and a common product of translated English participle tails (W-43).
- Bad → good: «…, convertint-se en el primer museu…» → «…i es va convertir en el primer museu…».
- Detect: comma plus a gerund with an enclitic pronoun at the end of a sentence (`-ant-se`, `-ent-se`, `-int-se`). Review other final gerunds.
- Exceptions: gerunds of manner or simultaneity («Va sortir corrent»).

### CA-05 · Punctuation conventions · medium

- What: English punctuation habits in Catalan text.
  - Quotation marks: avoid them (W-19). Name buttons, labels and titles without quotes. For a real quotation, straight quotes are enough.
  - No em dash in prose (W-11). Rewrite the aside with commas, a parenthesis or a new sentence.
  - No semicolons (W-10). Colons as hinges (W-12) are just as foreign in Catalan as in English.
  - In letters the salutation usually takes a comma («Benvolguda Anna,»).
  - Spaces: no space before «?», «!», «:», «;».
- Detect: « » and “ ” (`W-19`), em dashes (`W-11`), semicolons (`W-10`).
- Exceptions: code, URLs, data.

### CA-06 · Capitals · medium

- What: Title Case in titles, menus and buttons, and capitals on months, days of the week, languages and generic nouns.
- Why: Catalan uses sentence case. Only the first word and proper nouns take a capital.
- Bad → good: «Política De Privacitat» → «Política de privacitat». «Dilluns 3 De Novembre» → «Dilluns 3 de novembre».
- Detect: `W-32` in `detect.py` for headings.
- Exceptions: proper nouns and official names of institutions («Institut d'Estudis Catalans»).

### CA-07 · One-letter words at the end of a line · low

- What: «i», «o», «a», «e» left alone at the end of a line in headings, buttons and printed documents.
- Why: careful Catalan and Spanish typography keeps them with the next word. It is optional, but it shows care in titles and documents.
- Bad → good: insert a non-breaking space (U+00A0, `&nbsp;` in HTML) after the one-letter word.
- Detect: review rendered output. In HTML source, ` i `, ` o `, ` a `, ` e ` followed by a normal space can be flagged when a project adopts the rule.
- Exceptions: projects whose style guide does not use it.

### CA-08 · Inconsistent action labels · medium

- What: buttons and menus that mix the imperative («Desa», «Tanca»), the infinitive («Desar», «Tancar») and nouns («Desament»).
- Why: inconsistency looks careless. Pick one form for actions and use it across the product. Many Catalan products use the imperative, which reads as a direct instruction.
- Bad → good: «Desar», «Cancel·la», «Enviament» in the same dialog → «Desa», «Cancel·la», «Envia».
- Detect: review all button labels together.
- Exceptions: an existing style guide that mandates the other form.

### CA-09 · Register · medium

- What: mixing «tu» and «vostè» (or «vosaltres» and «vostès») in the same product or document, or using «vostè» in a context where the audience expects «tu».
- Why: it breaks the voice. The choice belongs to the brand, and once made it applies to every string, including emails, errors and chat widgets.
- Detect: verb forms and pronouns of both registers in the same project.
- Exceptions: quotations, legal texts with their own convention.

### CA-10 · Formulas and fillers · medium

- What: «Espero que estiguis bé», «No dubteu a posar-vos en contacte amb nosaltres», «Restem a la vostra disposició per a qualsevol dubte», «Quedo a l'espera de les vostres notícies», «Esperem que estigui tot bé», «En resum», «En definitiva», «Cal destacar que», «Val a dir que», «És important tenir en compte que», «Anem a veure», «Som-hi», «A continuació us expliquem».
- Why: W-21 and W-26 in Catalan. They lengthen emails and make them sound templated.
- Detect: list in `detect.py` (`W-21`, `W-26`).
- Exceptions: one closing formula in a formal letter is fine when it is the expected form.

### CA-11 · Bureaucratic verbs · low

- What: «realitzar» (→ «fer»), «efectuar», «procedir a», «dur a terme» everywhere, «comptar amb» (→ «tenir»), «disposar de».
- Why: heavier and vaguer than the plain verb.
- Detect: frequency of these verbs (`CA-11`).
- Exceptions: legal and administrative texts that require them.

### CA-12 · Generic headings · medium

- What: «Coses a tenir en compte», «Aspectes clau», «Punts clau», «Conclusions finals», «Consideracions addicionals», «Informació important».
- Why: W-34 in Catalan.
- Detect: list in `detect.py` (`W-34`).
- Exceptions: report templates.

### CA-13 · Anglicisms in interfaces · low

- What: «email», «online», «click», «login», «password» where Catalan has an established term: «correu», «en línia», «clic», «inici de sessió», «contrasenya».
- Why: mixed vocabulary looks unfinished.
- Detect: list in `detect.py` (`CA-13`).
- Exceptions: brand names, technical audiences that use the English term, «app».
