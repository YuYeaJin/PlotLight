// src/components/SettingsModal.tsx
import type React from "react";

type Theme = "light" | "dark" | "sage";

type Props = {
  theme: Theme;
  onThemeChange: (t: Theme) => void;
  persist: boolean;
  onPersistChange: (v: boolean) => void;
  saveReport: boolean;
  onSaveReportChange: (v: boolean) => void;
  requirePassword: boolean;
  onRequirePasswordChange: (v: boolean) => void;
  onClose: () => void;
};

export default function SettingsModal({
  theme,
  onThemeChange,
  persist,
  onPersistChange,
  saveReport,
  onSaveReportChange,
  requirePassword,
  onRequirePasswordChange,
  onClose,
}: Props) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.35)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        style={{
          width: 480,
          maxWidth: "90vw",
          background: "var(--card)",
          color: "var(--ink)",
          borderRadius: 12,
          padding: 20,
          boxShadow: "0 12px 40px rgba(0,0,0,0.25)",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <header
          style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}
        >
          <h2 style={{ margin: 0, fontSize: 18 }}>설정</h2>
          <button
            onClick={onClose}
            style={{ border: "none", background: "none", cursor: "pointer" }}
          >
            ✕
          </button>
        </header>

        {/* 테마 */}
        <section style={{ marginBottom: 16 }}>
          <h3 style={{ margin: "4px 0 8px", fontSize: 14 }}>테마</h3>
          <div style={{ display: "flex", gap: 8 }}>
            {(["light", "dark", "sage"] as Theme[]).map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => onThemeChange(t)}
                className="btn btn--ghost"
                style={{
                  border:
                    theme === t ? "2px solid var(--accent)" : "1px solid var(--line)",
                  padding: "4px 10px",
                }}
              >
                {t === "light" ? "라이트" : t === "dark" ? "다크" : "세이지"}
              </button>
            ))}
          </div>
        </section>

        {/* 저장 옵션 */}
        <section style={{ marginBottom: 16 }}>
          <h3 style={{ margin: "4px 0 8px", fontSize: 14 }}>저장 기본값</h3>
          <label style={{ display: "block", fontSize: 14 }}>
            <input
              type="checkbox"
              checked={persist}
              onChange={(e) => onPersistChange(e.target.checked)}
            />{" "}
            원문 자동 저장
          </label>
          <label style={{ display: "block", fontSize: 14, marginTop: 4 }}>
            <input
              type="checkbox"
              checked={saveReport}
              onChange={(e) => onSaveReportChange(e.target.checked)}
            />{" "}
            분석 레포트 자동 저장
          </label>
        </section>

        {/* 비밀번호 (지금은 UI만, 나중에 기능 연결) */}
        <section style={{ marginBottom: 16 }}>
          <h3 style={{ margin: "4px 0 8px", fontSize: 14 }}>보안</h3>
          <label style={{ display: "block", fontSize: 14 }}>
            <input
              type="checkbox"
              checked={requirePassword}
              onChange={(e) => onRequirePasswordChange(e.target.checked)}
            />{" "}
            실행 시 비밀번호 요구
          </label>
          <p style={{ fontSize: 12, opacity: 0.7, marginTop: 4 }}>
            (지금은 표시만 하고, 실제 비밀번호 로직은 나중에 백엔드랑 연결해도 됩니다.)
          </p>
        </section>

        <footer style={{ textAlign: "right" }}>
          <button
            type="button"
            onClick={onClose}
            className="btn btn--ghost"
            style={{ padding: "6px 14px" }}
          >
            닫기
          </button>
        </footer>
      </div>
    </div>
  );
}
