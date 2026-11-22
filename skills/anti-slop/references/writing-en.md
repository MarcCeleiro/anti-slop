# Writing anti-patterns: English

Load with `writing.md` when the text is in English. The general rules (W-xx) still apply. This file adds the English word lists and the patterns specific to English (EN-xx). English has the best public documentation of AI-writing tells, mainly the Wikipedia guide "Signs of AI writing" (see `sources.md`).

Word lists drift. Models trained to avoid "delve" and the em dash move to new favourites, so look at clusters and at the reader's effort rather than at single words.

### EN-01 · Inflated vocabulary · medium

- What: words that are statistically over-used by models compared with human writers.
  - Classic set (2023 onwards): delve, tapestry, testament, pivotal, crucial, intricate, intricacies, interplay, meticulous(ly), underscore, landscape (figurative), realm, vibrant, bustling, boasts, garner, bolster, enduring, showcase, foster, enhance, align with, resonate with, valuable insights, robust, seamless(ly), leverage, holistic, synergy, multifaceted, navigate (figurative), embark, journey (figurative), elevate, empower, unlock, harness, transformative, cutting-edge, game-changer, ever-evolving, nestled, in the heart of, a myriad of, a plethora of.
  - Newer favourites (2025–2026): quietly, steady, practical, dependable, clearer, matters, echoed, prioritize, universally.
- Why: they are vague, and several in one text are a strong signal.
- Bad → good: "This pivotal update underscores our commitment to a seamless experience." → "This update fixes the checkout bug on Safari."
- Detect: list in `detect.py` (`EN-01`). Flag clusters (two or more per paragraph) higher than single hits.
- Exceptions: technical meanings (robust statistics, financial leverage, a real landscape).

### EN-02 · Marketing buzzwords · high

- What: "empower your team", "supercharge", "unleash the power of", "transform your business", "revolutionize", "best-in-class", "world-class", "industry-leading", "enterprise-grade", "next-generation", "future-proof", "mission-critical", "trusted by leading companies", "built for the modern…", "drive growth", "take it to the next level".
- Why: interchangeable claims that fit any product, the copy equivalent of D-34.
- Bad → good: "Supercharge your workflow with our next-generation platform." → "Invoices go out automatically on the first of the month."
- Detect: list in `detect.py` (`EN-02`).
- Exceptions: none in product copy.

### EN-03 · Throat-clearing and filler openers · medium

- What: "Here's the thing", "The truth is", "Let me be clear", "It turns out", "In today's fast-paced world", "In a world where", "When it comes to", "At its core", "At the end of the day", "It's worth noting that", "It is important to note that", "Moving forward", "Needless to say".
- Why: W-21 and W-26 in English.
- Detect: list in `detect.py`.
- Exceptions: speech transcripts.

### EN-04 · Softener and intensifier adverbs · low

- What: really, just, literally, genuinely, honestly, simply, actually, deeply, truly, fundamentally, inherently, incredibly, importantly, crucially, interestingly.
- Why: they add emphasis without content.
- Detect: frequency per paragraph (`EN-04`).
- Exceptions: when the adverb changes the meaning ("only", "just" meaning recently).

### EN-05 · Significance inflation · medium

- What: "stands as a testament to", "plays a pivotal role in", "underscores the importance of", "marks a turning point", "sets the stage for", "leaves an indelible mark", "deeply rooted in", "reflects a broader trend", "a rich tapestry of".
- Why: it inflates ordinary facts and asserts importance without evidence.
- Bad → good: "The bridge stands as a testament to the town's enduring spirit." → "The bridge was rebuilt in 1952 after the flood."
- Detect: list in `detect.py` (`EN-05`).
- Exceptions: none worth listing.

### EN-06 · Vague attribution · medium

- What: "experts say", "studies show", "industry reports suggest", "observers have noted", "many believe".
- Why: it borrows authority without a source.
- Bad → good: name the source or drop the claim.
- Detect: list in `detect.py` (`EN-06`).
- Exceptions: none.

### EN-07 · Title Case in interface and headings · low

- What: "Our Services And Pricing", "Get Started Today".
- Why: most modern style guides and products use sentence case for headings, buttons and menus.
- Detect: `W-32` in `detect.py` checks Catalan and Spanish only by default, since English Title Case can be a house style. Review English headings by hand.
- Exceptions: titles of works, house styles that require it.

### EN-08 · Dash and quote habits · low

- What: spaced em dashes used as all-purpose pauses (W-11), and straight and curly quotes mixed in the same text.
- Why: density of dashes is the most quoted tell, and mixed quotes look unedited.
- Detect: em dash density (`W-11`).
- Exceptions: one house style applied consistently.

### EN-09 · Generic UI strings · medium

- What: "Submit", "OK", "Yes/No" for decisions, "Click here", "Learn more" on every card, "Oops! Something went wrong", "Uh-oh", apologetic or cute error messages, "Are you sure?" on reversible actions.
- Why: labels should say what happens and errors should say what failed and how to fix it.
- Bad → good: "Submit" → "Send request". "Oops! Something went wrong." → "We couldn't save the draft. Check your connection and try again."
- Detect: list in `detect.py` (`EN-09`).
- Exceptions: none.

### EN-10 · Uniform sentence length · low

- What: paragraphs where every sentence has 8 to 20 words and the same shape (subject, verb, object, comma, tail). This is a newer tell from models tuned to avoid long sentences and dashes.
- Why: monotone rhythm, even when each sentence is correct.
- Bad → good: vary length with the logic. Join related ideas with connectors (W-04) and keep short sentences for emphasis.
- Detect: review question: read the paragraph aloud.
- Exceptions: instructions.
