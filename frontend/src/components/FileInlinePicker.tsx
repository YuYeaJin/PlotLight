import { useId, useRef, useState } from "react";

export default function FileInlinePicker({
  placeholder = "파일 설명(선택)",
  accept = ".txt,.md,.docx,.pdf",
  onPick,
}: {
  placeholder?: string;
  accept?: string;
  onPick: (file: File) => void;
}) {
  const uid = useId();
  const fileRef = useRef<HTMLInputElement>(null);
  const [fileName, setFileName] = useState("");

  const openDialog = () => fileRef.current?.click();

  return (
    <div className="field">
      {/* ✅ 편집 불가: 단순 표시용 영역 (클릭 시 파일 선택 창 열림) */}
      <div
        id={`${uid}-display`}
        className={`field__display ${fileName ? "" : "field__display--placeholder"}`}
        onClick={openDialog}
        aria-live="polite"
      >
        {fileName ? `선택됨: ${fileName}` : placeholder}
      </div>

      {/* 숨김 파일 인풋: 실제 다이얼로그 트리거 대상 */}
      <input
        ref={fileRef}
        type="file"
        accept={accept}
        style={{ position: "absolute", left: "-9999px", width: 1, height: 1 }}
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) { setFileName(f.name); onPick(f); }
          if (fileRef.current) fileRef.current.value = ""; // 같은 파일 재선택 허용
        }}
      />

      {/* 우측 버튼: 명시적으로도 열 수 있게 */}
      <button type="button" className="field__action" onClick={openDialog}>
        파일 선택
      </button>
    </div>
  );
}
