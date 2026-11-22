---
tags: [design, negative]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

Polish this stylesheet if it needs it. If it is already fine, say so.

```css
:root { --ink: #1f2328; --muted: #59636e; --accent: #0b6e4f; --space: 1rem; }
body { font: 1.0625rem/1.6 "Source Serif 4", Georgia, serif; color: var(--ink); background: #fff; max-width: 68ch; margin: 0 auto; padding: var(--space); }
h1 { font-size: 2.25rem; line-height: 1.15; margin-bottom: calc(var(--space) * 1.5); }
h2 { font-size: 1.5rem; margin-top: calc(var(--space) * 2.5); }
a { color: var(--accent); }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.meta { color: var(--muted); font-size: 0.875rem; }
```
