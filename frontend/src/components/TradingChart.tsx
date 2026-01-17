import { useEffect, useRef } from "react";
import { createChart, type IChartApi } from "lightweight-charts";

type Candle = {
  time: string | number;
  open: number;
  high: number;
  low: number;
  close: number;
};

export default function TradingChart({
  title = "Graphique",
  data
}: {
  title?: string;
  data?: Candle[];
}) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      height: 320,
      layout: {
        background: { color: "transparent" },
        textColor: "#94a3b8"
      },
      grid: {
        vertLines: { color: "rgba(148, 163, 184, 0.12)" },
        horzLines: { color: "rgba(148, 163, 184, 0.12)" }
      }
    });
    chartRef.current = chart;

    const series = chart.addCandlestickSeries();
    const toUtcSeconds = (t: string | number) => {
      if (typeof t === "number") return Math.floor(t);
      const d = new Date(t);
      if (!Number.isNaN(d.getTime())) return Math.floor(d.getTime() / 1000);
      const s = t.slice(0, 10);
      const d2 = new Date(`${s}T00:00:00Z`);
      return Math.floor(d2.getTime() / 1000);
    };
    const input = data ?? [
      { time: "2026-01-01", open: 100, high: 110, low: 95, close: 105 },
      { time: "2026-01-02", open: 105, high: 112, low: 101, close: 109 },
      { time: "2026-01-03", open: 109, high: 115, low: 106, close: 111 },
    ];
    const normalized = input
      .map((c) => ({
        time: toUtcSeconds(c.time),
        open: c.open,
        high: c.high,
        low: c.low,
        close: c.close,
      }))
      .sort((a, b) => a.time - b.time);
    series.setData(normalized as any);

    const ro = new ResizeObserver(() => {
      if (!containerRef.current) return;
      chart.applyOptions({ width: containerRef.current.clientWidth });
    });
    ro.observe(containerRef.current);

    return () => {
      ro.disconnect();
      chart.remove();
      chartRef.current = null;
    };
  }, [data]);

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900/30">
      <h2 className="mb-3 text-sm font-semibold text-slate-700 dark:text-slate-200">
        {title}
      </h2>
      <div ref={containerRef} className="w-full" />
    </section>
  );
}
