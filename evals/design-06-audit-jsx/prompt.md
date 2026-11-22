---
tags: [design, audit]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

Review this component for the generic AI-generated look and tell me what to fix. Don't rewrite it yet.

```jsx
export default function Hero() {
  return (
    <section className="py-24 text-center">
      <span className="text-xs uppercase tracking-widest text-indigo-500">✨ Introducing</span>
      <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-600 to-blue-500 bg-clip-text text-transparent">The future of team collaboration</h1>
      <p className="mt-6 text-gray-500">It's not just a tool — it's a whole new way of working.</p>
      <div className="mt-12 grid grid-cols-3 gap-6">
        {features.map(f => (
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} className="rounded-2xl border bg-white p-6 shadow-lg">
            <div className="rounded-xl border p-4 bg-gray-50">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100">{f.emoji}</div>
              <h3 className="mt-4 font-semibold">{f.title}</h3>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
```
