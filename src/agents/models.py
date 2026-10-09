from typing import Optional

from pydantic import BaseModel


class ResearchFindings(BaseModel):
    answered: bool
    overview: Optional[str] = None
    claims: list[dict] = []
    conflicts: list[str] = []
    gaps: list[str] = []
    reason: Optional[str] = None


class DataFindings(BaseModel):
    used: bool
    dataset_path: Optional[str] = None
    profile: Optional[dict] = None
    stats: Optional[dict] = None
    charts: list[dict] = []


class SourceRef(BaseModel):
    id: str
    title: str
    url: str
    year: Optional[int] = None


class UnifiedAnalysis(BaseModel):
    question: str
    research: ResearchFindings
    data: DataFindings
    sources: list[SourceRef] = []
    limitations: list[str] = []
    warnings: list[str] = []
    insights: list[str] = []