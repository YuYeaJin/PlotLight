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
    <div
      className="field"
      style={{
        display: "flex",
        alignItems: "center",
        gap: 8,
        width: "100%",
        maxWidth: "100%",
        minWidth: 0,            // 줄어들 수 있게
        boxSizing: "border-box" // 패딩/보더 포함 폭 계산
      }}
    >
      {/* 표시용 클릭 타겟 */}
      <div
        id={`${uid}-display`}
        className={`field__display ${fileName ? "" : "field__display--placeholder"}`}
        onClick={openDialog}
        aria-live="polite"
        style={{
          flex: 1,
          minWidth: 0,          // 내부 텍스트가 길어도 줄어듦
          overflow: "hidden",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
          cursor: "pointer"
        }}
      >
        {fileName ? `선택됨: ${fileName}` : placeholder}
      </div>

      {/* 숨김 파일 인풋 */}
      <input
        ref={fileRef}
        type="file"
        accept={accept}
        style={{ position: "absolute", left: -9999, width: 1, height: 1 }}
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) { setFileName(f.name); onPick(f); }
          if (fileRef.current) fileRef.current.value = ""; // 같은 파일 재선택 허용
        }}
      />

      {/* 트리거 버튼 */}
      <button
        type="button"
        className="btn btn--ghost"
        onClick={openDialog}
        style={{ whiteSpace: "nowrap" }} // 버튼 글자 줄바꿈 방지
      >
        파일 선택
      </button>
    </div>
  );
}
