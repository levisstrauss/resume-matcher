import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from ...api.deps import get_db
from ...schemas.resume import (
    ResumeResponse,
    ResumeDetail,
    ResumeCreate,
    ResumeUploadResponse,
)
from ...services import (
    extract_text_from_pdf,
    PDFExtractionError,
    create_resume,
    get_resume,
    get_resumes,
    delete_resume,
    regenerate_embedding,
    ResumeNotFoundError,
    EmbeddingError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload", response_model=ResumeUploadResponse, status_code=201)
async def upload_resume(
        file: UploadFile = File(...),
        name: str = Form(...),
        email: str = Form(None),
        db: Session = Depends(get_db),
):
    """
    Upload a resume PDF and extract its content.

    - **file**: PDF file of the resume
    - **name**: Name of the candidate
    - **email**: Optional email address
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # Extract text from PDF
    try:
        raw_text = extract_text_from_pdf(file.file)
    except PDFExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Create resume
    resume_data = ResumeCreate(
        name=name,
        email=email,
        filename=file.filename,
        raw_text=raw_text,
    )

    resume = create_resume(db, resume_data)

    return ResumeUploadResponse(
        message="Resume uploaded and processed successfully",
        resume=ResumeResponse(
            id=resume.id,
            name=resume.name,
            email=resume.email,
            filename=resume.filename,
            created_at=resume.created_at,
            has_embedding=resume.embedding is not None,
        )
    )


@router.get("/", response_model=List[ResumeResponse])
def list_resumes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    """Get all resumes with pagination."""
    resumes = get_resumes(db, skip=skip, limit=limit)
    return [
        ResumeResponse(
            id=r.id,
            name=r.name,
            email=r.email,
            filename=r.filename,
            created_at=r.created_at,
            has_embedding=r.embedding is not None,
        )
        for r in resumes
    ]


@router.get("/{resume_id}", response_model=ResumeDetail)
def get_resume_detail(
        resume_id: int,
        db: Session = Depends(get_db),
):
    """Get detailed information about a specific resume."""
    resume = get_resume(db, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return ResumeDetail(
        id=resume.id,
        name=resume.name,
        email=resume.email,
        filename=resume.filename,
        created_at=resume.created_at,
        has_embedding=resume.embedding is not None,
        text_preview=resume.raw_text[:500] + "..." if len(resume.raw_text) > 500 else resume.raw_text,
    )


@router.delete("/{resume_id}", status_code=204)
def remove_resume(
        resume_id: int,
        db: Session = Depends(get_db),
):
    """Delete a resume."""
    if not delete_resume(db, resume_id):
        raise HTTPException(status_code=404, detail="Resume not found")
    return None


@router.post("/{resume_id}/regenerate-embedding", response_model=ResumeResponse)
def regenerate_resume_embedding(
        resume_id: int,
        db: Session = Depends(get_db),
):
    """Regenerate the embedding for a resume."""
    try:
        resume = regenerate_embedding(db, resume_id)
        return ResumeResponse(
            id=resume.id,
            name=resume.name,
            email=resume.email,
            filename=resume.filename,
            created_at=resume.created_at,
            has_embedding=resume.embedding is not None,
        )
    except ResumeNotFoundError:
        raise HTTPException(status_code=404, detail="Resume not found")
    except EmbeddingError as e:
        raise HTTPException(status_code=500, detail=str(e))