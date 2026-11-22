# Content anti-patterns

Patterns in what is said, as opposed to how it is said (`writing.md`) or how it looks (`design.md`). Generated content tends to fill every slot of a template with plausible material. The rule underneath all of these: if a sentence, number or element could be swapped for random text without anyone noticing, it should not be there.

## Contents

C-01 to C-15

### C-01 · Invented numbers · high

- What: statistics, percentages, counts and metrics that nobody supplied ("Trusted by 10,000+ teams", "98% satisfaction", "3x faster").
- Why: they are false, and readers who check will distrust everything else.
- Bad → good: "Join 10,000+ happy customers" → leave it out, or use the real figure with its source.
- Detect: numbers with "+", "%", "x" in marketing copy. Review question: "Where does this number come from?" If there is no answer, remove it.
- Exceptions: figures provided by the owner, with a date or source.

### C-02 · Invented people, quotes and logos · high

- What: testimonials, names, job titles, avatars and client logos that are made up. Placeholder identities such as "Acme", "Globex", "John Doe", "Jane Smith", "Sarah Chen", "Alex Johnson", "Lorem Corp".
- Why: they are false and often recognisable as placeholders.
- Bad → good: a testimonial from "Sarah Chen, CTO at Acme" → no testimonial section until there are real ones, or a clearly marked placeholder in a draft that will not ship.
- Detect: list of placeholder names and companies in `detect.py` (`C-02`).
- Exceptions: documentation examples marked as fictional.

### C-03 · Empty value proposition · high

- What: headlines and intros that say nothing specific. "Empower your team with our innovative platform." "Solutions that make a difference." "Your partner for digital transformation."
- Why: any company could sign them, so they tell the reader nothing.
- Bad → good: "Empower your business with smart solutions" → "Booking software for physiotherapy clinics. Patients book and pay online."
- Detect: review question: "Would this sentence fit a competitor's site unchanged?" Buzzword lists (EN-02, CA-01, ES-01).
- Exceptions: none.

### C-04 · Generic and repeated calls to action · medium

- What: "Get started", "Learn more", "Contact us" repeated on every section, CTAs that do not say what happens, placeholder pages that promise vaguely ("Coming soon! Stay tuned for exciting news!").
- Why: repetition dilutes the main action, and vague promises sound empty.
- Bad → good: three "Learn more" buttons → one CTA per page that names the result ("Book a visit"). A placeholder page: "This page will list the course dates. The calendar will be published in September."
- Detect: identical CTA strings appearing three or more times.
- Exceptions: navigation patterns.

### C-05 · Filler sections · high

- What: sections and points that exist because the template has a slot: "Our values", "Why choose us", "Future outlook", "Challenges", obvious steps in an action plan, absurd or redundant recommendations.
- Why: they bury the useful parts and make the document longer.
- Bad → good: an eight-point action plan where three points are "keep plugins updated" (already done) → the three points that change something.
- Detect: review question per section: "What would the reader lose without it?"
- Exceptions: required sections in formal templates (tenders, legal documents).

### C-06 · Explaining the obvious · high

- What: microcopy and sentences that describe what the reader already sees or will discover by acting: "Below you will find the data you submitted", "If you reply to this email, your reply will reach the sender", a description under a table that restates its column names, helper text that repeats the label.
- Why: it adds reading time and sounds like the system talking to itself.
- Bad → good: an internal notification with three explanatory lines → the title and the data. An acknowledgement email → one sentence: "We have received your request and will contact you."
- Detect: sentences that start with "Below", "Here you can", "This section", "If you…, …", helper text that repeats its label.
- Exceptions: instructions for a non-obvious action.

### C-07 · Internal notes in public text · high

- What: drafting notes, doubts and internal facts that reach the published version: "subject to validation", "TBD", "feature not yet enabled", "as agreed internally", names of internal tools, the model or the assistant.
- Why: it exposes the process and undermines trust.
- Bad → good: a user manual that says "this option is not active yet" → describe what is available, keep the roadmap internal.
- Detect: list in `detect.py` (`C-07`): TODO, TBD, FIXME, "to be confirmed", "subject to validation", "lorem ipsum", "placeholder".
- Exceptions: changelogs and roadmaps meant to be public.

### C-08 · Generic mockups and stock as proof · medium

- What: device mockups with invented screens, stock photos of offices and teams, AI-generated illustrations used where the reader expects evidence of the real thing.
- Why: they promise something they do not show. See D-49 for the visual side.
- Bad → good: an invented dashboard on a laptop → a real screenshot with real (or anonymised) data.
- Detect: review question.
- Exceptions: concept work clearly labelled as such.

### C-09 · Unrequested additions · medium

- What: content the brief did not ask for: personal contact details, extra sections, signatures, disclaimers, a FAQ, social links, credits.
- Why: it can expose private data and it changes the scope.
- Bad → good: a report with the author's phone number added in the footer → only what the brief includes.
- Detect: compare the output with the request.
- Exceptions: none without asking.

### C-10 · Fake urgency and borrowed authority · medium

- What: countdowns, "Only 3 spots left", "As seen in", "Award-winning", "Experts agree", certifications nobody has.
- Why: manipulative when false, and recognisable even when true.
- Detect: review question: "Is it true and can we prove it?"
- Exceptions: real, verifiable facts.

### C-11 · The same information in several places · medium

- What: one fact repeated in the intro, the body, a callout and the conclusion. Duplicated entries in lists and directories.
- Why: it makes documents long and hard to maintain, and contradictions appear when one copy changes.
- Detect: repeated sentences (`W-20` in `detect.py`).
- Exceptions: summaries meant to be read alone.

### C-12 · Placeholder and lorem left in · high

- What: "Lorem ipsum", "[Your name]", "example.com", "123 Main Street", "(555) 555-0100", "2026-xx-xx", grey boxes where an image should be.
- Why: it ships unfinished work.
- Detect: list in `detect.py` (`C-12`).
- Exceptions: documentation examples.

### C-13 · Vague claims with no specifics · medium

- What: "We work with leading brands", "Years of experience", "A wide range of services", "High quality", "Tailored solutions".
- Why: unverifiable and interchangeable. A specific claim is stronger even when it is smaller.
- Bad → good: "Years of experience with public institutions" → "Since 2015 we have built the booking systems of 30 dental clinics."
- Detect: review question: "Which fact proves this?"
- Exceptions: none.

### C-14 · Inventory as content · medium

- What: the page lists what the builders produced instead of what the visitor can do: counts of views, tools, datasets, methods and languages ("300 screens", "45 integrations", "12 languages", "9 algorithms"), dated release notes on the home page ("New (03-04): two dashboards merged, five new filters…"), and every feature of the product given its own section until the home page runs to twenty sections.
- Why: it is how a generator reports its own work back, and it ends up on the page. The visitor cannot use a count of features, the dates age within weeks, and the one thing they came for drowns among the rest.
- Bad → good: a strip of five counts and a dated "what's new" paragraph → one sentence on what the product answers, an example of a real question, and a link to the changelog.
- Detect: review questions: "Does this number help the visitor decide or act?" "Will this sentence still be true next month?" Count the sections of the home page. More than eight is a signal.
- Exceptions: a changelog or release-notes page, a catalogue page whose job is to list everything.

### C-15 · Precision dump · medium

- What: real figures and method terms poured into marketing or summary text at a density the audience cannot read: correlation coefficients, confidence ranges, parameter values and named algorithms in a teaser ("r = 0.74; p < 0.001; n = 1,284", "AUC 0.91 with a 0.35 threshold", "2.3 M€ in the base case (−0.8 to 5.1)").
- Why: it is the over-correction of "be specific". Every number is true, so nothing tells the reader which one matters, and the jargon signals rigour instead of explaining the result.
- Bad → good: a teaser with eight figures and three method names → the finding in one sentence with its one key figure ("Customers who get a reminder miss half as many appointments."), and the method and ranges in the study itself.
- Detect: review question: "Which single figure would the reader remember?" More than three figures or one technical statistic per sentence outside a methods section is the signal.
- Exceptions: methods sections, papers, data tables and audiences that asked for the numbers.
