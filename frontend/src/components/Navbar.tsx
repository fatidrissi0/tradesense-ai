import { Link, NavLink } from "react-router-dom";
import { Moon, Sun } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useTranslation } from "react-i18next";
import LanguageSwitcher from "./LanguageSwitcher";

function getInitialTheme(): "dark" | "light" {
  const stored = localStorage.getItem("theme");
  if (stored === "dark" || stored === "light") return stored;
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

export default function Navbar() {
  const { user, logout, loading } = useAuth();
  const [theme, setTheme] = useState<"dark" | "light">(() =>
    getInitialTheme()
  );
  const { t } = useTranslation();

  const isDark = useMemo(() => theme === "dark", [theme]);

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") root.classList.add("dark");
    else root.classList.remove("dark");
    localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <header className="border-b border-slate-200 bg-white text-slate-900 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-100">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
        <Link to="/" className="font-semibold tracking-tight">
          {t("navbar.title")}
        </Link>
        <nav className="flex items-center gap-4 text-sm">
          {loading ? null : user ? (
            <>
              <NavLink
                to="/dashboard"
                className={({ isActive }) =>
                  isActive ? "font-semibold" : "opacity-80 hover:opacity-100"
                }
              >
                {t("navbar.dashboard")}
              </NavLink>
              <NavLink
                to="/leaderboard"
                className={({ isActive }) =>
                  isActive ? "font-semibold" : "opacity-80 hover:opacity-100"
                }
              >
                {t("navbar.leaderboard")}
              </NavLink>
              <span className="opacity-80">{t("navbar.greeting", { username: user.username })}</span>
              <button
                onClick={logout}
                className="opacity-80 hover:opacity-100"
              >
                {t("navbar.logout")}
              </button>
            </>
          ) : (
            <>
              <NavLink
                to="/login"
                className={({ isActive }) =>
                  isActive ? "font-semibold" : "opacity-80 hover:opacity-100"
                }
              >
                {t("navbar.login")}
              </NavLink>
              <NavLink
                to="/register"
                className={({ isActive }) =>
                  isActive ? "font-semibold" : "opacity-80 hover:opacity-100"
                }
              >
                {t("navbar.register")}
              </NavLink>
            </>
          )}
          <button
            type="button"
            onClick={() => setTheme((t) => (t === "dark" ? "light" : "dark"))}
            className="inline-flex items-center gap-2 rounded-md border border-slate-200 px-3 py-1.5 text-xs dark:border-slate-800"
          >
            {isDark ? <Sun size={16} /> : <Moon size={16} />}
            {isDark ? t("navbar.theme_light") : t("navbar.theme_dark")}
          </button>
          <LanguageSwitcher />
        </nav>
      </div>
    </header>
  );
}
