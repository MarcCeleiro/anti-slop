# anti-slop

An Agent Skill that keeps generated interfaces and text from looking generated. It gives the model a catalog of concrete anti-patterns with IDs, a heuristic detector for files, and a review pass to run before anything is delivered. It covers design (CSS, Tailwind, components, slides), writing in English, Catalan and Spanish, and content (claims, sections, placeholders).

Examples of what it catches: boxes inside boxes, a thick coloured border on one side of a card, an eyebrow label above every heading, purple-to-blue gradients, fade-up on every section, comma splices, verbless fragments, headings such as "The project, phase by phase", headlines split into two colours, text that only appears on scroll, custom cursors, "It's not just X, it's Y", a "…, not a guarantee" caveat under every caption, word-by-word calques, invented testimonials, unsourced numbers and home pages that list everything the team built.

## What is in the repository

```
.claude-plugin/          plugin.json and marketplace.json (Claude Code plugin)
skills/anti-slop/
  SKILL.md               principles, workflow and the 20-item review checklist
  references/
    design.md            D-01 to D-60
    writing.md           W-01 to W-44, language-independent
    writing-ca.md        Catalan (CA-xx)
    writing-es.md        Spanish (ES-xx)
    writing-en.md        English (EN-xx)
    content.md           C-01 to C-15
    sources.md           attribution
  scripts/
    detect.py            heuristic detector, standard library only
    test_detect.py       regression test against the fixtures
  evals/detect-fixtures/ positive and negative files for the detector
evals/                   cases for `claude plugin eval` (outside skills/, as the runner requires)
```

Each catalog entry has the same fields: what the pattern is, why it hurts, a bad and a good example, how to detect it (regex, CSS property, Tailwind class or review question) and the legitimate exceptions.

## Installation

### As a Claude Code skill

Clone the repository and link the skill folder into your skills directory:

```bash
git clone https://github.com/MarcCeleiro/anti-slop.git ~/code/anti-slop
ln -s ~/code/anti-slop/skills/anti-slop ~/.claude/skills/anti-slop
```

For a single project, link or copy it into `<project>/.claude/skills/anti-slop` instead.

### As a Claude Code plugin

The repository is also a plugin marketplace:

```
/plugin marketplace add MarcCeleiro/anti-slop
/plugin install anti-slop@anti-slop
```

### Other tools

The skill is plain Markdown plus one Python script, so any agent that can read files can use it. Point the agent's instructions (for example `AGENTS.md`, a Cursor rule or a system prompt) at `skills/anti-slop/SKILL.md` and tell it to load the reference files that the skill lists for each kind of task.

### Making it the default

To apply it on every task, add a short note to your global instructions (for Claude Code, `~/.claude/CLAUDE.md`):

```markdown
## Anti-slop
Before delivering any UI or text, apply the anti-slop skill and run its review pass.
```

## Personal and project rules

The skill reads two optional files and gives them priority over its own catalog:

- `~/.claude/anti-slop.personal.md` for your own preferences across all projects (for example "never use semicolons" or "action labels in the imperative").
- `.anti-slop.md` at the root of a project for that project's rules, such as a brand that uses uppercase labels on purpose. Inside the project it wins over the personal file.

Keep personal data and client names in those files, not in the shared skill.

## Running the detector

```bash
python3 skills/anti-slop/scripts/detect.py src/ content/ --min-severity medium
python3 skills/anti-slop/scripts/detect.py README.md --json
python3 skills/anti-slop/scripts/detect.py --list-rules
```

It reads `.css .scss .html .tsx .jsx .vue .svelte .astro .md .mdx .txt` and reports `file:line: RULE [severity] message | excerpt`. The exit code is 1 when there are findings at or above `--fail-on` (default `high`), so it can run in CI. Language is detected per paragraph and can be forced with `--lang ca|es|en`.

To silence a line, add a comment with `anti-slop-ignore`, optionally followed by rule IDs (`anti-slop-ignore D-14`). `anti-slop-ignore-file` skips a whole file.

The detector is a heuristic. It finds suspicions, not verdicts, and it cannot see most structural problems (a box without a job, a flat hierarchy, filler sections). The review checklist in `SKILL.md` covers those.

Run its tests with:

```bash
python3 skills/anti-slop/scripts/test_detect.py
```

## Evaluations

`evals/` holds 36 cases for `claude plugin eval` (design, writing in three languages, content, and clean inputs that should be left alone). Each case has a prompt and LLM graders. To compare runs with and without the skill:

```bash
claude plugin eval . --runs 1 --no-publish
```

These are real model runs and cost money.

## Attribution

Several design rules are adapted from [Impeccable](https://github.com/pbakaus/impeccable) by Paul Bakaus (Apache License 2.0). Other ideas come from Anthropic's frontend-design skill and cookbook, the Wikipedia guide "Signs of AI writing", [stop-slop](https://github.com/hardikpandya/stop-slop) and [humanizer](https://github.com/blader/humanizer). Everything is reworded. See `NOTICE` and `skills/anti-slop/references/sources.md` for details.

## Licence

Apache License 2.0. See `LICENSE` and `NOTICE`.
