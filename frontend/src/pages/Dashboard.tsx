import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { marketAPI, tradingAPI } from "../services/api";
import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle, Play, Pause } from "lucide-react";
import TradingChart from "../components/TradingChart";
import { useTranslation } from "react-i18next";

interface LivePrice {
  price: number;
  change_percent: number;
  timestamp: string;
  currency?: string;
}

interface Signal {
  signal: "BUY" | "SELL" | "HOLD";
  confidence: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "low" | "medium" | "high";
  reason: string;
}

interface Challenge {
  id: number;
  status: "active" | "passed" | "failed";
  initial_balance: number;
  current_balance: number;
  profit_target: number;
  max_daily_loss_percent: number;
  max_total_loss_percent: number;
}

const internationalSymbols = ["AAPL", "TSLA", "BTC-USD", "ETH-USD", "MSFT", "GOOGL"];
const moroccoSymbols = ["IAM", "ATW", "BCP", "MNG", "SNEP"];

export default function Dashboard() {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [selectedSymbol, setSelectedSymbol] = useState("AAPL");
  const [livePrice, setLivePrice] = useState<LivePrice | null>(null);
  const [signal, setSignal] = useState<Signal | null>(null);
  const [challenge, setChallenge] = useState<Challenge | null>(null);
  const [chartData, setChartData] = useState<
    { time: string; open: number; high: number; low: number; close: number }[] | undefined
  >(undefined);
  const [quantity, setQuantity] = useState(1);
  const [isPolling, setIsPolling] = useState(true);
  const [isTrading, setIsTrading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [modalStatus, setModalStatus] = useState<"failed" | "passed" | null>(null);
  const [modalReason, setModalReason] = useState<string | null>(null);

  // Fetch challenge data on mount
  useEffect(() => {
    const fetchChallenge = async () => {
      try {
        const response = await tradingAPI.getActiveChallenge();
        setChallenge(response.data.challenge);
      } catch (err: any) {
        setError(err.response?.data?.error || "Failed to fetch challenge");
      }
    };

    fetchChallenge();
  }, []);

  // Fetch live price, signal and chart when symbol changes
  useEffect(() => {
    const fetchData = async () => {
      try {
        const isMorocco = moroccoSymbols.includes(selectedSymbol);
        if (isMorocco) {
          const [priceResponse, signalResponse] = await Promise.all([
            marketAPI.getMoroccoStock(selectedSymbol),
            marketAPI.getMoroccoSignal(selectedSymbol),
          ]);
          setLivePrice(priceResponse.data);
          setSignal(signalResponse.data);
          setChartData(undefined);
        } else {
          const [priceResponse, signalResponse, chartResponse] = await Promise.all([
            marketAPI.getLivePrice(selectedSymbol),
            marketAPI.getSignal(selectedSymbol),
            marketAPI.getChartData(selectedSymbol),
          ]);
          setLivePrice(priceResponse.data);
          setSignal(signalResponse.data);
          const candles = (chartResponse.data?.data ?? []).map((r: any) => ({
            time: r.timestamp,
            open: r.open,
            high: r.high,
            low: r.low,
            close: r.close,
          }));
          setChartData(candles);
        }
        setError(null);
      } catch (err: any) {
        setError(err.response?.data?.error || "Failed to fetch data");
      }
    };

    fetchData();

    if (isPolling) {
      const interval = setInterval(fetchData, 30000); // Poll every 30 seconds
      return () => clearInterval(interval);
    }
  }, [selectedSymbol, isPolling]);

  const executeTrade = async (action: "buy" | "sell") => {
    if (!livePrice || !challenge) return;

    setIsTrading(true);
    try {
      const totalValue = quantity * livePrice.price;
      const tradeResponse = await tradingAPI.executeTrade({
        symbol: selectedSymbol,
        action,
        quantity,
        price: livePrice.price,
      });

      const ruleCheck = tradeResponse.data?.rule_check;
      if (ruleCheck && (ruleCheck.status === "failed" || ruleCheck.status === "passed")) {
        setModalStatus(ruleCheck.status);
        setModalReason(ruleCheck.reason ?? null);
        setShowModal(true);
      }

      // Refresh challenge data after trade
      const response = await tradingAPI.getActiveChallenge();
      setChallenge(response.data.challenge);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to execute trade");
    } finally {
      setIsTrading(false);
    }
  };

  const getProfitPercent = () => {
    if (!challenge) return 0;
    return ((challenge.current_balance - challenge.initial_balance) / challenge.initial_balance) * 100;
  };

  const getProfitColor = () => {
    const profit = getProfitPercent();
    if (profit >= 0) return "text-green-500";
    if (profit >= -5) return "text-yellow-500";
    return "text-red-500";
  };

  const getSignalColor = () => {
    if (!signal) return "";
    switch (signal.signal) {
      case "BUY":
        return "bg-green-500/20 text-green-400";
      case "SELL":
        return "bg-red-500/20 text-red-400";
      case "HOLD":
        return "bg-yellow-500/20 text-yellow-400";
      default:
        return "";
    }
  };

  const getRiskColor = () => {
    if (!signal) return "";
    const level = signal.risk_level.toString().toLowerCase();
    switch (level) {
      case "low":
        return "bg-green-500/20 text-green-400";
      case "medium":
        return "bg-yellow-500/20 text-yellow-400";
      case "high":
        return "bg-red-500/20 text-red-400";
      default:
        return "";
    }
  };

  return (
    <>
    <div className="flex min-h-dvh bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-white">
      {/* Left Sidebar */}
      <aside className="w-64 border-r border-slate-200 bg-slate-100 p-4 dark:border-slate-800 dark:bg-slate-900">
        <h3 className="mb-4 text-lg font-semibold">{t("dashboard.international")}</h3>
        <div className="mb-4 space-y-2">
          {internationalSymbols.map((symbol) => (
            <button
              key={symbol}
              onClick={() => setSelectedSymbol(symbol)}
              className={`w-full rounded-md px-3 py-2 text-left transition ${
                selectedSymbol === symbol
                  ? "bg-blue-600 text-white"
                  : "bg-slate-200 hover:bg-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700"
              }`}
            >
              {symbol}
            </button>
          ))}
        </div>

        <h3 className="mb-4 text-lg font-semibold">{t("dashboard.morocco")}</h3>
        <div className="space-y-2">
          {moroccoSymbols.map((symbol) => (
            <button
              key={symbol}
              onClick={() => setSelectedSymbol(symbol)}
              className={`w-full rounded-md px-3 py-2 text-left transition ${
                selectedSymbol === symbol
                  ? "bg-blue-600 text-white"
                  : "bg-slate-200 hover:bg-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700"
              }`}
            >
              {symbol}
            </button>
          ))}
        </div>
      </aside>

      {/* Center Zone */}
      <main className="flex-1 overflow-y-auto">
        {/* Top Bar */}
        <div className="border-b border-slate-200 p-4 dark:border-slate-800">
          {challenge && (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium">
                  {t("dashboard.challenge_status")}:{" "}
                  <span className="text-blue-400">{challenge.status}</span>
                </span>
                <div className="flex-1">
                  <div className="w-64 bg-slate-200 rounded-full h-2 dark:bg-slate-800">
                    <div
                      className={`h-2 rounded-full ${
                        getProfitPercent() >= 0 ? "bg-green-500" : "bg-red-500"
                      }`}
                      style={{ width: `${Math.min(Math.abs(getProfitPercent()) * 10, 100)}%` }}
                    />
                  </div>
                </div>
              </div>

              {getProfitPercent() < -7 && (
                <div className="flex items-center gap-2 text-red-500">
                  <AlertTriangle className="h-5 w-5" />
                  <span className="font-semibold">{t("dashboard.approaching_max_loss")}</span>
                </div>
              )}

              {getProfitPercent() >= 10 && (
                <div className="flex items-center gap-2 text-green-500">
                  <CheckCircle className="h-5 w-5" />
                  <span className="font-semibold">{t("dashboard.profit_target_reached")}</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Price Display */}
        <div className="border-b border-slate-200 p-6 text-center dark:border-slate-800">
          <h1 className="text-4xl font-bold">{selectedSymbol}</h1>
          {livePrice ? (
            <>
              <p className="text-5xl font-extrabold text-blue-400">
                {livePrice.currency === "MAD" ? "MAD " : "$"}
                {livePrice.price.toFixed(2)}
              </p>
              <div className="mt-2 flex items-center justify-center gap-2">
                {livePrice.change_percent >= 0 ? (
                  <TrendingUp className="h-6 w-6 text-green-500" />
                ) : (
                  <TrendingDown className="h-6 w-6 text-red-500" />
                )}
                <span
                  className={`text-2xl font-semibold ${
                    livePrice.change_percent >= 0 ? "text-green-500" : "text-red-500"
                  }`}
                >
                  {livePrice.change_percent >= 0 ? "+" : ""}
                  {livePrice.change_percent.toFixed(2)}%
                </span>
              </div>
              <div className="mt-4 flex items-center justify-center gap-2">
                <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                <span className="text-sm text-slate-400">{t("dashboard.live_updates")}</span>
                <button
                  onClick={() => setIsPolling(!isPolling)}
                  className="ml-2 rounded-full p-1 hover:bg-slate-800"
                >
                  {isPolling ? (
                    <Pause className="h-4 w-4" />
                  ) : (
                    <Play className="h-4 w-4" />
                  )}
                </button>
              </div>
            </>
          ) : (
            <p className="text-slate-600 dark:text-slate-400">{t("dashboard.loading_price")}</p>
          )}
        </div>

        {/* Chart Area */}
        <div className="flex-1 p-4">
          {!moroccoSymbols.includes(selectedSymbol) && chartData && chartData.length > 0 ? (
            <TradingChart title={`${t("dashboard.chart_title")} ${selectedSymbol}`} data={chartData} />
          ) : (
            <div className="h-full rounded-lg border border-slate-200 bg-white p-4 text-center text-slate-600 dark:border-slate-800 dark:bg-slate-900/30 dark:text-slate-400">
              <p className="text-xl">{t("dashboard.chart_title")}</p>
              <p className="mt-2">
                {moroccoSymbols.includes(selectedSymbol)
                  ? t("dashboard.chart_unavailable_maroc")
                  : t("dashboard.chart_loading", { symbol: selectedSymbol })}
              </p>
            </div>
          )}
        </div>

        {/* Trade Execution Bar */}
        <div className="sticky bottom-0 z-10 border-t border-slate-200 bg-slate-100/70 p-4 backdrop-blur dark:border-slate-800 dark:bg-slate-950/70">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <label className="text-sm font-medium">{t("dashboard.quantity")}:</label>
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                className="w-20 rounded-md bg-slate-200 px-3 py-2 text-center dark:bg-slate-800"
                min="1"
              />
              {livePrice && (
                <span className="text-sm text-slate-400">
                  {t("dashboard.total")}:{" "}
                  {livePrice.currency === "MAD" ? "MAD " : "$"}
                  {(quantity * livePrice.price).toFixed(2)}
                </span>
              )}
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => executeTrade("buy")}
                disabled={isTrading || !livePrice || !challenge}
                className="rounded-md bg-green-600 px-6 py-2 font-semibold text-white transition hover:bg-green-700 disabled:opacity-50"
              >
                {t("dashboard.buy")}
              </button>
              <button
                onClick={() => executeTrade("sell")}
                disabled={isTrading || !livePrice || !challenge}
                className="rounded-md bg-red-600 px-6 py-2 font-semibold text-white transition hover:bg-red-700 disabled:opacity-50"
              >
                {t("dashboard.sell")}
              </button>
            </div>
          </div>
          {!challenge && (
            <div className="mt-3 text-center text-sm text-yellow-400">
              {t("dashboard.no_challenge")}
            </div>
          )}
        </div>
      </main>

      {/* Right Sidebar */}
      <aside className="w-80 border-l border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
        {/* AI Signals Panel */}
        <div className="mb-6 rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <h3 className="mb-4 text-lg font-semibold">{t("dashboard.ai_title")}</h3>
          {signal ? (
            <>
              <div className={`mb-4 rounded-md p-3 text-center ${getSignalColor()}`}>
                <span className="text-2xl font-bold">{signal.signal}</span>
              </div>
              <div className="mb-4">
                <p className="text-sm text-slate-600 dark:text-slate-400">{t("dashboard.confidence")}</p>
                <div className="mt-2 h-2 w-full rounded-full bg-slate-200 dark:bg-slate-800">
                  <div
                    className="h-2 rounded-full bg-blue-500"
                    style={{ width: `${signal.confidence}%` }}
                  />
                </div>
                <p className="mt-1 text-right text-sm text-slate-600 dark:text-slate-400">{signal.confidence}%</p>
              </div>
              <div className="mb-4">
                <p className="text-sm text-slate-600 dark:text-slate-400">{t("dashboard.risk_level")}</p>
                <div className={`mt-2 rounded-md p-2 text-center ${getRiskColor()}`}>
                  <span className="font-semibold">{signal.risk_level}</span>
                </div>
              </div>
              <p className="mb-4 text-sm text-slate-700 dark:text-slate-300">{signal.reason}</p>
              <p className="text-xs text-slate-600 dark:text-slate-500">
                {t("dashboard.signal_note")}
              </p>
            </>
          ) : (
            <p className="text-slate-600 dark:text-slate-400">{t("dashboard.loading_signal")}</p>
          )}
        </div>

        {/* Challenge Stats */}
        <div className="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <h3 className="mb-4 text-lg font-semibold">{t("dashboard.challenge_title")}</h3>
          {challenge ? (
            <>
              <div className="mb-4">
                <p className="text-sm text-slate-600 dark:text-slate-400">{t("dashboard.initial_balance")}</p>
                <p className="text-xl font-bold">
                  ${challenge.initial_balance.toFixed(2)}
                </p>
              </div>
              <div className="mb-4">
                <p className="text-sm text-slate-600 dark:text-slate-400">{t("dashboard.current_balance")}</p>
                <p className="text-xl font-bold">
                  ${challenge.current_balance.toFixed(2)}
                </p>
              </div>
              <div className="mb-4">
                <p className="text-sm text-slate-600 dark:text-slate-400">{t("dashboard.pl")}</p>
                <p className={`text-xl font-bold ${getProfitColor()}`}>
                  {getProfitPercent() >= 0 ? "+" : ""}
                  {getProfitPercent().toFixed(2)}%
                </p>
              </div>
              <hr className="my-4 border-slate-800" />
              <div className="mb-2">
                <p className="text-sm text-slate-600 dark:text-slate-400">{t("dashboard.target")}</p>
                <p className="font-semibold text-green-500">+{challenge.profit_target}%</p>
              </div>
              <div className="mb-2">
                <p className="text-sm text-slate-600 dark:text-slate-400">{t("dashboard.max_daily_loss")}</p>
                <p className="font-semibold text-red-500">{challenge.max_daily_loss_percent}%</p>
              </div>
              <div>
                <p className="text-sm text-slate-600 dark:text-slate-400">{t("dashboard.max_total_loss")}</p>
                <p className="font-semibold text-red-500">{challenge.max_total_loss_percent}%</p>
              </div>
            </>
          ) : (
            <p className="text-slate-600 dark:text-slate-400">{t("dashboard.loading_stats")}</p>
          )}
        </div>
      </aside>

      {error && (
        <div className="fixed bottom-4 right-4 rounded-md bg-red-500/20 p-4 text-red-400 shadow-lg">
          <p>{error}</p>
          <button
            onClick={() => setError(null)}
            className="mt-2 rounded-md bg-red-500 px-3 py-1 text-sm text-white"
          >
            {t("dashboard.dismiss")}
          </button>
        </div>
      )}
    </div>
    {showModal && modalStatus && (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
        <div className="max-w-md rounded-2xl bg-slate-900 p-8 text-center shadow-2xl">
          <div className="mb-4 text-4xl">
            {modalStatus === "failed" ? "❌" : "🎉"}
          </div>
          <h2 className="mt-2 text-2xl font-bold">
            {modalStatus === "failed"
              ? "Challenge Failed!"
              : "Congratulations! You're Funded!"}
          </h2>
          {modalReason && (
            <p className="mt-3 text-slate-400">
              {modalReason}
            </p>
          )}
          <button
            onClick={() => setShowModal(false)}
            className="mt-6 rounded-md bg-blue-600 px-6 py-2 text-white transition hover:bg-blue-700"
          >
            OK
          </button>
        </div>
      </div>
    )}
    </>
  );
}
