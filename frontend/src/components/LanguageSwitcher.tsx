import { useEffect, useState } from "react";
import i18n from "../i18n";

const flags: Record<string, string> = {
  fr: "🇫🇷",
  en: "🇬🇧",
  ar: "🇲🇦"
};

const languages = [
  { code: "fr", label: "FR" },
  { code: "en", label: "EN" },
  { code: "ar", label: "AR" }
];

export default function LanguageSwitcher() {
  const [lang, setLang] = useState(i18n.language);

  useEffect(() => {
    localStorage.setItem("lang", lang);
    i18n.changeLanguage(lang);
    document.documentElement.setAttribute("lang", lang);
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  }, [lang]);

  return (
    <div className="flex items-center gap-2">
      {languages.map((l) => (
        <button
          key={l.code}
          type="button"
          onClick={() => setLang(l.code)}
          className={`inline-flex items-center gap-1 rounded-md border px-2 py-1 text-xs ${
            lang === l.code
              ? "border-blue-500 text-blue-500"
              : "border-slate-200 text-slate-700 dark:border-slate-800 dark:text-slate-200"
          }`}
        >
          <span className="text-base leading-none">{flags[l.code]}</span>
          {l.label}
        </button>
      ))}
    </div>
  );
}
