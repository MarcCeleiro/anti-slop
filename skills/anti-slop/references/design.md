# Design anti-patterns

Catalog of visual patterns that make an interface, slide or document look machine-made, or simply worse. Each entry has the same fields. Severity is a default and the context can raise or lower it.

- What: the pattern.
- Why: why it reads as generated or hurts the result.
- Bad → good: a concrete swap.
- Detect: a CSS/Tailwind signal, a regex used by `scripts/detect.py`, or a review question.
- Exceptions: when the pattern is legitimate.

The detector only raises suspicions. The final call is always a look at the rendered result.

## Contents

1. Containers and surfaces: D-01 to D-08
2. Typography: D-10 to D-19
3. Colour: D-20 to D-28
4. Layout and spacing: D-30 to D-39
5. Consistency: D-40 to D-42
6. Decoration and imagery: D-45 to D-49
7. Motion and interaction: D-50 to D-58
8. Quality floor: D-60

## 1. Containers and surfaces

### D-01 · Box without a job · high

- What: content wrapped in a bordered, filled or shadowed container that does nothing a heading and some space would not do. Pages end up "boxed in", every paragraph sitting in its own panel.
- Why: generators reach for a card because it is the safest way to make anything look finished. Boxes add noise, cut the reading width, and flatten hierarchy because everything gets the same frame.
- Bad → good: three paragraphs of an about page, each in a white card with a shadow → the same paragraphs on the page background, separated by space and a heading.
- Detect: review question: "If I remove this container and keep the spacing, is anything lost?" Count framed blocks per screen. More than one framed block per viewport that is neither interactive nor a distinct object is suspect.
- Exceptions: things that are objects (a product, a message, a file, a draggable item), interactive targets, regions that must stay grouped when content reflows, alerts.

### D-02 · Card inside a card · high

- What: a framed element (border, shadow, radius or fill) nested inside another framed element.
- Why: two frames say the same thing twice. The inner frame steals space and the eye cannot tell which level matters.
- Bad → good: a settings card holding three bordered sub-cards → one card with sections divided by spacing or a single hairline, or three sibling cards with no wrapper.
- Detect: an element whose classes include `card`, `panel`, or `rounded-*` plus `border`/`shadow`/`bg-*` with an ancestor that has the same traits (`D-02` in `detect.py`). Ignore menus, popovers, dialogs and tiny chips.
- Exceptions: a real object inside a container (an attachment inside a message, a code block inside a doc card), modal content.

### D-03 · Side-stripe border · high

- What: a box with a thick coloured border on only one side, usually left or top, as an "accent". Also the callout with a left bar and a tinted fill.
- Why: it is the single most recognisable generated-UI tell. It decorates without meaning anything, and when every note, quote and card has the stripe it stops signalling anything.
- Bad → good: `border-left: 4px solid var(--accent)` on every feature card → no border, a heading and space. If the box must stand out, use a full subtle tint or a leading icon that means something.
- Detect: CSS `border-(left|right|top|bottom|inline-start|block-start): Npx solid` with N ≥ 2 while the other sides have no border. Tailwind `border-l-4`, `border-t-2`, `border-s-4`, `border-l-[3px]`. Severity rises when the box also has a radius.
- Exceptions: blockquotes in long-form text, the active item in a navigation list, status regions where the colour encodes state (error, warning) and the pattern is used once, diff and code annotations, table rows with a 1px bottom divider.

### D-04 · Stacked chrome · medium

- What: border, shadow and background fill all on the same element. Includes the "ghost card": 1px light border plus a wide soft shadow. Also shadows on everything.
- Why: each of the three already separates the element from the page. Stacking them is indecision, and a soft shadow repeated on every element makes the page look foggy.
- Bad → good: `border border-gray-200 shadow-lg bg-white rounded-2xl` → one of them, chosen for the context: a border on a white page or a fill on a tinted page.
- Detect: same element with `border` + `shadow-(md|lg|xl|2xl)` + `bg-*` in Tailwind, or a CSS rule with `border`, a non-`none` `box-shadow` and `background` together.
- Exceptions: elevated layers that float over content (menus, popovers, sticky bars), where shadow plus border helps on any background.

### D-05 · Decorative dividers · low

- What: horizontal rules, ornaments or separator lines between blocks that are already separated by space or headings. Footer columns split by vertical lines.
- Why: the separation already exists. Extra lines add stripes and make the page look like a form.
- Bad → good: `<hr>` between every section → larger space above each heading.
- Detect: more than two `<hr>` or `divide-*`/`border-b` separators per screen that are not in a list or table.
- Exceptions: dense lists and tables, menus, long documents where a rule marks a real change of part.

### D-06 · One radius and pills everywhere · low

- What: the same large radius (16–24px or more) on every surface, or every button, tag and input shaped as a pill.
- Why: a single soft radius is the default of every UI kit. Without a reason, it looks like a template.
- Bad → good: buttons, cards, images and inputs all `rounded-2xl` → a small radius scale tied to size (inputs and buttons 6–8px, cards 12–16px, pills only for small chips).
- Variant: a signature shape (a cut corner, a notch, a slanted edge) applied to every element, including videos, buttons, tags and the cookie banner. The motif stops meaning anything once nothing is without it.
- Detect: one `rounded-*` value covering most framed elements, or `rounded-full` on buttons with text. More than a dozen `clip-path: polygon(…)` rules in one stylesheet.
- Exceptions: a brand system that defines the shape. Avatars and small chips. A signature shape kept for a few elements that deserve it, such as the logo and the main media.

### D-07 · Glass and blur as decoration · medium

- What: frosted translucent panels (`backdrop-filter: blur`) used as the default surface, often on top of a gradient.
- Why: it costs contrast and performance and was a fashion default for two years.
- Bad → good: glass cards over a gradient hero → opaque surfaces with a clear text colour.
- Detect: `backdrop-filter`, `backdrop-blur-*`.
- Exceptions: system bars and overlays on platforms where translucency is native (for example iOS materials), sheets over live content.

### D-08 · Hard offset shadow by default · low

- What: crisp unblurred offset shadows (`4px 4px 0 #000`) on cards and buttons.
- Why: a neobrutalist default that generators apply to make something look "bold".
- Bad → good: offset shadow on every card → no shadow, or a real brand reason documented in the design system.
- Detect: `box-shadow` with zero blur and offset ≥ 3px.
- Exceptions: a deliberate neobrutalist identity applied consistently.

## 2. Typography

### D-10 · Default font without intent · medium

- What: Inter, Roboto, Arial, Helvetica, Open Sans, Lato, Montserrat, Poppins or `system-ui` used as the only face, chosen because it was there. Also the reflex "tasteful" picks: Playfair Display, Fraunces, Instrument Serif, Space Grotesk, DM Sans.
- Why: it makes every product look like every other one.
- Bad → good: `font-family: Inter, sans-serif` on a cultural festival site → a face that belongs to the subject, or the brand's face. For product UI, the platform font is a legitimate deliberate choice.
- Detect: the first family in `font-family`, Google Fonts URLs, Tailwind `fontFamily` config.
- Exceptions: brand fonts, native apps using the platform face on purpose, internal tools where neutrality is the brief.

### D-11 · No type scale · high

- What: many sizes that are close to each other (14, 15, 16, 17, 18px), or a few sizes so close that headings do not read as headings. Also running text below 16px on the web and labels below 12px.
- Why: hierarchy comes from clear steps. Close sizes look like mistakes and tiny text hurts everyone.
- Bad → good: seven sizes between 13 and 20px → four or five sizes on a ratio of at least 1.2 (product UI) or 1.25 (marketing and documents), body at 16px or more.
- Detect: distinct `font-size` values in a file (more than six is suspect), sizes below 12px (`font-size: 11px`, `text-[10px]`), the largest step below 1.2.
- Exceptions: dense data tables and legal footnotes, which can go to 12–14px if they stay readable.

### D-12 · Eyebrow above every heading · high

- What: a small uppercase, tracked, often coloured label above a heading ("FEATURES", "OUR PROCESS", "WHY US").
- Why: it repeats the heading, adds a third level of type that rarely means anything, and is one of the most recognisable template moves.
- Bad → good: `<span class="uppercase tracking-widest text-xs text-indigo-600">Features</span><h2>Everything you need</h2>` → `<h2>Features</h2>` with a real sentence below.
- Detect: classes named `eyebrow`, `kicker`, `overline`, `pretitle`, or `uppercase` + `tracking-*` + `text-xs`/`text-sm` on an element placed just before an `h1`–`h3`.
- Exceptions: a real category or date above an article title, in an editorial context, used consistently.

### D-13 · Small grey uppercase labels · medium

- What: table headers, form labels, card metadata and section labels set in small, grey, uppercase, often tracked type.
- Why: it lowers contrast and legibility exactly where people scan, and it is a template default.
- Bad → good: table headers `text-xs uppercase text-gray-400 tracking-wider` → sentence case, normal size, a darker colour, medium weight.
- Detect: `uppercase` together with `text-(gray|slate|zinc|neutral)-(300|400|500)` and a small size. `text-transform: uppercase` in `th` or label rules.
- Exceptions: very short codes (country, currency, status abbreviations) and a brand system that specifies it.

### D-14 · Letter-spacing added by default · medium

- What: tracking added to text that does not need it, mostly to uppercase labels and headings (`tracking-wide`, `letter-spacing: 0.1em`), or negative tracking pushed too far on display text.
- Why: positive tracking on labels is part of the eyebrow kit. Strong negative tracking makes letters collide. A good typeface is already spaced.
- Bad → good: `letter-spacing: 0.12em` on headings → remove it. On very large display text, a small negative value (−0.01 to −0.02em) may be justified and must stay above −0.04em.
- Detect: `letter-spacing` values other than `normal`/`0`, Tailwind `tracking-*`.
- Exceptions: small caps or all-caps acronyms set intentionally, and display sizes above about 60px. Many teams prefer a strict "no letter-spacing unless asked" rule, which belongs in the personal file.

### D-15 · Weight noise · medium

- What: bold scattered through menus, labels and paragraphs, or the opposite, one weight for everything so nothing stands out.
- Why: emphasis only works when it is rare. Bold submenus and bold labels everywhere flatten the page.
- Bad → good: every menu item at 600 → regular items, the current one marked by colour or an indicator.
- Detect: proportion of elements with `font-bold`/`font-semibold`/`font-weight: 600+`. In prose see W-37.
- Exceptions: data tables where totals are bold, headings.

### D-16 · Monospace as costume · medium

- What: monospace for labels, numbers and captions to look technical or "editorial brutalist".
- Why: mono is useful when fixed width does a job (aligned figures, code, coordinates). Used everywhere it is a style tic.
- Bad → good: `font-mono uppercase text-xs` on every label → the body face. Use tabular numerals (`font-variant-numeric: tabular-nums`) where columns must align.
- Detect: `font-mono` on elements that contain words rather than code or figures.
- Exceptions: code, terminals, tables of figures, technical products where mono is part of the brand.

### D-17 · Arbitrary serif and italic display · low

- What: an italic serif headline over a sans body, or serif and sans mixed without a role for each.
- Why: it is the "editorial" default of generators and rarely tied to the subject.
- Bad → good: italic serif h1 on a SaaS dashboard → the UI face at a heavier weight.
- Detect: review question: "What job does each family do?" Two families without distinct roles is suspect.
- Exceptions: publications and brands whose identity uses that pairing.

### D-18 · Long lines and tight leading · medium

- What: paragraphs running the full width of a wide screen, or body text with line-height below 1.4.
- Why: lines above about 80 characters and cramped leading slow reading.
- Bad → good: full-width paragraph at 1.2 → `max-width: 65ch` and line-height 1.5–1.6.
- Detect: missing `max-width` on prose containers, `line-height` below 1.4 on body text, `leading-tight` on paragraphs.
- Exceptions: short UI strings, captions, headings (1.1–1.3 is fine).

### D-19 · Stub lines in headings · low

- What: headings that break with one word on the last line, and in Catalan, Spanish and other languages a one-letter word stranded at the end of a line.
- Why: it looks unfinished and is easy to prevent.
- Bad → good: add `text-wrap: balance` to headings and `text-wrap: pretty` to paragraphs. Bind single-letter words to the next word with a non-breaking space where the language convention asks for it.
- Detect: review at two or three widths. No reliable static check.
- Exceptions: none worth listing.

## 3. Colour

### D-20 · AI palette gradient · high

- What: purple to blue, violet to pink or indigo to cyan gradients as the primary brand surface. Also neon cyan or purple accents on near-black.
- Why: it is the palette every generator falls back to and has become a recognisable signature.
- Bad → good: `bg-gradient-to-r from-purple-600 to-blue-500` hero → a flat colour from the subject's world, or the brand palette.
- Detect: `linear-gradient`/`radial-gradient` whose stops include purple, violet or indigo hues together with blue, cyan, pink or fuchsia. Tailwind `from-(purple|violet|indigo|fuchsia)-N` with `to-(blue|cyan|sky|pink|indigo|violet)-N`.
- Exceptions: a brand whose identity really is that gradient.

### D-21 · Gradient text · high

- What: headings filled with a gradient through `background-clip: text`.
- Why: it lowers legibility and is a strong generated-landing-page tell.
- Bad → good: gradient h1 → solid colour, emphasis through size or weight.
- Detect: `background-clip: text`, `-webkit-background-clip: text`, Tailwind `bg-clip-text` with `text-transparent`.
- Exceptions: a logo or wordmark.

### D-22 · Glow on dark · medium

- What: coloured outer glows, neon borders and radial halos behind sections on dark backgrounds.
- Why: dark mode with glowing accents is a stock "tech" look and the halos reduce contrast.
- Bad → good: `box-shadow: 0 0 40px rgba(139,92,246,.5)` → no glow, contrast from surface colours.
- Detect: chromatic `box-shadow` with blur and no offset, Tailwind `shadow-(purple|cyan|blue|indigo|violet)-*`, `shadow-[0_0_`, low-alpha radial gradients.
- Exceptions: focus rings (no blur), real light sources in an illustration.

### D-23 · Untinted pure black and grey · low

- What: `#000` text on `#fff`, and greys with no hue, across the whole interface.
- Why: pure black on white is harsh on screens and dead greys look generic next to a coloured brand.
- Bad → good: `#000` and `#6b7280` → near-black and greys tinted slightly towards the brand hue.
- Detect: `#000`, `#000000`, `rgb(0,0,0)` as text or background colour on large areas.
- Exceptions: print, e-ink, deliberately stark identities.

### D-24 · Default cream background · low

- What: a beige or cream page background chosen to look "warm and tasteful", often with a serif and a terracotta accent.
- Why: it is one of the named AI aesthetic clusters.
- Bad → good: `bg-stone-50` everywhere with no brand reason → white, or a colour from the brand.
- Detect: page background with a light warm tone (Tailwind `bg-(amber|orange|stone|yellow)-50/100`, hex with high values and red > green > blue).
- Exceptions: the brand's real colour (for example a paper or logo colour).

### D-25 · Gradient as default fill · medium

- What: gradients on page headers, buttons, cards or photo overlays where a flat colour would do. Page headers that fade into a different colour than the section below.
- Why: gradients are a shortcut to "polish". On headers they break the continuity with the content.
- Bad → good: header with a gradient that does not match the hero below → flat colour, the same as the next section.
- Detect: `linear-gradient` on header, button and card selectors, Tailwind `bg-gradient-to-*`.
- Exceptions: photography overlays needed for text contrast (keep them subtle), data visualisation scales.

### D-26 · Grey on colour and low contrast · high

- What: neutral grey text on a coloured background, light grey text on white, placeholder-grey for real content.
- Why: it fails contrast and looks washed out.
- Bad → good: `text-gray-500` on `bg-blue-600` → white or a light tint of the blue.
- Detect: Tailwind `text-(gray|slate|zinc|neutral)-*` on an element or parent with a saturated `bg-*`. Check 4.5:1 for body text and 3:1 for large text and icons.
- Exceptions: none for real content.

### D-27 · Colour without a system · medium

- What: icons, chips or categories with colours that do not follow a rule (some blue, some red, for no reason), or the default framework blue where the brand colour should be.
- Why: random colour reads as noise and makes people look for a meaning that is not there.
- Bad → good: map pins in blue and red with no meaning → one colour, or a colour per category that matches the legend.
- Detect: review question: "What does each colour mean?" Default blues (`#3b82f6`, `#2563eb`, `#007bff`) in a branded project.
- Exceptions: data where colour encodes a real category.

### D-28 · Two-tone headline · medium

- What: a heading split in two, with the second half in the accent colour, a lighter weight or a muted tone ("We build products. <span>That people use.</span>"). Often the second half sits on its own line after a `<br>`.
- Why: it is the landing-page default of current generators. The colour change stresses a rhythm, not a meaning, and it turns every heading into a two-part slogan (W-31).
- Bad → good: "Interiors, / <span class="accent">made to last</span>" → one colour and one weight, and a heading that names the section ("Kitchen renovations").
- Detect: an `h1`–`h3` whose text ends in a `<span>`, `<em>` or `<strong>` that holds the last phrase, especially after a `<br>` or with an accent, muted or text-colour class.
- Exceptions: a brand mark or a product name set in its own colour, or one emphasised word that carries real meaning.

## 4. Layout and spacing

### D-30 · Cramped · high

- What: elements touching each other, forms with no space between fields, buttons glued to text, text touching the edge of its container or the viewport.
- Why: it makes the page feel broken and hard to scan.
- Bad → good: form fields with `margin: 4px` → 16–24px between fields, 8px between label and input, comfortable padding inside controls.
- Detect: padding below about half the font size inside controls, `gap-0`/`gap-1` between blocks, text within 16px of the viewport edge on mobile.
- Exceptions: dense data views designed as such.

### D-31 · Spacing without rhythm · medium

- What: the same gap everywhere, so nothing groups, or large random gaps (a big empty band above a title, uneven space between sections).
- Why: proximity is how people see groups. Uniform or random spacing hides the structure.
- Bad → good: 48px between every element → small gaps inside a group, larger gaps between groups, more space above a heading than below it.
- Detect: one spacing value used for more than about 60% of gaps, or gaps that differ between sibling sections. Review question: "Can I see the groups with my eyes half closed?"
- Exceptions: none.

### D-32 · Everything centred · medium

- What: headings, paragraphs, lists and buttons all centre-aligned, section after section.
- Why: centred paragraphs are hard to read and a page of centred blocks has no edge to follow.
- Bad → good: centred three-line paragraphs → left-aligned text on a shared edge. Keep centring for a short hero line or a single call to action.
- Detect: many `text-center`/`text-align: center` and `mx-auto` in one file, or on paragraphs longer than two lines.
- Exceptions: very short marketing moments, empty states, logos.

### D-33 · Inconsistent alignment · high

- What: some rows aligned left and others stretched across, lists with a left padding that breaks the page edge, labels and values on different baselines, icons not centred with their text.
- Why: misalignment is the clearest sign that nobody looked at the result.
- Bad → good: list rows where some items have a two-line layout and others span the full width → one row pattern for the whole list.
- Detect: review at desktop and mobile widths. Look for `pl-*` on lists inside already padded containers.
- Exceptions: none.

### D-34 · Identical icon-card grid · high

- What: the classic three (or four, or six) equal cards, each with an icon, a short heading and two lines of text, used as a page section.
- Why: it is the most common generated section. It forces content into equal boxes whether or not the items are equal.
- Bad → good: "Fast · Secure · Scalable" cards → a short paragraph, a list with real detail, or one strong example.
- Detect: `grid-cols-3`/`md:grid-cols-3`/`repeat(3, …)` whose children all hold an icon plus heading plus paragraph.
- Exceptions: real collections of similar objects (products, people, articles).

### D-35 · Hero metric and KPI strip · high

- What: a big number with a small label and a gradient accent ("10x faster", "99.9% uptime"), or a row of KPI tiles on top of a dashboard that nobody acts on.
- Why: the numbers are often invented (see C-01) and KPI strips push the useful content down.
- Bad → good: four KPI tiles above an admin screen → the list or table people came for, with the one figure that matters in the page title.
- Detect: large `text-4xl`+ numbers followed by a small label, repeated in a row. Review question: "Which decision does this number support?"
- Exceptions: dashboards whose job is the metric, with real data.

### D-36 · Repeated identical sections · medium

- What: section after section with the same structure (heading, paragraph, three items), only the words change.
- Why: the page has no rhythm and the reader cannot tell what matters.
- Bad → good: five sections built from the same block → vary the form with the content: a table, a quote, an image, a list.
- Detect: review question. The same component repeated more than three times in a row as page structure.
- Exceptions: long documentation with a fixed pattern.

### D-37 · Flat hierarchy · high

- What: headings that do not stand out from text, several elements competing for attention, no obvious first thing to read.
- Why: the reader has to work out the order alone.
- Bad → good: title and body at 18 and 16px with the same weight → a clear size step and a single primary action per view.
- Detect: squint test. Heading-to-body ratio below 1.25. More than one primary-styled button per view.
- Exceptions: none.

### D-38 · Inconsistent density · medium

- What: one part of the screen is tight and another very loose, or one list packs five fields per row while the next has one.
- Why: density changes should follow content. Random density looks unplanned.
- Bad → good: a compact table next to an airy card grid with the same data → one density per data type.
- Detect: review question.
- Exceptions: a deliberate change between overview and detail.

### D-39 · Split header on every section · medium

- What: every section opens with the same two-column header, a large heading on the left and a grey lead paragraph on the right, followed by a full-width block.
- Why: it is the most common section shell in generated landing pages. Repeated down the page it flattens rhythm (D-36) and pushes the lead paragraph into a narrow column far from the content it introduces.
- Bad → good: eight sections, each with "H2 left, intro right" → a heading above its content, an intro only where it adds something, and a different shape where the content asks for it.
- Detect: review question: "How many sections open with the same header layout?" More than two on a page is the signal.
- Exceptions: a deliberate editorial grid used throughout a long document.

## 5. Consistency

### D-40 · Same element, different look · high

- What: two buttons that do the same thing look different, headings of the same level vary in size, boxes on one page differ from boxes on another, the font changes between sections, icons come from different sets.
- Why: inconsistency is what people notice first and it breaks trust in the rest.
- Bad → good: a page title at 40px on one page and 32px on the next → one style per role, defined once and reused.
- Detect: compare the same role across screens. Look for repeated components with different classes.
- Exceptions: intentional variants named in the design system.

### D-41 · One-off values · medium

- What: hard-coded colours, sizes and spacings that bypass the existing tokens or variables.
- Why: one-off values drift and create D-40.
- Bad → good: `color: #1d4ed8` in a component → `color: var(--color-primary)`.
- Detect: hex colours and pixel values in component files when the project defines tokens or CSS variables.
- Exceptions: one-time art direction, documented.

### D-42 · Template sameness · medium

- What: different products, pages or widgets built from the same generated template so they all look alike (every chatbot widget, every landing page, every report cover).
- Why: the result is interchangeable. A useful test is "could this belong to any company in any sector?"
- Bad → good: identical chat widgets on five client sites → each takes its type, colours and tone from its own site.
- Detect: review question.
- Exceptions: a shared product that is meant to look the same.

## 6. Decoration and imagery

### D-45 · Emoji and unicode as icons · high

- What: emoji or symbols (✨, 🚀, ✅, ★, →) standing in for icons in headings, lists, buttons and features.
- Why: they render differently on each system, cannot be styled, and are a strong generated tell.
- Bad → good: "🚀 Fast setup" → a real icon from the project's set, or no icon.
- Detect: emoji code points inside headings, buttons, list items and labels.
- Exceptions: user-generated content, chat apps, informal channels where emoji are part of the voice. A star rating is information when it varies and has a source. A row of five stars over every hand-picked review is decoration.

### D-46 · Icon in a tinted circle · medium

- What: a small icon inside a coloured circle or rounded square placed above every heading or card. The same tile with an initial («R», «A») standing in for a reviewer's photo is the testimonial version.
- Why: decoration that repeats the heading and fills the grid in D-34.
- Bad → good: an icon tile on each of six features → no icon, or a small inline icon that helps scanning.
- Detect: `rounded-full`/`rounded-xl` + `bg-*-50/100` + fixed `w-10 h-10`/`size-12` wrapping an svg or icon component.
- Exceptions: app launchers, file types, avatars.

### D-47 · Badge and pill soup · medium

- What: many small chips and pills ("New", "Beta", "AI", status, tags) scattered across a view.
- Why: when everything is tagged nothing is.
- Bad → good: five pills per card → one status where it matters, the rest as plain text.
- Detect: more than about five `rounded-full` + `text-xs` + padding chips per view.
- Exceptions: tag-based interfaces (filters, labels in an inbox) and line or route chips that carry identity.

### D-48 · Fake instrumentation · medium

- What: decorative numbers (01/02/03), coordinates, version codes, grid backgrounds, stripes, grain and technical labels that do not refer to anything real. Also numbered navigation items, "02 / Selected work" labels, "01 / 03" counters on things that are not a sequence, and the year in Roman numerals in the footer ("© MMXXVI").
- Why: they imitate rigour. If the element could be replaced by random text without anyone noticing, it is decoration in disguise.
- Bad → good: "01 / Discovery, 02 / Design" on unordered items → plain headings. Numbering only for real sequences.
- Detect: `01`, `02`, `03` labels next to headings, `repeating-linear-gradient` and tiled grid backgrounds, `feTurbulence` grain.
- Exceptions: real steps, real coordinates, a visible grid that is the actual layout grid.

### D-49 · Generic imagery · medium

- What: stock photos of smiling teams at laptops, 3D blobs, abstract waves, unDraw-style illustrations, fake device mockups with made-up screens.
- Why: they carry no information about this product and look generated.
- Bad → good: a mockup with invented dashboard numbers → a real screenshot, a real photo of the place or team, or no image.
- Detect: filenames and alt text such as `hero-illustration`, `mockup`, `blob`, `abstract`. Review question: "Is this image of something real here?"
- Exceptions: projects that commission or license an illustration style on purpose.

## 7. Motion and interaction

### D-50 · Entrance animation on everything · high

- What: every section fades up, zooms in or slides in on scroll. Big elements scale from 0.8 to 1 on load. Headlines split into lines or words that slide up from a mask, and paragraphs that stay faded until they reach the middle of the screen.
- Why: it delays content, repeats the same gesture, and is the default of scroll-animation libraries. Text that is invisible at rest also fails in screenshots, print, reader mode and for anyone who jumps to an anchor: they see a blank or half-faded block.
- Bad → good: `data-aos="fade-up"` on every block → content visible at rest. Keep at most one authored moment that says something (a drawing line, a map that settles).
- Detect: `data-aos`, `whileInView`, `initial={{ opacity: 0`, `animate-fade-*`, `fade-up`, `zoom-in`, IntersectionObserver adding reveal classes to many elements, `animation-timeline: view()`, `data-split` or SplitText on headings. Take a screenshot without scrolling: any text that is missing or faded fails.
- Exceptions: one considered sequence on a landing page, with a reduced-motion alternative.

### D-51 · Bounce and elastic easing · medium

- What: springs, bounces and elastic overshoot on UI elements.
- Why: it feels toy-like and slows interaction.
- Bad → good: `cubic-bezier(0.68,-0.55,0.27,1.55)` → an ease-out such as `cubic-bezier(0.16,1,0.3,1)`, 150–300ms for state changes.
- Detect: `bounce`, `elastic`, `wobble` in names, `animate-bounce`, `cubic-bezier` with a y value below 0 or above 1.
- Exceptions: playful brands and games, used rarely.

### D-52 · Hover that changes structure · medium

- What: hovering adds a border, a new container or padding, moves neighbours, or loses the element's border.
- Why: it shifts layout and looks broken.
- Bad → good: submenu item that gains a bordered box on hover → change of colour or background in the same box.
- Detect: `:hover` rules that change `border-width`, `padding`, `margin` or `width`. Review the hover state of every interactive element.
- Exceptions: none.

### D-53 · Animating layout properties · low

- What: transitions on `width`, `height`, `padding`, `margin`, `top`, `left` or `letter-spacing`.
- Why: they cause reflow and jank.
- Bad → good: `transition: width .3s` → animate `transform` and `opacity`.
- Detect: `transition` or keyframes that name layout properties, `transition-all` on large components.
- Exceptions: small accordions where the height must animate and there is no alternative.

### D-54 · Infinite decorative motion · medium

- What: pulsing status dots, blinking cursors, marquees, spinning rings, auto-playing carousels that nobody asked for.
- Why: constant motion pulls attention from content and costs battery.
- Bad → good: a pulsing "live" dot on a static page → a static dot, or none.
- Detect: `animation: … infinite`, `animate-pulse`, `animate-ping`, `animate-spin` outside loading states, `<marquee>`.
- Exceptions: real loading and recording indicators.

### D-55 · Modal by default · medium

- What: dialogs for content that could live on the page (details, forms, confirmations for reversible actions).
- Why: modals interrupt, break the back button and hide context.
- Bad → good: a modal to edit a single field → inline editing, or a dedicated page for long forms. Undo instead of "Are you sure?" for reversible actions.
- Detect: count of `Dialog`/`Modal` components, `role="dialog"`.
- Exceptions: destructive or blocking decisions.

### D-56 · No reduced-motion alternative · medium

- What: motion with no `prefers-reduced-motion` handling, or handling that simply kills all transitions.
- Why: motion can make people sick, and an abrupt kill breaks state changes.
- Bad → good: keep opacity changes and remove movement under `prefers-reduced-motion: reduce`.
- Detect: animation code with no `prefers-reduced-motion` in the project.
- Exceptions: none.

### D-57 · Hover effects on every card · low

- What: every card lifts, scales (1.03–1.05) or casts a bigger shadow on hover, including cards that are not links. Images zooming inside cards.
- Why: hover should signal that something is clickable. On everything it signals nothing.
- Bad → good: `hover:scale-105 hover:shadow-xl` on every card → a hover state only on clickable items, as a colour or underline change.
- Detect: `hover:scale-*`, `hover:-translate-y-*`, `:hover { transform: scale(` on non-link elements.
- Exceptions: none worth listing.

### D-58 · Cursor and scroll gimmicks · medium

- What: a custom cursor that follows the pointer (a dot with `mix-blend-mode: difference`), a reading-progress bar pinned to the top, a logo marquee that scrolls forever, and a floating chat button stacked on a sticky header and a bottom bar.
- Why: they are the stock "premium" add-ons of portfolio and agency templates. A custom cursor hides the system pointer and lags behind it, a progress bar on a landing page measures nothing the reader cares about, and stacked fixed elements eat the viewport on mobile.
- Bad → good: a custom cursor, a progress line and a marquee of three media logos → the system cursor, no progress bar and the three logos in a static row.
- Detect: `cursor: none`, a fixed element with a `cursor`, `cursor-dot` or `cursor-follower` class, `animation-timeline: scroll()`, `scroll-progress` or `reading-progress` classes, more than two `position: fixed` elements on the page.
- Exceptions: long-form reading where a progress indicator answers "how much is left", drawing and game interfaces where the cursor is a tool.

## 8. Quality floor

### D-60 · Broken basics · medium

- What: touch targets smaller than 44×44px on mobile, focus outlines removed without a replacement, skipped heading levels, inputs below 16px on iOS (they trigger zoom), images without meaningful `alt`.
- Why: these are not style choices. They break use for real people.
- Bad → good: `outline: none` on buttons → a visible themed focus ring.
- Detect: `outline: none`/`outline-0` without a `focus-visible` style, heading order, control sizes.
- Exceptions: none.
