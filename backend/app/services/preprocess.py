import io
from typing import Optional
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
try:
    from docx import Document
except ImportError:
    Document = None
import chardet

async def extract_text_from_upload(filename: str, data: bytes) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in {"txt", "md", ""}:
        enc = chardet.detect(data).get("encoding") or "utf-8"
        return data.decode(enc, errors="replace")
    if ext == "pdf":
        if not PdfReader:
            raise RuntimeError("pypdf 미설치")
        reader = PdfReader(io.BytesIO(data))
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    if ext == "docx":
        if not Document:
            raise RuntimeError("python-docx 미설치")
        buf = io.BytesIO(data)
        doc = Document(buf)
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError(f"미지원 확장자: .{ext}")
