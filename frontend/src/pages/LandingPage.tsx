import { Link, useNavigate } from "react-router-dom";
import {
  TrendingUp,
  Newspaper,
  Users,
  GraduationCap,
  CheckCircle,
  BrainCircuit,
} from "lucide-react";
import { useTranslation } from "react-i18next";

const features = [
  {
    name: "Trading IA",
    description:
      "Nos algorithmes analysent le marché pour vous fournir des signaux de trading pertinents.",
    icon: <TrendingUp className="h-10 w-10 text-blue-500" />,
  },
  {
    name: "News Hub",
    description:
      "Restez informé avec un flux d'actualités financières en temps réel, analysées par notre IA.",
    icon: <Newspaper className="h-10 w-10 text-green-500" />,
  },
  {
    name: "Communauté",
    description:
      "Échangez avec d'autres traders, partagez des stratégies et apprenez ensemble.",
    icon: <Users className="h-10 w-10 text-yellow-500" />,
  },
  {
    name: "MasterClass",
    description:
      "Accédez à des formations exclusives pour maîtriser le trading, du niveau débutant à expert.",
    icon: <GraduationCap className="h-10 w-10 text-purple-500" />,
  },
];

const pricingPlans = [
  {
    name: "Starter",
    price: "200 DH",
    balance: "5 000 DH",
    features: [
      "Accès aux signaux IA",
      "Tableau de bord basique",
      "Support par email",
    ],
  },
  {
    name: "Pro",
    price: "500 DH",
    balance: "10 000 DH",
    features: [
      "Signaux IA avancés",
      "Analyse de performance",
      "Support prioritaire",
    ],
    popular: true,
  },
  {
    name: "Elite",
    price: "1000 DH",
    balance: "25 000 DH",
    features: [
      "Accès complet aux signaux",
      "Support VIP 24/7",
      "Accès anticipé aux nouveautés",
    ],
  },
];

export default function LandingPage() {
  const navigate = useNavigate();
  const { t } = useTranslation();

  return (
    <div className="bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100">

      {/* Hero Section */}
      <section className="relative bg-gradient-to-b from-blue-200/30 to-purple-200/30 dark:from-blue-900/30 dark:to-purple-900/30 py-20 text-center">
        <div className="container mx-auto px-4">
          <BrainCircuit className="mx-auto h-16 w-16 text-blue-500 dark:text-blue-400" />
          <h1 className="mt-4 text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl">
            {t("landing.hero_title")}
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-600 dark:text-slate-300">
            {t("landing.hero_subtitle")}
          </p>
          <div className="mt-8 flex justify-center gap-4">
            <button
              onClick={() => navigate("/register")}
              className="rounded-md bg-blue-600 px-8 py-3 font-semibold text-white shadow-lg transition hover:bg-blue-700"
            >
              {t("landing.cta_start")}
            </button>
            <button
              onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })}
              className="rounded-md bg-slate-200 px-8 py-3 font-semibold text-slate-900 transition hover:bg-slate-300 dark:bg-slate-700/50 dark:text-white dark:hover:bg-slate-700"
            >
              {t("landing.cta_learn")}
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <div
                key={feature.name}
                className="rounded-xl bg-white p-6 text-center shadow-lg transition hover:scale-105 dark:bg-slate-900"
              >
                <div className="flex justify-center">{feature.icon}</div>
                <h3 className="mt-4 text-xl font-bold">{feature.name}</h3>
                <p className="mt-2 text-slate-600 dark:text-slate-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="bg-slate-100 py-20 dark:bg-slate-900/50">
        <div className="container mx-auto px-4">
          <h2 className="text-center text-3xl font-bold">
            {t("landing.pricing_title")}
          </h2>
          <div className="mt-12 grid grid-cols-1 gap-8 lg:grid-cols-3">
            {pricingPlans.map((plan) => (
              <div
                key={plan.name}
                className={`relative rounded-2xl border-2 p-8 shadow-lg ${
                  plan.popular
                    ? "border-blue-500"
                    : "border-slate-200 dark:border-slate-800"
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 rounded-full bg-blue-500 px-4 py-1 text-sm font-semibold">
                    Populaire
                  </div>
                )}
                <h3 className="text-2xl font-bold">{plan.name}</h3>
                <p className="mt-4">
                  <span className="text-5xl font-extrabold">{plan.price}</span>
                </p>
                <p className="mt-2 text-slate-600 dark:text-slate-400">
                  Balance virtuelle de {plan.balance}
                </p>
                <ul className="mt-6 space-y-3">
                  {plan.features.map((item) => (
                    <li key={item} className="flex items-center gap-2">
                      <CheckCircle className="h-5 w-5 text-green-500" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
                <button
                  onClick={() => navigate("/checkout", { state: { plan } })}
                  className={`mt-8 w-full rounded-md py-3 font-semibold transition ${
                    plan.popular
                      ? "bg-blue-600 text-white hover:bg-blue-700"
                      : "bg-slate-200 text-slate-900 hover:bg-slate-300 dark:bg-slate-800 dark:text-white dark:hover:bg-slate-700"
                  }`}
                >
                  {t("landing.choose_plan")}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="relative my-20">
        <div className="container mx-auto rounded-2xl bg-gradient-to-r from-purple-600 to-blue-600 px-4 py-12 text-center">
          <h2 className="text-3xl font-bold">
            {t("landing.cta_final_title", { defaultValue: "Prêt à Devenir un Trader Financé?" })}
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-slate-100 dark:text-slate-200">
            {t("landing.cta_final_sub", { defaultValue: "Votre carrière de trader professionnel commence ici. Prouvez vos compétences et nous vous fournissons le capital." })}
          </p>
          <button
            onClick={() => navigate("/register")}
            className="mt-8 rounded-md bg-white px-8 py-3 font-semibold text-slate-900 shadow-lg transition hover:bg-slate-200"
          >
            {t("landing.cta_final_button", { defaultValue: "S'inscrire Maintenant" })}
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800 py-8">
        <div className="container mx-auto flex flex-col items-center justify-between px-4 text-sm text-slate-600 dark:text-slate-400 sm:flex-row">
          <p>&copy; {new Date().getFullYear()} TradeSense AI. Tous droits réservés.</p>
          <div className="mt-4 flex gap-6 sm:mt-0">
            <Link to="/terms" className="hover:text-slate-900 dark:hover:text-white">
              Conditions
            </Link>
            <Link to="/privacy" className="hover:text-slate-900 dark:hover:text-white">
              Confidentialité
            </Link>
            <Link to="/support" className="hover:text-slate-900 dark:hover:text-white">
              Support
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
