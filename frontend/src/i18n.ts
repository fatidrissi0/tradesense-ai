import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import fr from "./locales/fr.json";
import en from "./locales/en.json";
import ar from "./locales/ar.json";

const saved = localStorage.getItem("lang");
const initialLang =
  saved && (saved === "fr" || saved === "en" || saved === "ar")
    ? saved
    : "fr";

i18n.use(initReactI18next).init({
  resources: {
    fr: { translation: fr },
    en: { translation: en },
    ar: { translation: ar },
  },
  lng: initialLang,
  fallbackLng: "fr",
  interpolation: { escapeValue: false },
});

document.documentElement.setAttribute("lang", initialLang);
document.documentElement.dir = initialLang === "ar" ? "rtl" : "ltr";

export default i18n;
