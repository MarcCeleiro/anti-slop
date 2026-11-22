export function Pricing({ plans }: { plans: Plan[] }) {
  const [open, setOpen] = useState<boolean>(false);
  return (
    <section className="mx-auto max-w-3xl px-4 py-16">
      <h2 className="text-3xl font-semibold">Prices</h2>
      <p className="mt-4 text-lg text-gray-700">Every plan includes hosting, daily backups and email support on working days.</p>
      <ul className="mt-8 divide-y">
        {plans.map((p) => (
          <li key={p.id} className="flex justify-between py-4">
            <span>{p.name}</span>
            <span>{p.price} € a month</span>
          </li>
        ))}
      </ul>
      <img src="/team.jpg" alt="The four people of the support team at their desks" />
      <button onClick={() => setOpen(true)} className="mt-8 rounded-md bg-emerald-700 px-4 py-2 text-white">Compare plans</button>
    </section>
  );
}
