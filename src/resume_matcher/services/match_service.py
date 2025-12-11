import logging
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..models.resume import Resume
from ..models.job import Job
from ..schemas.match import MatchResult, MatchResponse
from .resume_service import get_resume_or_404, ResumeNotFoundError
from .job_service import get_jobs_with_embeddings

logger = logging.getLogger(__name__)


class MatchError(Exception):
    """Raised when matching fails."""
    pass


def find_matching_jobs(
        db: Session,
        resume_id: int,
        top_k: int = 10,
        min_score: float = 0.0
) -> MatchResponse:
    """
    Find the best matching jobs for a resume using vector similarity.

    Args:
        db: Database session
        resume_id: ID of the resume to match
        top_k: Number of top matches to return
        min_score: Minimum similarity score threshold

    Returns:
        MatchResponse with ranked job matches
    """
    # Get resume
    resume = get_resume_or_404(db, resume_id)

    if resume.embedding is None:
        raise MatchError(f"Resume {resume_id} has no embedding. Please regenerate it.")

    # Use pgvector's cosine distance operator
    # Note: <=> is cosine distance, so lower is more similar
    # We convert to similarity: 1 - distance
    query = text("""
                 SELECT id,
                        title,
                        company,
                        1 - (embedding <=> :resume_embedding) as similarity
                 FROM jobs
                 WHERE embedding IS NOT NULL
                 ORDER BY embedding <=> :resume_embedding
        LIMIT :limit
                 """)

    result = db.execute(
        query,
        {
            "resume_embedding": str(resume.embedding),
            "limit": top_k * 2  # Get extra to filter by min_score
        }
    )

    matches = []
    for row in result:
        similarity = float(row.similarity)

        if similarity >= min_score:
            matches.append(MatchResult(
                job_id=row.id,
                job_title=row.title,
                company=row.company,
                similarity_score=round(similarity, 4),
                match_percentage=round(similarity * 100)
            ))

    # Limit to top_k after filtering
    matches = matches[:top_k]

    # Get total job count for context
    total_jobs = db.query(Job).filter(Job.embedding.isnot(None)).count()

    return MatchResponse(
        resume_id=resume.id,
        resume_name=resume.name,
        total_jobs_compared=total_jobs,
        matches=matches
    )


def find_matching_resumes(
        db: Session,
        job_id: int,
        top_k: int = 10,
        min_score: float = 0.0
) -> List[dict]:
    """
    Find the best matching resumes for a job.

    Args:
        db: Database session
        job_id: ID of the job to match
        top_k: Number of top matches to return
        min_score: Minimum similarity score threshold

    Returns:
        List of matching resumes with scores
    """
    from .job_service import get_job_or_404

    job = get_job_or_404(db, job_id)

    if job.embedding is None:
        raise MatchError(f"Job {job_id} has no embedding.")

    query = text("""
                 SELECT id,
                        name,
                        email,
                        1 - (embedding <=> :job_embedding) as similarity
                 FROM resumes
                 WHERE embedding IS NOT NULL
                 ORDER BY embedding <=> :job_embedding
        LIMIT :limit
                 """)

    result = db.execute(
        query,
        {
            "job_embedding": str(job.embedding),
            "limit": top_k
        }
    )

    matches = []
    for row in result:
        similarity = float(row.similarity)
        if similarity >= min_score:
            matches.append({
                "resume_id": row.id,
                "name": row.name,
                "email": row.email,
                "similarity_score": round(similarity, 4),
                "match_percentage": round(similarity * 100)
            })

    return matches