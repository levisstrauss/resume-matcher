import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...api.deps import get_db
from ...schemas.match import MatchResponse, MatchRequest
from ...services import (
    find_matching_jobs,
    find_matching_resumes,
    ResumeNotFoundError,
    JobNotFoundError,
    MatchError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/resume/{resume_id}", response_model=MatchResponse)
def match_resume_to_jobs(
        resume_id: int,
        top_k: int = Query(default=10, ge=1, le=50),
        min_score: float = Query(default=0.0, ge=0.0, le=1.0),
        db: Session = Depends(get_db),
):
    """
    Find the best matching jobs for a resume.

    - **resume_id**: ID of the resume to match
    - **top_k**: Number of top matches to return (1-50)
    - **min_score**: Minimum similarity score threshold (0.0-1.0)
    """
    try:
        matches = find_matching_jobs(
            db,
            resume_id=resume_id,
            top_k=top_k,
            min_score=min_score,
        )
        return matches
    except ResumeNotFoundError:
        raise HTTPException(status_code=404, detail="Resume not found")
    except MatchError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/job/{job_id}/candidates")
def match_job_to_resumes(
        job_id: int,
        top_k: int = Query(default=10, ge=1, le=50),
        min_score: float = Query(default=0.0, ge=0.0, le=1.0),
        db: Session = Depends(get_db),
):
    """
    Find the best matching resumes (candidates) for a job.

    - **job_id**: ID of the job to match
    - **top_k**: Number of top matches to return (1-50)
    - **min_score**: Minimum similarity score threshold (0.0-1.0)
    """
    try:
        matches = find_matching_resumes(
            db,
            job_id=job_id,
            top_k=top_k,
            min_score=min_score,
        )
        return {
            "job_id": job_id,
            "total_candidates": len(matches),
            "candidates": matches,
        }
    except JobNotFoundError:
        raise HTTPException(status_code=404, detail="Job not found")
    except MatchError as e:
        raise HTTPException(status_code=400, detail=str(e))