---
name: anti-slop
description: Prevents and removes "AI slop", the generic look and voice of generated work. Load it before you write or edit anything a person will read or see, however short: a list of headings or slide titles, button labels, an error message, one paragraph, an email, a full document or a whole interface. That covers UI, CSS, Tailwind, components, landing pages, slides, documents, reports, proposals, emails, messages, release notes, docs and microcopy, in English, Catalan or Spanish. Also use it to review existing work and when someone says "slop", "AI-flop", "looks AI-generated", "polish", "review the style", "sembla fet per IA", "revisa l'estil" or "parece hecho por IA". It holds a catalog of concrete anti-patterns (boxes, cards in cards, side stripes, eyebrows, gradients, comma splices, fragments, comma-tag and slogan headings, calques, filler, invented facts) and a review pass to run before delivering.
---

# Anti-slop

Generated work drifts towards the same defaults: boxes around everything, a purple gradient, an eyebrow over every heading, sentences joined with commas, headings that sound like slogans and paragraphs that explain what the reader already knows. Each default is harmless alone. Together they make work look unreviewed.

This skill gives you a catalog of those defaults with IDs, a way to detect them, and a review pass to run before anything is delivered.

## Personal and project rules

Before starting, look for these files and load them if they exist:

1. `.anti-slop.md` at the root of the current project.
2. `~/.claude/anti-slop.personal.md`.

Their rules take priority over this skill. If the two files disagree, the project file wins inside that project. They may also switch off a rule of this skill (for example, a brand that uses tracked uppercase labels on purpose).

## Principles

- Every element and every sentence has a job. If removing it loses nothing, remove it.
- Say the specific thing. A real number, name or example beats a general claim. Specific means taken from the brief, the source or the project. When those facts are missing, write less or leave a marked gap. Never invent details, deadlines or promises to sound concrete. Specific is not exhaustive either: one figure the reader will remember beats ten that are all true.
- Write sentences that join ideas with the right connector. Do not stack fragments or splice clauses with commas.
- Headings and titles name the topic with a short noun label. They are not slogans, questions or taglines, and they never end in a comma tag such as "…, step by step", «…, pregunta per pregunta» or «…, ben aviat».
- Hierarchy comes from size, weight, space and position before borders, boxes and colour.
- Reuse what the project already has. One component, one spacing scale, one way to label actions.
- Decoration must carry information. Numbers, coordinates, labels and dividers that mean nothing are fake.
- Never invent facts. No made-up metrics, testimonials, clients or quotes.
- Do what was asked and no more. No extra sections, items, notes, disclaimers or follow-up offers that the brief did not ask for. A short brief gets a short answer.
- Your own messages follow the same rules. Explanations to the user are plain prose, without bold-label bullet lists.

## Workflow

1. Load references. Before generating, read the catalogs that apply:
   - Interface, CSS, components, slides layout: `references/design.md`.
   - Any text: `references/writing.md` plus the file for the language, `writing-ca.md`, `writing-es.md` or `writing-en.md`.
   - Marketing pages, documents, emails, reports, any page with claims or sections: `references/content.md`.
   For a short text or a small component, the checklist below is enough.
2. Generate. Follow the project's existing patterns first, then the principles above.
3. Review. Before delivering, go through the checklist below item by item against what you produced. If there are files, also run the detector:
   ```bash
   python3 <skill-dir>/scripts/detect.py <paths> --min-severity medium
   ```
   Treat its output as suspicions. Each hit needs a decision, and the detector cannot see most structural problems, so the checklist still applies.
4. Fix before delivering. Rewrite what fails and review again. Never deliver a sloppy version with a list of its defects at the end. If a rule conflicts with an explicit request, follow the request. If the request itself invites slop ("add animations so it feels alive", "make it pop"), meet the intent with the restrained version and say so in one sentence.
   When the input is already clean, say so in one sentence and return it unchanged. Do not justify the verdict with a checklist, and do not polish for the sake of it.
   Small fixes to existing work go ahead without asking: a label, a spacing value, a border, a comma splice, a heading, a word. Before a large change, stop and ask the user, even when the catalog calls for it. In design that means a new layout, palette, type system or navigation, or removing, merging or reordering sections. In text it means rewriting most of a passage, or changing its structure, tone, argument or length. Describe the proposed change in a few lines, apply the small fixes, and wait for an answer before doing the large one.
5. Audits. When asked to review existing work, return findings instead of rewriting. Sort them by severity, high first. Write one numbered line per finding in this form:
   `[high] D-21 · line 5, <h1> · gradient text on the heading · use a solid colour from the palette`
   That is severity, rule ID, location (line, element, slide, section or quoted text), the problem and a concrete fix. Check that each ID matches the catalog. Group repeated instances of the same rule on one line. Do not rewrite the work and do not add a summary of what is fine. End with one sentence offering to apply the fixes.

## Review checklist

The most frequent and most damaging patterns come first. IDs point to the catalogs.

1. Sentence joins (W-01, W-03, W-04). No two main clauses glued with a comma. No runs of short sentences that read in jolts. Ideas are linked with connectors that state the relation (because, but, so, which).
2. Fragments and compression (W-02, W-05, W-06). Running text uses complete sentences with a verb. No noun piles such as "Monthly incidents and per-area contacts". No shorthand that forces the reader to rebuild the meaning.
3. Consistency (D-40, D-41, CA-08). The same element looks and behaves the same everywhere. Values come from the scale, not one-offs. Action labels use one grammatical form.
4. Spacing and alignment (D-30, D-31, D-33, D-38). Enough room around and between elements, spacing that follows a rhythm, shared alignment edges, and the same density for content of the same kind.
5. Boxes (D-01, D-02, D-04). No container without a job, no card inside a card, no border plus background plus shadow on the same box. Use space and type to group.
6. Filler and the obvious (C-05, C-06, C-09, C-11, W-20). No sections that exist because a template has a slot, no action points that are already done or obvious, no microcopy that describes what the reader already sees, no fact repeated in several places, nothing the brief did not ask for. No counts of what was built and no dated release notes on a home page (C-14), no pile of true figures where one would do (C-15). An automatic notification is a clear subject plus the data. An acknowledgement email is one or two sentences.
7. Type hierarchy (D-10, D-11, D-15, D-37). A deliberate type scale with clear steps, few weights, readable sizes, and a visible order of importance.
8. Labels and tracking (D-12, D-13, D-14). No eyebrow above every heading, no small grey uppercase labels by default, no letter-spacing added without a reason.
9. Punctuation tics (W-10, W-11, W-12, W-19). No semicolons, no em dashes, no « » or “ ” around names, labels and titles, and no colon used as a hinge between two clauses.
10. Headings (W-30, W-31, W-33, W-34). No comma tags such as "Topic, step by step", «Resultats, punt per punt» or «El proyecto, en detalle», even when the brief uses that phrase. No slogans, no "2 things to know before you visit", no generic "Key takeaways". The heading names what the section contains, and card or column subtitles name the topic, not a verdict. Read all the headings of the piece in a row: any that sounds like a slogan or a translation gets rewritten, and several that share one formula ("30 tools, each with its label") get varied. No headline split into two colours or weights (D-28).
11. Side stripes (D-03). No thick coloured border on one side of a box as decoration.
12. Gradients and glow (D-20, D-21, D-22, D-25). No purple-to-blue gradients, no gradient text, no glow on dark backgrounds, no gradient as the default fill.
13. Motion (D-50, D-51, D-54, D-56, D-58). No fade-up on every section, no text that stays hidden or faded until it is scrolled into view, no bounce or elastic easing, no infinite decorative motion (float, drift, pulse, glow loops, logo marquees), no custom cursor or reading-progress bar, and a reduced-motion alternative for what remains. Even when asked for more motion, use one or two purposeful moments.
14. Negation (W-13, W-18, W-23). No "It's not X, it's Y" or "not just X but Y", and no "…, not a guarantee" tail on every caption. Say what the thing is, and keep a caveat only where a wrong reading is likely.
15. Openers, closers and signposting (W-21, W-26, W-27). No "I hope this finds you well", "It's worth noting", "Below you will find", no text about the text, no internal notes.
16. Calques and register (W-40, W-41, CA-02, ES-02). No word-by-word translations ("fa sentit", "a nivel de"). One register throughout.
17. Template sections (D-34, D-35, D-36, D-39). No grid of identical icon cards, no big-number hero strip, no sequence of sections with the same layout, such as a heading on the left and a lead paragraph on the right in every section.
18. Invented content and internal notes (C-01, C-02, C-07, C-12). No unsourced numbers, details or deadlines, no placeholder names, lorem ipsum, TODOs or "subject to validation". Public documentation describes what is available and leaves out features that are not active yet.
19. Emoji (D-45, W-38). No emoji used as icons in UI or as decoration in headings and bullets.
20. Bold and bullets (W-14, W-35, W-37). No "**Label:** fragment" bullet lists, no bullets where a paragraph belongs, no bold scattered through prose.

Two more checks for tone, when the text addresses people: no inflated or cheerleading language (W-22, W-29) and no warmth that cannot be verified, such as "our door is always open" (W-24).

## Detector

`scripts/detect.py` is a heuristic scanner with no dependencies. It reads `.css .scss .html .tsx .jsx .vue .svelte .astro .md .mdx .txt`, skips `node_modules`, `.git`, `dist`, `build` and `vendor`, and reports `file:line: RULE [severity] message | excerpt`.

- `--json` for machine-readable output.
- `--min-severity low|medium|high` to filter, `--fail-on high` (default) sets which findings give exit code 1, `--fail-on none` never fails.
- `--lang ca|es|en` forces the language. By default it is detected per paragraph.
- `--list-rules` prints every rule it implements.
- `anti-slop-ignore` on a line silences it, optionally for given IDs (`anti-slop-ignore D-14`). `anti-slop-ignore-file` skips a file.

Severity in the detector reflects confidence as well as impact, so a rule can be high in the catalog and medium in the detector. `python3 scripts/test_detect.py` runs it against the fixtures in `evals/detect-fixtures/`.

## Working with other skills

For deep design work (a full critique, a redesign, a design system), a dedicated design skill such as Impeccable goes further than this catalog. Use both: the other skill for direction, this checklist as the final pass. When another skill or a project style guide sets an explicit rule, it wins over a default here.

## Reference files

| File | Load when |
|---|---|
| `references/design.md` | Any interface, component, CSS, Tailwind, slide or document layout (D-01 to D-60) |
| `references/writing.md` | Any text (W-01 to W-44) |
| `references/writing-ca.md` | Text in Catalan (CA-01 to CA-13) |
| `references/writing-es.md` | Text in Spanish (ES-01 to ES-10) |
| `references/writing-en.md` | Text in English (EN-01 to EN-10) |
| `references/content.md` | Pages, documents and emails with claims, sections, numbers or calls to action (C-01 to C-15) |
| `references/sources.md` | Attribution and background |
