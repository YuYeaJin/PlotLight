// src/pages/QuickAnalyze.tsx
import { useState } from "react";
import FileInlinePicker from "../components/FileInlinePicker";

type Metric = { name: string; value: number; unit?: string | null; zscore?: number | null; note?: string | null };
type EvidenceItem = { source_id: string; snippet: string; score?: number | null; meta?: any };
type SectionScore = { label: string; score: number; metrics: Metric[]; evidences?: EvidenceItem[] };
type AnalyzeRunResponse = {
  total_score: number;
  strengths: string[];
  improvements: string[];
  sections: SectionScore[];
  manuscript_id?: string | null;
  title?: string | null;
  analyzed_at?: string;
  processing_ms?: number;
  persisted?: boolean;
};

type QuickAnalyzeProps = {
  defaultPersist?: boolean;
  defaultSaveReport?: boolean;
};


const API = import.meta.env.VITE_API_BASE as string;

export default function QuickAnalyze({
  defaultPersist = true,
  defaultSaveReport = false,
}: QuickAnalyzeProps) {

  const [file, setFile] = useState<File | null>(null);
  const [persist, setPersist] = useState(defaultPersist);
  const [saveReport, setSaveReport] = useState(defaultSaveReport);
  const [loading, setLoading] = useState(false);
  const [resp, setResp] = useState<AnalyzeRunResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    setLoading(true); setError(null); setResp(null);

    const fd = new FormData();
    fd.append("file", file);
    fd.append("persist", String(persist));
    fd.append("save_report", String(saveReport));

    try {
      const r = await fetch(`${API}/files/analyze/quick`, { method: "POST", body: fd });
      if (!r.ok) throw new Error(`${r.status} ${r.statusText}: ${await r.text()}`);
      setResp(await r.json());
    } catch (err: any) {
      setError(err?.message ?? String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 960, margin: "20px auto", padding: "0 16px" }}>
      <section className="card" style={{ padding: 16 }}>
        <h2 className="section-title">원문 분석</h2>

        <form onSubmit={onSubmit}>
          {/* 체크박스 줄 */}
          <div style={{ display: "flex", gap: 16, alignItems: "center", flexWrap: "wrap", marginBottom: 12 }}>
            <button type="submit" className="btn btn--primary" disabled={loading || !file}>
              {loading ? "분석 중…" : "분석"}
            </button>
          </div>

          {/* 파일 설명 + 파일 선택 (오버플로 방지 스타일) */}
          <div
            style={{
              width: "100%",
              boxSizing: "border-box",
            }}
          >
            <FileInlinePicker
              accept=".txt,.md,.pdf,.docx"
              onPick={(picked) => { setFile(picked); setError(null); }}
            />
          </div>
        </form>
      </section>

      {error && <pre style={{ color: "crimson", marginTop: 12, whiteSpace: "pre-wrap" }}>{error}</pre>}

      {resp && (
        <div style={{ marginTop: 16 }}>
          <div style={{ fontWeight: 600 }}>총점: {resp.total_score}</div>
          {resp.title && <div>제목: {resp.title}</div>}
          {resp.manuscript_id && <div>manuscript_id: {resp.manuscript_id}</div>}

          <div style={{ marginTop: 12 }}>
            <strong>강점</strong>
            <ul>{resp.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul>
            <strong>개선점</strong>
            <ul>{resp.improvements.map((s, i) => <li key={i}>{s}</li>)}</ul>
          </div>

          {resp.sections.map((sec, i) => (
            <div key={i} style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 12, marginTop: 8 }}>
              <div style={{ fontWeight: 600 }}>{sec.label} — {sec.score}</div>
              <ul style={{ margin: 0 }}>
                {sec.metrics.map((m, j) => (
                  <li key={j}>{m.name}: {m.value}{m.unit ? ` ${m.unit}` : ""}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
