# Writing anti-patterns (all languages)

Patterns that make text read as generated or simply badly written, whatever the language. Load the file for the language of the text as well: `writing-ca.md`, `writing-es.md` or `writing-en.md`. They add word lists, calques and punctuation conventions, and their examples take priority when they conflict with the English examples here.

Each entry has the same fields as the other catalogs. Severity is a default.

None of these signs proves anything alone. Plain, careful human writing also uses a colon or a list now and then. What gives text away is the density and the combination, and what makes it bad is that the reader has to work harder. Fix the sentence, not the symptom: replacing every em dash with a colon creates W-12.

## Contents

1. Sentence construction: W-01 to W-07
2. Punctuation and rhetorical tics: W-10 to W-19
3. Voice and filler: W-20 to W-29
4. Headings and format: W-30 to W-39
5. Language and register: W-40 to W-44

## 1. Sentence construction

These are the most frequent problems and the first thing to check.

### W-01 · Comma splice · high

- What: two independent clauses, each with its own conjugated verb, joined only by a comma.
- Why: the reader cannot tell how the two ideas relate (cause, contrast, sequence). It is a top complaint about generated text in Romance languages, where the habit comes from English-trained models.
- Bad → good: "We already send the invoices by email, we would like to add a payment link." → "We already send the invoices by email and would now like to add a payment link." Or two sentences, or a connector that states the relation ("so", "but", "because").
- Detect: `detect.py` flags a comma followed by a subject pronoun or finite verb when the part before also has a finite verb and there is no conjunction or relative pronoun. Review question: "Could a full stop replace this comma?" If yes, it needs a connector or a full stop.
- Exceptions: very short parallel clauses in a series ("I came, I saw, I left"), dialogue, deliberate style in fiction.

### W-02 · Fragment standing in for a sentence · high

- What: verbless phrases used as sentences: bullet points, captions, subtitles and table notes that are only noun phrases. Also sentences cut in half ("Small sample. Online only.").
- Why: fragments force the reader to rebuild the missing verb and they sound like notes, not writing.
- Bad → good: "Weekends: closed." → "The office is closed at weekends." Bullet "Hosting, backups, monitoring" in a proposal → "We host the site, keep daily backups and monitor uptime."
- Detect: lines or bullets with three or more words and no conjugated verb, in running text. Review captions and subtitles one by one.
- Exceptions: headings, labels, table cells, form fields and short lists of items (ingredients, features in a spec), where noun phrases are the norm.

### W-03 · Choppy chain · high

- What: a run of short sentences with no connectors between them, so the text advances in jolts. "We tested it. It works. It is fast. You will like it."
- Why: models overcorrect long sentences into staccato. The logic between the ideas disappears and the tone becomes curt or dramatic.
- Bad → good: "The library opens at nine. Not on Saturdays. The café does." → "The library opens at nine on weekdays and is closed on Saturdays, but the café is open every day."
- Detect: three or more consecutive sentences of six words or fewer in the same paragraph.
- Exceptions: instructions where each step is a sentence, deliberate rhythm used once for effect.

### W-04 · Missing or wrong connector · high

- What: ideas placed side by side without "because", "so", "but", "although", "which", or with a connector that states the wrong relation ("however" where there is no contrast, "therefore" where nothing follows).
- Why: connectors carry the reasoning. Without them the reader has to guess, with the wrong one they get misled.
- Bad → good: "The order arrived late. The warehouse moved in March." → "The order arrived late because the warehouse moved in March."
- Detect: review question per paragraph: "What is the relation between sentence 1 and sentence 2, and does the text say it?"
- Exceptions: lists of independent facts.

### W-05 · Compressed sentence · high

- What: a sentence that packs so much (or leaves so much implicit) that it has to be decoded. "Returns 30 days, 15 if on sale."
- Why: compression saves words for the writer and costs time for the reader. In UI it causes mistakes.
- Bad → good: "Returns 30 days, 15 if on sale." → "You can return an item within 30 days of delivery. Sale items have 15 days."
- Detect: review question: "Would someone new understand this on first read without context?" Read it aloud.
- Exceptions: none.

### W-06 · Noun pile · medium

- What: two or three noun phrases stacked with "and" or "of" without a verb, typically in titles and subtitles. "Report of incidents and list of contacts of each area."
- Why: the reader cannot tell what the text is about or what to do. It sounds like a database field.
- Bad → good: "Monthly incidents and per-area contacts" → "See this month's incidents" (or "Each area has its own contacts").
- Detect: titles and labels with two "and"/"of" joins and no verb, more than five words long.
- Exceptions: navigation labels and table headers that name a known object.

### W-07 · Dangling or misattached clause · medium

- What: a participle or subordinate clause that attaches to the wrong subject or hangs at the end. "Having reviewed the logs, the error is clear."
- Why: it is grammatically wrong in most languages and confusing in all of them.
- Bad → good: "Having reviewed the logs, the error is clear." → "After reviewing the logs, we found the error."
- Detect: sentences that open with a participle or gerund followed by a subject that cannot perform it.
- Exceptions: none.

## 2. Punctuation and rhetorical tics

### W-10 · Semicolon as style · high

- What: semicolons used to join clauses for rhythm, especially in parallel structures ("Mondays are for planning; Fridays, for reviews").
- Why: in everyday prose, emails and UI text the semicolon is rare. Even one reads as a generated tell, and many readers find it stiff.
- Bad → good: "The upload failed twice; the file was too large." → "The upload failed twice because the file was too large."
- Detect: any `;` in prose (outside code, citations and formulas).
- Exceptions: complex lists whose items contain commas, legal and academic text that follows its own conventions.

### W-11 · Em dash and middle dot as separators · high

- What: the em dash (—) used as a pause, for asides or for dramatic reveals, and the spaced middle dot ( · ) used to string pieces together in subjects, titles, labels, metadata and running text.
- Why: the em dash is the most cited generated tell of 2023–2026, and the spaced middle dot is its sibling in subjects and labels. Readers who have learnt to spot them stop trusting the text at the first one, so density no longer matters.
- Bad → good: "The result — after weeks of testing — was clear." → "After weeks of testing, the result was clear." "MOOC v2 · Staging ready for review" → "MOOC v2 staging ready for review".
- Detect: any em dash in prose, any spaced en dash used the same way, any spaced middle dot.
- Exceptions: dialogue in Catalan and Spanish fiction, ranges with an en dash ("2023–2026"), a proper name that contains one, the Catalan ela geminada (l·l).

### W-12 · Colon hinge · medium

- What: colons used as a reveal inside sentences ("The answer is simple: we build it"), and label-colon openings ("Key point:", "Result:", "The catch:").
- Why: the colon does the work a verb or connector should do. It turns every paragraph into a setup and a payoff.
- Bad → good: "Our goal is clear: faster pages." → "We want the pages to load faster." "Result: a 30% drop." → "The bounce rate dropped by 30%."
- Detect: a colon followed by a lowercase clause in running prose, and lines that begin with one to three words plus a colon.
- Exceptions: introducing a list or a quotation, times and ratios, structured fields such as "Date: 3 May", greetings in Spanish letters ("Estimado Juan:").

### W-13 · Negative parallelism · high

- What: "It's not X, it's Y", "not only X but also Y", "not just X, but Y", "no X, no Y, just Z", "Y rather than X" as a framing device.
- Why: it argues with a claim nobody made. It is one of the most repeated generated structures in every language.
- Bad → good: "It's not just an app, it's a new way to look after your garden." → "The app reminds you when to water each plant."
- Detect: the regex families in `detect.py` for each language (`not (just|only) … but`, `no és … és`, `no solo … sino`).
- Exceptions: a real correction of a real misunderstanding ("It is not free. It costs 5 € per month.").

### W-14 · Bold-label bullets · medium

- What: bullet lists where each item starts with a bold term and a colon followed by a fragment. "**Speed:** faster pages."
- Why: it is the default output format of chat assistants. The bold labels repeat what the fragment says and the fragments lack verbs (W-02).
- Bad → good: "- **Hosting:** managed servers" → a sentence: "We host the site on managed servers and keep daily backups."
- Detect: three or more list items that start with `**…**:` or `<strong>…</strong>:`.
- Exceptions: glossaries, specs and reference catalogs where every item has the same fields.

### W-15 · Rhetorical questions and question labels · medium

- What: questions the text immediately answers ("What does this mean for you? It means…"), and headings or labels phrased as questions ("Where does the data come from?" over a single sentence).
- Why: it is a staged dialogue. The reader wanted the answer, not the question.
- Bad → good: "So, why does this matter? Because…" → state the reason.
- Detect: a question mark in running prose followed by a sentence that answers it, question headings over short sections.
- Exceptions: FAQ pages, where questions are the real interface. That holds only for questions customers actually ask. "Why should I choose a local supplier?" is a pitch dressed as a question.

### W-16 · Default triads · medium

- What: groups of three adjectives, nouns or clauses used by reflex ("fast, secure and scalable"; "clear, concise and compelling"), and three-beat headings ("One studio. Three crafts."). The hero version stacks one word per line, each with its own full stop ("Ideas. Craft. Care." "Plan it. Build it. Grow it."), and the section version names three verbs ("Listen, design, deliver").
- Why: three items sound complete, so generators produce three whether or not there are three things to say.
- Bad → good: "a modern, intuitive and powerful dashboard" → name the one property that matters, with a fact: "a dashboard that loads every invoice in under a second".
- Detect: review question: "Are there really three, and does each add something?" `detect.py` flags three-fragment headings separated by full stops.
- Exceptions: real lists of three.

### W-17 · Punchline closer · medium

- What: a short, quotable line at the end of a paragraph that restates it as a maxim ("And that makes all the difference." "Simple as that.").
- Why: it is an ending formula. It adds nothing and sounds like an advert.
- Bad → good: delete it. If the paragraph needs a conclusion, make it concrete.
- Detect: final sentences of six words or fewer that contain no new information.
- Exceptions: speeches and slogans written as such.

### W-18 · Reflex caveat tail · medium

- What: a short correction clause glued to the end of statements and captions, saying what the thing is not ("These are estimates, not a guarantee." "Weekdays only, never holidays." "Retail price, not trade price." "Shot on a phone, no filters."). On generated pages it appears under almost every figure.
- Why: one caveat where a reader could misread the data is precision. A caveat on every line is a tic: it argues with objections nobody raised, buries the caveats that matter and makes the page sound defensive.
- Bad → good: "Average wait at each clinic. Estimated, not measured." → keep the caveat only where a wrong reading is likely and costly, and state it once in the methods note.
- Detect: sentences that end in a comma plus "not", "never" or "no" and a short noun phrase (`, not a…`, `, no una…`, `, mai un…`, `, no un…`, `, nunca…`). Three or more in a file is the signal.
- Exceptions: legal and safety notices, a single methodological warning next to the figure it qualifies.

### W-19 · Quotation marks as habit · high

- What: angled quotes « » and curly quotes “ ” wrapped around button names, labels, titles, product names, terms and scare quotes.
- Why: people rarely type typographic quotes, and almost never around every name they mention. A paragraph with several pairs of « » or “ ” reads as generated at once, in any language.
- Bad → good: "Clica «Desa» i torna a «Cursos»." → "Clica Desa i torna a Cursos." "We created the “PROVA v2” course." → "We created a test course."
- Detect: any « » or “ ” in prose. Two pairs or more in one paragraph is a clear tell.
- Exceptions: a real quotation of someone's words, where plain straight quotes are enough, code and data.

## 3. Voice and filler

### W-20 · Restating and recap · medium

- What: summaries that repeat what was just said ("In short…", "To sum up…"), the same notice repeated in several sections, an intro that announces the content and an outro that repeats it.
- Why: repetition doubles the length and implies the reader did not understand.
- Bad → good: a note about the data source repeated under every chart → say it once where it first applies.
- Detect: sentences or phrases that appear more than once (`detect.py` flags repeated sentences), closing paragraphs that start with a summary connector.
- Exceptions: long reports with an executive summary meant to be read alone.

### W-21 · Empty openers and closers · high

- What: "Great question", "I hope this email finds you well", "I hope everything is fine", "Don't hesitate to contact us", "Let me know if you have any questions", "Hope this helps".
- Why: they fill the first and last lines, which are the ones people read. They are also strong chatbot residue.
- Bad → good: "I hope this email finds you well. I'm writing to ask…" → "Could you send us…?"
- Detect: per-language lists in `detect.py`.
- Exceptions: a real apology for a real delay, said once and concretely ("Sorry for answering a week late").

### W-22 · Inflated or cheerleading tone · medium

- What: enthusiasm the situation does not call for ("We're thrilled to…", "Amazing!"), celebration emojis, every outcome described as exciting.
- Why: it sounds like marketing and lowers trust, especially in professional correspondence.
- Bad → good: "We're absolutely delighted to share this exciting news!" → "The project has been approved."
- Detect: exclamation marks in professional text, adjectives of excitement.
- Exceptions: personal messages where warmth is the point.

### W-23 · Defining by negation · medium

- What: describing something by what it is not or by a non-event ("Testing is never an afterthought", "No surprises", "Nothing is left to chance").
- Why: it raises a worry the reader did not have and hides the actual fact.
- Bad → good: "Testing is never an afterthought." → "We test every page as soon as it is built."
- Detect: sentences whose main verb is negated and that contain no concrete fact.
- Exceptions: real constraints ("We do not store card numbers").

### W-24 · Effect phrases and unverifiable warmth · medium

- What: metaphors and set phrases used for effect ("the heart of the matter", "a breath of fresh air"), intensifiers that add nothing ("real", "truly", "genuinely", "really useful"), and cute promises nobody can check ("our door is always open", "so you can rest easy").
- Why: they sound written for effect, and the promises can come across as presumptuous or false.
- Bad → good: "Truly fast pages" → "Pages that load in under two seconds". "Our door is always open" → "Write to us at hello@… and we reply within a working day".
- Detect: per-language intensifier lists. Review question: "Is this phrase a fact, or decoration?"
- Exceptions: a voice that is deliberately playful, agreed with the owner.

### W-25 · Describing the visual literally · low

- What: text that narrates the design ("Three blue circles form a leaf", "the blue card on the left shows…").
- Why: the reader can see it. Describing design elements sounds like a model explaining its own output.
- Bad → good: "Three blue circles form a leaf that grows towards the light." → explain what the logo stands for, or say nothing.
- Detect: sentences with colour names, hex codes or shapes as subject.
- Exceptions: alt text, accessibility descriptions, design specifications.

### W-26 · Signposting · medium

- What: announcing what the text is about to do ("Let's dive in", "Here's what you need to know", "Below we explain", "Let's take a look").
- Why: it delays the content and is a chatbot habit.
- Bad → good: "Let's take a closer look at the results." → present the results.
- Detect: per-language lists.
- Exceptions: long technical documents that need a navigation sentence.

### W-27 · Text about the text · medium

- What: copy that talks about itself or its own structure ("Two methods and an example, side by side", "What this guide covers, chapter by chapter"), and internal notes that reach the public version ("subject to validation", "TODO", "as discussed internally").
- Why: the reader sees the scaffolding and the writer's doubts instead of the content.
- Bad → good: "Two methods and an example, side by side" → title the section "Methods" and present each one.
- Detect: words such as "this document", "this section", "below", "subject to", "TBD", "to be confirmed" in public copy.
- Exceptions: legal documents that refer to their own clauses.

### W-28 · Hedging and stacked qualifiers · low

- What: "might potentially", "could possibly", "it is important to note that", "generally speaking", several qualifiers in one sentence.
- Why: it makes every claim weak and adds length.
- Bad → good: "It may potentially help to improve performance in some cases." → "It cuts load time on mobile by about a third."
- Detect: per-language lists of hedges.
- Exceptions: scientific claims that really are uncertain, with the uncertainty stated once.

### W-29 · Inflated vocabulary · medium

- What: the words generators over-use: in English "delve", "tapestry", "seamless", "robust", "leverage", "pivotal", "underscore", "testament", "landscape"; and their equivalents in each language ("potenciar", "sense fissures", "crucial", "fonamental"; "potenciar", "sin fisuras", "crucial").
- Why: they are vague and, in clusters, a well-known tell.
- Bad → good: "We leverage robust tools to deliver a seamless experience." → "The site loads in under two seconds on mobile."
- Detect: per-language lists in the `writing-*.md` files and in `detect.py`.
- Exceptions: technical meanings ("robust statistics", "leverage" in finance).

## 4. Headings and format

### W-30 · Comma-tag heading · high

- What: a heading made of a noun phrase plus a comma and a short adverbial tag. "The project, phase by phase." "The menu, dish by dish." "Two offices, one team." "The app, in detail."
- Why: it is a telegraphic magazine formula that generators reuse for every subtitle. It does not say what the section contains.
- Bad → good: "The project, phase by phase" → "Project phases". "The app, in detail" → "App features".
- Variant: the count formula "12 recipes, one ingredient each", "40 courses, each with its teacher", "6 routes, each with its own map". When several headings on one page share the formula, the page reads as filled from a template.
- Detect: headings with a comma whose second part has no verb and four words or fewer. Distributive tags ("one by one", "step by step", "phase by phase", "each", "cadascun", "cada uno" and their translations) are flagged as high, as are two or more headings that start with a number followed by a comma tag.
- Exceptions: names and places ("Paris, Texas"), dates.

### W-31 · Slogan heading · high

- What: section titles written as a punchline or a sentence ("Everything you need is already here", "What your team gains with…", "Built for what's next").
- Why: headings are for scanning. A slogan hides the topic and sounds like an advert.
- Bad → good: "What your team gains with the new tool" → "Benefits". "Everything is ready" → "Project status". Card and column subtitles follow the same rule: the topic in two or three words ("Delivery times", "Payment options"), not a verdict ("Slower than it should be", "Ready to go").
- Detect: headings of more than six words, headings with a finite verb, headings ending in an ellipsis or exclamation mark. Review question: "Could this heading be a short noun label?"
- Exceptions: article headlines and marketing hero lines, which can be sentences when written on purpose. Even there, avoid the empty grandiose slogan and the bare category label; describe what is offered. Two hero formulas to avoid in particular: the split of roles ("You dream it. We build it.") and the imperative chain ("Find a plan, compare it and switch today.").

### W-32 · Title Case where the language uses sentence case · medium

- What: capitalising every main word in headings ("Frequently Asked Questions", "Preguntes Freqüents") in languages and style guides that use sentence case.
- Why: Catalan and Spanish only capitalise the first word and proper nouns. Even in English, most modern style guides and interfaces use sentence case.
- Bad → good: "Preguntes Freqüents" → "Preguntes freqüents". "Our Services And Pricing" → "Services and pricing".
- Detect: headings in Catalan or Spanish with two or more capitalised words after the first that are not proper nouns or acronyms.
- Exceptions: proper nouns, titles of works in English, brand style guides that require Title Case.

### W-33 · Numerals and counts where words belong · medium

- What: digits for small counts in running text and headings ("2 things to know before you visit", "3 key benefits"), especially when the count adds nothing.
- Why: the count is filler and the digit makes the sentence look like a generated list title.
- Bad → good: "2 things to know before you visit the museum" → "The museum closes early on Fridays" (say what the thing is).
- Detect: a digit from 1 to 9 followed by "thing(s)", "tip(s)", "way(s)", "key", "reason(s)" and translations.
- Exceptions: data, prices, times, steps in a procedure, UI badges that show counts.

### W-34 · Generic label headings · medium

- What: headings that could sit on top of any content: "Things to keep in mind", "Key takeaways", "Overview", "Important information", "Final thoughts", "Additional considerations".
- Why: they do not tell the reader what is inside.
- Bad → good: "Things to keep in mind" → "Opening hours change in August".
- Detect: per-language lists.
- Exceptions: standard document parts ("Summary" in a report template, "Contact").

### W-35 · Bullets where prose belongs · medium

- What: reasoning, narratives and explanations broken into bullet points.
- Why: bullets drop the connectors (W-04) and the argument falls apart into assertions.
- Bad → good: a diagnosis written as eight bullets → three paragraphs that tell what happened, why, and what to do.
- Detect: lists whose items are full arguments or depend on each other, documents where bullets outnumber paragraphs.
- Exceptions: steps, checklists, inventories, options.

### W-36 · Over-structuring · low

- What: headings, sections and tables for an answer of a few sentences, or a table that holds one row.
- Why: structure makes short content longer and harder to read.
- Bad → good: a five-line email with two headings → five lines.
- Detect: headings in texts under about 150 words.
- Exceptions: templates the reader expects.

### W-37 · Scattered bold · medium

- What: several bold phrases per paragraph, bold on random key terms, bold in navigation and labels.
- Why: emphasis everywhere is emphasis nowhere and the page looks spotty.
- Bad → good: four bold fragments in a paragraph → none, or one for the single thing the reader must not miss.
- Detect: paragraphs with two or more bold spans, or bold in more than a third of paragraphs.
- Exceptions: reference documents where defined terms are bold once.

### W-38 · Decorative emoji · medium

- What: emoji at the start of headings or bullets, or at the end of sentences for tone ("🚀", "✨", "✅", "🎉").
- Why: in professional text they are a generated tell and they do not render the same everywhere.
- Bad → good: "🎉 Your account is ready!" → "Your account is ready."
- Detect: emoji in headings, bullets and professional emails.
- Exceptions: chat, social media, and brands that use them deliberately.

### W-39 · Repeated coda · medium

- What: the same justification or tagline repeated in every paragraph ("so that search engines can find you…", "to ensure a seamless experience"). It includes the brand mantra: a method or promise phrase that comes back in section after section ("made by people, for people", "every detail counts", "no jargon").
- Why: an argument works once. Repeating it sounds like a template.
- Bad → good: say it in the paragraph where it matters most and remove the others.
- Detect: repeated phrases of four or more words across paragraphs.
- Exceptions: legal clauses.

## 5. Language and register

### W-40 · Literal calque · high

- What: phrases translated word by word from English (or between Spanish and Catalan) that are not natural in the target language. "fa sentit" (from "makes sense"), "a nivell de", "en base a", "jugar un rol".
- Why: it is the clearest sign that text was generated or machine-translated, and in UI it can be incomprehensible.
- Bad → good: "Això fa sentit" → "Això té sentit".
- Detect: per-language lists of calques. Review question: "Would a native speaker say this?"
- Exceptions: established loanwords.

### W-41 · Register mix · medium

- What: switching between formal and informal address (tú and usted, tu and vostè, vous and tu) or between languages in the same product or document.
- Why: it looks careless and confuses the relationship with the reader.
- Bad → good: a site that uses "vostè" in pages and "tu" in the chat widget → one register everywhere.
- Detect: second-person pronouns and verb forms of both registers in the same project. Mixed languages in headings.
- Exceptions: quotations.

### W-42 · Copula avoidance · low

- What: "serves as", "stands as", "functions as", "boasts", "features" instead of "is" and "has".
- Why: inflated verbs for simple facts are a generated tell.
- Bad → good: "The library serves as a hub for the community." → "The library is the community's meeting place."
- Detect: per-language lists.
- Exceptions: none worth listing.

### W-43 · Participle tail · medium

- What: sentences that end with an "-ing" clause adding significance ("…, highlighting its importance", "…, ensuring a seamless experience") and the equivalent gerund tails in Catalan and Spanish.
- Why: the tail asserts a consequence with no evidence and the gerund often expresses posteriority, which is incorrect in Catalan and Spanish.
- Bad → good: "The museum reopened in May, marking a new era for the town." → "The museum reopened in May."
- Detect: comma plus an -ing verb from a list (highlighting, underscoring, ensuring, reflecting, marking, fostering) at the end of a sentence. Gerunds after a comma at the end of a sentence in Catalan and Spanish.
- Exceptions: gerunds of manner or simultaneity that are correct in the language.

### W-44 · Chatbot residue · high

- What: traces of the assistant conversation left in the deliverable: "Here is the revised version", "Certainly!", "As an AI", "I hope this helps", knowledge-cutoff notes, placeholders like `[Your Name]` or `2026-xx-xx`, Markdown symbols in a context that does not render Markdown, "utm_source=chatgpt.com".
- Why: it shows the text was pasted without reading.
- Bad → good: remove them all before delivery.
- Detect: lists in `detect.py`.
- Exceptions: none.
