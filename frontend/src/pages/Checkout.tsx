import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CreditCard, Bitcoin, Wallet, CheckCircle, XCircle, Loader2, ArrowLeft } from 'lucide-react';
import { paymentAPI } from '../services/api';

interface Plan {
  name: string;
  price: string;
  balance: string;
  features: string[];
}

export default function Checkout() {
  const location = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [unauthorized, setUnauthorized] = useState(false);
  
  const plan = location.state?.plan as Plan | undefined;

  useEffect(() => {
    if (!plan) {
      navigate('/');
    }
  }, [plan, navigate]);

  if (!plan) return null;

  const handlePayment = async (paymentMethod: string) => {
    setLoading(true);
    setError(null);

    // Simulate delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    try {
      await paymentAPI.checkout({
        plan_type: plan.name.toLowerCase(),
        payment_method: paymentMethod
      });
      setShowSuccessModal(true);
    } catch (err: any) {
      if (err?.response?.status === 401) {
        setUnauthorized(true);
        setError('Session expirée. Veuillez vous connecter.');
      } else {
        const apiError =
          err?.response?.data?.error ||
          err?.response?.data?.message ||
          err?.message;
        setError(apiError || 'Échec du paiement. Réessayez.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <button 
          onClick={() => navigate(-1)} 
          className="flex items-center text-slate-400 hover:text-white mb-8 transition-colors"
        >
          <ArrowLeft className="h-5 w-5 mr-2" />
          Retour
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Plan Details */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 shadow-xl">
            <h2 className="text-2xl font-bold text-white mb-6">Récapitulatif de la commande</h2>
            
            <div className="space-y-6">
              <div className="flex justify-between items-center pb-6 border-b border-slate-700">
                <div>
                  <h3 className="text-xl font-semibold text-white">{plan.name} Challenge</h3>
                  <p className="text-slate-400">Balance: {plan.balance}</p>
                </div>
                <div className="text-2xl font-bold text-blue-400">{plan.price}</div>
              </div>

              <div className="space-y-3">
                <h4 className="text-sm font-medium text-slate-300 uppercase tracking-wider">Inclus</h4>
                {plan.features.map((feature, index) => (
                  <div key={index} className="flex items-center text-slate-300">
                    <CheckCircle className="h-4 w-4 text-green-500 mr-3" />
                    {feature}
                  </div>
                ))}
              </div>

              <div className="pt-6 border-t border-slate-700">
                <div className="flex justify-between items-center text-lg font-bold text-white">
                  <span>Total à payer</span>
                  <span>{plan.price}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Payment Methods */}
          <div className="bg-slate-800 rounded-2xl p-8 shadow-xl">
            <h2 className="text-2xl font-bold text-white mb-6">Moyen de paiement</h2>
            
            <div className="space-y-4">
              <button
                onClick={() => handlePayment('cmi')}
                disabled={loading}
                className="w-full group relative flex items-center p-4 border border-slate-600 rounded-xl hover:border-blue-500 hover:bg-slate-700/50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className="h-12 w-12 bg-blue-500/10 rounded-lg flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
                  <CreditCard className="h-6 w-6 text-blue-400" />
                </div>
                <div className="ml-4 text-left">
                  <h3 className="font-semibold text-white">Carte Bancaire (CMI)</h3>
                  <p className="text-sm text-slate-400">Paiement sécurisé par CMI</p>
                </div>
              </button>

              <button
                onClick={() => handlePayment('crypto')}
                disabled={loading}
                className="w-full group relative flex items-center p-4 border border-slate-600 rounded-xl hover:border-orange-500 hover:bg-slate-700/50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className="h-12 w-12 bg-orange-500/10 rounded-lg flex items-center justify-center group-hover:bg-orange-500/20 transition-colors">
                  <Bitcoin className="h-6 w-6 text-orange-400" />
                </div>
                <div className="ml-4 text-left">
                  <h3 className="font-semibold text-white">Crypto-monnaies</h3>
                  <p className="text-sm text-slate-400">Bitcoin, USDT, Ethereum...</p>
                </div>
              </button>

              <button
                onClick={() => handlePayment('paypal')}
                disabled={loading}
                className="w-full group relative flex items-center p-4 border border-slate-600 rounded-xl hover:border-blue-400 hover:bg-slate-700/50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className="h-12 w-12 bg-blue-400/10 rounded-lg flex items-center justify-center group-hover:bg-blue-400/20 transition-colors">
                  <Wallet className="h-6 w-6 text-blue-400" />
                </div>
                <div className="ml-4 text-left">
                  <h3 className="font-semibold text-white">PayPal</h3>
                  <p className="text-sm text-slate-400">Paiement rapide et sécurisé</p>
                </div>
              </button>
            </div>

            {loading && (
              <div className="mt-6 flex flex-col items-center justify-center text-blue-400 animate-pulse">
                <Loader2 className="h-8 w-8 animate-spin mb-2" />
                <p>Traitement du paiement en cours...</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Success Modal */}
      {showSuccessModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 rounded-2xl p-8 max-w-md w-full text-center border border-green-500/20 shadow-2xl transform transition-all scale-100">
            <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-500/10 mb-6">
              <CheckCircle className="h-10 w-10 text-green-500" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Paiement Réussi !</h3>
            <p className="text-slate-400 mb-8">
              Félicitations ! Votre challenge {plan.name} a été activé avec succès. Vous pouvez commencer à trader dès maintenant.
            </p>
            <button
              onClick={() => navigate('/dashboard')}
              className="w-full bg-green-600 text-white py-3 px-4 rounded-xl font-semibold hover:bg-green-700 transition-colors shadow-lg hover:shadow-green-500/20"
            >
              Accéder au Dashboard
            </button>
          </div>
        </div>
      )}

      {/* Error Modal */}
      {error && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 rounded-2xl p-8 max-w-md w-full text-center border border-red-500/20 shadow-2xl">
            <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-500/10 mb-6">
              <XCircle className="h-10 w-10 text-red-500" />
            </div>
            <h3 className="text-2xl font-bold text-white mb-2">Échec du paiement</h3>
            <p className="text-slate-400 mb-8">{error}</p>
            <div className="flex gap-4">
              <button
                onClick={() => setError(null)}
                className="flex-1 bg-slate-700 text-white py-3 px-4 rounded-xl font-semibold hover:bg-slate-600 transition-colors"
              >
                Fermer
              </button>
              {unauthorized ? (
                <button
                  onClick={() => navigate('/login')}
                  className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
                >
                  Se connecter
                </button>
              ) : (
                <button
                  onClick={() => {
                    setError(null);
                  }}
                  className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
                >
                  Réessayer
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
