import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.job import Job
from ..schemas.job import JobCreate, JobUpdate
from .embedding_service import get_embedding, EmbeddingError

logger = logging.getLogger(__name__)


class JobNotFoundError(Exception):
    """Raised when a job is not found."""
    pass


def create_job(db: Session, job_data: JobCreate) -> Job:
    """
    Create a new job and generate its embedding.

    Args:
        db: Database session
        job_data: Job creation data

    Returns:
        Created Job object
    """
    job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        description=job_data.description,
    )

    # Generate embedding from title + description
    text_for_embedding = f"{job_data.title}\n\n{job_data.description}"

    try:
        embedding = get_embedding(text_for_embedding)
        job.embedding = embedding
        logger.info(f"Generated embedding for job: {job_data.title}")
    except EmbeddingError as e:
        logger.error(f"Failed to generate embedding: {e}")

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_job(db: Session, job_id: int) -> Optional[Job]:
    """Get a job by ID."""
    return db.query(Job).filter(Job.id == job_id).first()


def get_job_or_404(db: Session, job_id: int) -> Job:
    """Get a job by ID or raise error."""
    job = get_job(db, job_id)
    if not job:
        raise JobNotFoundError(f"Job with ID {job_id} not found")
    return job


def get_jobs(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[Job]:
    """Get all jobs with pagination."""
    return db.query(Job).offset(skip).limit(limit).all()


def update_job(db: Session, job_id: int, job_data: JobUpdate) -> Job:
    """Update a job and regenerate embedding if description changed."""
    job = get_job_or_404(db, job_id)

    update_data = job_data.model_dump(exclude_unset=True)
    description_changed = "description" in update_data or "title" in update_data

    for key, value in update_data.items():
        setattr(job, key, value)

    # Regenerate embedding if relevant fields changed
    if description_changed:
        text_for_embedding = f"{job.title}\n\n{job.description}"
        try:
            embedding = get_embedding(text_for_embedding)
            job.embedding = embedding
            logger.info(f"Regenerated embedding for job ID {job_id}")
        except EmbeddingError as e:
            logger.error(f"Failed to regenerate embedding: {e}")

    db.commit()
    db.refresh(job)

    return job


def delete_job(db: Session, job_id: int) -> bool:
    """Delete a job by ID."""
    job = get_job(db, job_id)
    if not job:
        return False

    db.delete(job)
    db.commit()
    return True


def get_jobs_with_embeddings(db: Session) -> List[Job]:
    """Get all jobs that have embeddings."""
    return db.query(Job).filter(Job.embedding.isnot(None)).all()