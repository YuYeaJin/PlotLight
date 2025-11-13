import { useEffect, useState } from "react";
import "./styles/tokens.css";
import "./styles/themes.css";
import "./styles/globals.css";
import QuickAnalyze from "./pages/QuickAnalyze";
import SettingsModal from "./components/SettingsModal";

export default function App() {
  const [theme, setTheme] = useState<"light" | "dark" | "sage">("light");
  const [defaultPersist, setDefaultPersist] = useState(true);
  const [defaultSaveReport, setDefaultSaveReport] = useState(false);
  const [requirePassword, setRequirePassword] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <>
      <header
        className="card"
        style={{
          padding: "12px 16px",
          display: "flex",
          gap: 12,
          alignItems: "center",
        }}
      >
        <h1 style={{ margin: 0, fontSize: 18, fontWeight: 700 }}>PlotLight</h1>

        <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: "center" }}>
          <button
            className="btn btn--ghost"
            type="button"
            onClick={() => setShowSettings(true)}
          >
            ⚙ 설정
          </button>
        </div>
      </header>

      {/* 분석 페이지: 설정에서 고른 기본값을 props로 전달 */}
      <QuickAnalyze
        defaultPersist={defaultPersist}
        defaultSaveReport={defaultSaveReport}
      />

      {/* 설정 모달 */}
      {showSettings && (
        <SettingsModal
          theme={theme}
          onThemeChange={setTheme}
          persist={defaultPersist}
          onPersistChange={setDefaultPersist}
          saveReport={defaultSaveReport}
          onSaveReportChange={setDefaultSaveReport}
          requirePassword={requirePassword}
          onRequirePasswordChange={setRequirePassword}
          onClose={() => setShowSettings(false)}
        />
      )}
    </>
  );
}
