from typing import List, Optional
from pydantic import BaseModel, Field


class MatchResult(BaseModel):
    """Single match result."""
    job_id: int
    job_title: str
    company: Optional[str]
    similarity_score: float = Field(..., ge=0, le=1)
    match_percentage: int = Field(..., ge=0, le=100)

    class Config:
        from_attributes = True


class MatchResponse(BaseModel):
    """Response for matching a resume to jobs."""
    resume_id: int
    resume_name: str
    total_jobs_compared: int
    matches: List[MatchResult]


class MatchRequest(BaseModel):
    """Request to find matches for a resume."""
    resume_id: int
    top_k: int = Field(default=10, ge=1, le=50)
    min_score: float = Field(default=0.0, ge=0, le=1)