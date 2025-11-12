import { useEffect, useState } from "react";
import "./styles/tokens.css";
import "./styles/themes.css";
import "./styles/globals.css";
import QuickAnalyze from "./pages/QuickAnalyze";

export default function App() {
  const [theme, setTheme] = useState<"light"|"dark"|"sage">("light");
  useEffect(() => { document.documentElement.setAttribute("data-theme", theme); }, [theme]);

  return (
    <>
      <header className="card" style={{ padding:"12px 16px", display:"flex", gap:12, alignItems:"center" }}>
        <h1 style={{ margin:0, fontSize:18, fontWeight:700 }}>PlotLight</h1>
        <div style={{ marginLeft:"auto", display:"flex", gap:8 }}>
          <button className="btn btn--ghost" onClick={()=>setTheme("light")}>Light</button>
          <button className="btn btn--ghost" onClick={()=>setTheme("dark")}>Dark</button>
          <button className="btn btn--ghost" onClick={()=>setTheme("sage")}>Sage</button>
        </div>
      </header>

      {/* 본문은 QuickAnalyze 한 개만 */}
      <QuickAnalyze />
    </>
  );
}
