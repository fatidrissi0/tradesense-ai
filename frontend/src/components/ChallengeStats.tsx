export default function ChallengeStats() {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900/30">
      <h2 className="mb-2 text-sm font-semibold text-slate-700 dark:text-slate-200">
        Statistiques Challenge
      </h2>
      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-lg bg-slate-50 p-3 dark:bg-slate-950/40">
          <div className="text-slate-500 dark:text-slate-400">P&L</div>
          <div className="font-semibold">+0.00%</div>
        </div>
        <div className="rounded-lg bg-slate-50 p-3 dark:bg-slate-950/40">
          <div className="text-slate-500 dark:text-slate-400">Trades</div>
          <div className="font-semibold">0</div>
        </div>
      </div>
    </section>
  );
}

