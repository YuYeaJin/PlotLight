from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from datetime import datetime

class EvidenceItem(BaseModel):
    source_id: str
    snippet: str
    score: float
    meta: Dict[str, str] = {}

class Metric(BaseModel):
    name: str
    value: float
    unit: Optional[str] = None
    zscore: Optional[float] = None
    note: Optional[str] = None

class SectionScore(BaseModel):
    label: Literal["genre","style","character","causality","market"]
    score: float = Field(..., ge=0, le=100)
    metrics: List[Metric] = []
    evidences: List[EvidenceItem] = []

class AnalyzeRunRequest(BaseModel):
    manuscript_id: str
    options: Dict[str, str] = {}

class AnalyzeRunResponse(BaseModel):
    total_score: float
    strengths: List[str]
    improvements: List[str]
    sections: List[SectionScore]
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)
    manuscript_id: str
    title: Optional[str] = None
