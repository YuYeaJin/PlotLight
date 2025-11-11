import { useState } from "react";
import "./styles/tokens.css";
import "./styles/themes.css";
import "./styles/globals.css";

export default function App(){
  const [theme, setTheme] = useState<"light"|"dark"|"sage">("light");
  return (
    <div data-theme={theme}>
      <header className="card" style={{padding:"12px 16px", display:"flex", gap:12}}>
        <h1 style={{margin:0,fontSize:18,fontWeight:700}}>PlotLight</h1>
        <div style={{marginLeft:"auto", display:"flex", gap:8}}>
          <button className="btn btn--ghost" onClick={()=>setTheme("light")}>Light</button>
          <button className="btn btn--ghost" onClick={()=>setTheme("dark")}>Dark</button>
          <button className="btn btn--ghost" onClick={()=>setTheme("sage")}>Sage</button>
        </div>
      </header>

      <main style={{maxWidth:960, margin:"20px auto", padding:"0 16px"}}>
        <section className="card" style={{padding:16}}>
          <h2 className="section-title">빠른 분석</h2>
          <button className="btn btn--primary">분석</button>
        </section>
      </main>
    </div>
  );
}
