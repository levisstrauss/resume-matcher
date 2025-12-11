import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..models.resume import Resume
from ..schemas.resume import ResumeCreate
from .embedding_service import get_embedding, EmbeddingError

logger = logging.getLogger(__name__)


class ResumeNotFoundError(Exception):
    """Raised when a resume is not found."""
    pass


def create_resume(db: Session, resume_data: ResumeCreate) -> Resume:
    """
    Create a new resume and generate its embedding.

    Args:
        db: Database session
        resume_data: Resume creation data

    Returns:
        Created Resume object
    """
    # Create resume
    resume = Resume(
        name=resume_data.name,
        email=resume_data.email,
        filename=resume_data.filename,
        raw_text=resume_data.raw_text,
    )

    # Generate embedding
    try:
        embedding = get_embedding(resume_data.raw_text)
        resume.embedding = embedding
        logger.info(f"Generated embedding for resume: {resume_data.name}")
    except EmbeddingError as e:
        logger.error(f"Failed to generate embedding: {e}")
        # Continue without embedding - can be generated later

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_resume(db: Session, resume_id: int) -> Optional[Resume]:
    """Get a resume by ID."""
    return db.query(Resume).filter(Resume.id == resume_id).first()


def get_resume_or_404(db: Session, resume_id: int) -> Resume:
    """Get a resume by ID or raise error."""
    resume = get_resume(db, resume_id)
    if not resume:
        raise ResumeNotFoundError(f"Resume with ID {resume_id} not found")
    return resume


def get_resumes(
        db: Session,
        skip: int = 0,
        limit: int = 100
) -> List[Resume]:
    """Get all resumes with pagination."""
    return db.query(Resume).offset(skip).limit(limit).all()


def delete_resume(db: Session, resume_id: int) -> bool:
    """Delete a resume by ID."""
    resume = get_resume(db, resume_id)
    if not resume:
        return False

    db.delete(resume)
    db.commit()
    return True


def regenerate_embedding(db: Session, resume_id: int) -> Resume:
    """Regenerate embedding for a resume."""
    resume = get_resume_or_404(db, resume_id)

    try:
        embedding = get_embedding(resume.raw_text)
        resume.embedding = embedding
        db.commit()
        db.refresh(resume)
        logger.info(f"Regenerated embedding for resume ID {resume_id}")
    except EmbeddingError as e:
        raise EmbeddingError(f"Failed to regenerate embedding: {e}")

    return resume


def get_resumes_with_embeddings(db: Session) -> List[Resume]:
    """Get all resumes that have embeddings."""
    return db.query(Resume).filter(Resume.embedding.isnot(None)).all()