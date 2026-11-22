# Sources and attribution

The catalogs in this skill are written in our own words. Where an entry follows a source closely, the source is listed here. Rule names and ideas are not copyrightable, but we credit them anyway because they shaped the catalog.

## Adapted sources

### Impeccable, by Paul Bakaus

- Repository: https://github.com/pbakaus/impeccable · site: https://impeccable.style (anti-pattern gallery at https://impeccable.style/slop).
- Licence: Apache License 2.0, copyright 2025 Paul Bakaus. A copy of the licence is in `LICENSE` and the attribution is in `NOTICE`.
- What we adapted (reworded, with our own thresholds and examples, and merged with other rules):
  - Design: side-stripe border (D-03), nested cards (D-02), glassmorphism (D-07), hard offset shadow (D-08), eyebrows and tracked uppercase labels (D-12, D-13), monospace as costume (D-16), AI palette gradients and gradient text (D-20, D-21), dark glow (D-22), cream default (D-24), grey on colour (D-26), identical card grid (D-34), hero metric (D-35), everything centred (D-32), icon in a tinted circle (D-46), bounce and elastic easing (D-51), animating layout properties (D-53), modal by default (D-55), the cramped/flat-hierarchy family (D-30, D-37).
  - Workflow: the idea of a review pass with severity levels before delivery and of a static detector that flags patterns by rule ID.
- Changes: new IDs, new wording, merged and split rules, added exceptions and detection rules for Tailwind and plain CSS. No Impeccable files are copied.

### Anthropic frontend-design skill

- https://github.com/anthropics/skills (skills/frontend-design). Licence: Apache License 2.0, copyright Anthropic.
- Adapted ideas: structural devices must encode information (D-48), template chrome such as tracked eyebrows and mono labels (D-12, D-16), the recognisable "AI design" clusters behind D-24 and D-42, entrance animation on every section and hover on every card (D-50, D-57), "spend boldness in one place".

### Anthropic cookbook: prompting for frontend aesthetics

- https://github.com/anthropics/claude-cookbooks · article "Prompting for frontend aesthetics". Licence: MIT, copyright Anthropic.
- Adapted ideas: default fonts and purple gradients as signals of generated design (D-10, D-20), commit to one direction instead of averaging.

### Wikipedia: Signs of AI writing

- https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing. Licence: CC BY-SA 4.0.
- Used as background for the English catalog and several general rules: vocabulary by period (EN-01), significance inflation (EN-05), vague attribution (EN-06), copula avoidance (W-42), negative parallelism (W-13), participle tails (W-43), rule of three (W-16), formatting tells (W-14, W-37), chatbot residue (W-44). Everything is reformulated. No sentences or lists are copied, so the share-alike clause does not apply to this skill.

### stop-slop, by Hardik Pandya

- https://github.com/hardikpandya/stop-slop. Licence: MIT, copyright 2025 Hardik Pandya.
- Adapted ideas: throat-clearing openers (EN-03), intensifier adverbs (EN-04), punchline closers (W-17).

### humanizer, by Siqi Chen

- https://github.com/blader/humanizer. Licence: MIT, copyright 2025 Siqi Chen.
- Adapted ideas: grouping AI-writing tells into content, language, style and communication patterns, and the instruction to rewrite rather than only list problems.

## Language references

- Catalan: Institut d'Estudis Catalans (https://www.iec.cat), Optimot (https://aplicacions.llengua.gencat.cat/llc/AppJava/index.html), ésAdir (https://esadir.cat).
- Spanish: Real Academia Española and the Diccionario panhispánico de dudas (https://www.rae.es), FundéuRAE (https://www.fundeu.es).

No public catalog of AI-writing tells exists for Catalan or Spanish. The CA-xx and ES-xx entries come from observed corrections of generated text and from the usage references above.

## Other influences

- Public anti-slop design checklists consulted for coverage: impeccable.style/slop, unslop-ui, and essays on generic AI design from design studios. No text from them is reused.
- Nielsen's usability heuristics, Bringhurst's *The Elements of Typographic Style* and WCAG 2.2 for the baseline checks in D-11, D-18, D-26 and D-60.
