import { useState, useEffect } from 'react';
import { Trophy, Medal } from 'lucide-react';
import { leaderboardAPI } from '../services/api';
import { useTranslation } from 'react-i18next';

interface Trader {
  rank?: number;
  username: string;
  profit_percent?: number;
  avg_profit_percent?: number;
  total_trades: number;
}

const getRankClass = (rank: number) => {
  switch (rank) {
    case 1:
      return 'bg-gradient-to-r from-amber-500/30 to-yellow-500/30';
    case 2:
      return 'bg-gradient-to-r from-slate-400/30 to-gray-400/30';
    case 3:
      return 'bg-gradient-to-r from-orange-700/30 to-amber-800/30';
    default:
      return 'bg-slate-800/50';
  }
};

const getRankIcon = (rank: number) => {
  if (rank <= 3) {
    let color = '';
    if (rank === 1) color = 'text-yellow-400';
    if (rank === 2) color = 'text-slate-300';
    if (rank === 3) color = 'text-orange-500';
    return <Medal className={`h-5 w-5 ${color}`} />;
  }
  return <span className="text-sm text-slate-400">{rank}</span>;
};

export default function Leaderboard() {
  const [leaderboardData, setLeaderboardData] = useState<Trader[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { t } = useTranslation();

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await leaderboardAPI.getMonthly();
      console.log('Leaderboard API response:', response.data);
      const raw = Array.isArray(response.data) ? response.data : [];
      const normalized: Trader[] = raw.map((item: any, idx: number) => ({
        rank: item.rank ?? idx + 1,
        username: item.username,
        profit_percent: item.profit_percent ?? item.avg_profit_percent ?? 0,
        avg_profit_percent: item.avg_profit_percent,
        total_trades: item.total_trades ?? 0,
      }));
      console.log('Normalized leaderboard data:', normalized);
      setLeaderboardData(normalized);
      setError(null);
    } catch (err) {
      setError('Failed to fetch leaderboard data.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeaderboard(); // Initial fetch

    const intervalId = setInterval(() => {
      fetchLeaderboard();
    }, 60000); // Refresh every 60 seconds

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100 p-4 sm:p-6 lg:p-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <Trophy className="h-12 w-12 mx-auto text-amber-400 mb-2" />
          <h1 className="text-3xl sm:text-4xl font-bold">{t('leaderboard.title')}</h1>
          <p className="text-slate-400 mt-2">{t('leaderboard.updated')}</p>
        </div>

        <div className="bg-white/60 dark:bg-slate-900/50 backdrop-blur-sm rounded-2xl shadow-xl overflow-hidden border border-slate-200 dark:border-slate-800">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-800">
              <thead className="bg-slate-200/60 dark:bg-slate-800/50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                    {t('leaderboard.rank')}
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                    {t('leaderboard.username')}
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                    {t('leaderboard.profit')}
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider">
                    {t('leaderboard.trades')}
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {loading ? (
                  <tr>
                    <td colSpan={4} className="text-center py-8 text-slate-400">{t('leaderboard.loading')}</td>
                  </tr>
                ) : error ? (
                  <tr>
                    <td colSpan={4} className="text-center py-8 text-red-400">{t('leaderboard.error')}</td>
                  </tr>
                ) : (
                  leaderboardData.map((trader, idx) => {
                    const profit = Number(trader.profit_percent ?? trader.avg_profit_percent ?? 0);
                    const rank = trader.rank ?? idx + 1;
                    return (
                    <tr key={rank} className={`transition-colors hover:bg-slate-800/70 ${getRankClass(rank)}`}>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center justify-center h-6 w-6 rounded-full bg-slate-700/50">
                          {getRankIcon(rank)}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-white">{trader.username}</div>
                      </td>
                      <td className={`px-6 py-4 whitespace-nowrap text-sm font-semibold ${profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {profit.toFixed(2)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                        {trader.total_trades}
                      </td>
                    </tr>
                  )})
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
