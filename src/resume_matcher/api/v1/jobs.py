import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...api.deps import get_db
from ...schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobDetail,
)
from ...services import (
    create_job,
    get_job,
    get_jobs,
    update_job,
    delete_job,
    JobNotFoundError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/", response_model=JobResponse, status_code=201)
def create_new_job(
        job_data: JobCreate,
        db: Session = Depends(get_db),
):
    """
    Create a new job posting.

    The job description will be automatically embedded for similarity matching.
    """
    job = create_job(db, job_data)
    return JobResponse(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        created_at=job.created_at,
        has_embedding=job.embedding is not None,
    )


@router.get("/", response_model=List[JobResponse])
def list_jobs(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    """Get all jobs with pagination."""
    jobs = get_jobs(db, skip=skip, limit=limit)
    return [
        JobResponse(
            id=j.id,
            title=j.title,
            company=j.company,
            location=j.location,
            description=j.description,
            created_at=j.created_at,
            has_embedding=j.embedding is not None,
        )
        for j in jobs
    ]


@router.get("/{job_id}", response_model=JobDetail)
def get_job_detail(
        job_id: int,
        db: Session = Depends(get_db),
):
    """Get detailed information about a specific job."""
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobDetail(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        created_at=job.created_at,
        has_embedding=job.embedding is not None,
        description_preview=job.description[:500] + "..." if len(job.description) > 500 else job.description,
    )


@router.patch("/{job_id}", response_model=JobResponse)
def update_existing_job(
        job_id: int,
        job_data: JobUpdate,
        db: Session = Depends(get_db),
):
    """Update a job posting."""
    try:
        job = update_job(db, job_id, job_data)
        return JobResponse(
            id=job.id,
            title=job.title,
            company=job.company,
            location=job.location,
            description=job.description,
            created_at=job.created_at,
            has_embedding=job.embedding is not None,
        )
    except JobNotFoundError:
        raise HTTPException(status_code=404, detail="Job not found")


@router.delete("/{job_id}", status_code=204)
def remove_job(
        job_id: int,
        db: Session = Depends(get_db),
):
    """Delete a job posting."""
    if not delete_job(db, job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    return None