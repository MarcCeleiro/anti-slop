---
tags: [design]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

This note box on our documentation site looks off. Fix the CSS and return the corrected version.

```css
.note {
  border-left: 4px solid #7c3aed;
  background: linear-gradient(135deg, #f5f3ff, #ede9fe);
  box-shadow: 0 10px 30px rgba(124, 58, 237, 0.25);
  border-radius: 16px;
  padding: 24px;
}
.note-title {
  text-transform: uppercase;
  letter-spacing: 0.15em;
  font-size: 11px;
  color: #7c3aed;
}
```
