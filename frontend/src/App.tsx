import { useState } from "react";

export default function App() {
  const [status, setStatus] = useState<string>("(미확인)");

  const ping = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/health");
      const json = await res.json();
      setStatus(JSON.stringify(json));
    } catch (e) {
      setStatus("접속 실패");
    }
  };

  return (
    <div style={{ padding: 24 }}>
      <h1>PlotLight</h1>
      <p>프론트 OK ✅</p>
      <button onClick={ping}>백엔드 헬스체크</button>
      <div style={{ marginTop: 8 }}>서버 상태: {status}</div>
    </div>
  );
}
