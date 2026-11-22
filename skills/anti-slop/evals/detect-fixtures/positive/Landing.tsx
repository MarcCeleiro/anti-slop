// expect: D-02 D-03 D-12 D-13 D-20 D-21 D-45 D-46 D-50 D-54 D-60 W-13 EN-02 C-02 C-04 D-14 W-01
export function Landing() {
  return (
    <section className="py-24">
      <p className="eyebrow uppercase tracking-widest text-xs text-gray-500">Features</p>
      <h1 className="bg-gradient-to-r from-purple-600 to-blue-500 bg-clip-text text-transparent">Supercharge your workflow</h1>
      <p>It's not just a tool, it's a whole new way of working with your team.</p>
      <div className="rounded-xl border p-6 shadow-sm">
        <div className="rounded-lg border p-4 bg-white">Nested card content goes here for testing.</div>
      </div>
      <div className="border-l-4 border-indigo-500 pl-4">Quote from Jane Smith at Globex about our service.</div>
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100">🚀</div>
      <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }}>Animated block of marketing text</motion.div>
      <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
      <img src="/hero.png" />
      <a href="/a">Learn more</a>
      <a href="/b">Learn more</a>
      <a href="/c">Learn more</a>
    </section>
  );
}
