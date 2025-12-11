from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ResumeBase(BaseModel):
    """Base schema for resume data."""
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None


class ResumeCreate(ResumeBase):
    """Schema for creating a resume (used internally after PDF parsing)."""
    filename: str
    raw_text: str


class ResumeResponse(ResumeBase):
    """Schema for resume responses."""
    id: int
    filename: str
    created_at: datetime
    has_embedding: bool = False

    class Config:
        from_attributes = True


class ResumeDetail(ResumeResponse):
    """Detailed resume response including text preview."""
    text_preview: str = Field(..., description="First 500 chars of resume")

    class Config:
        from_attributes = True


class ResumeUploadResponse(BaseModel):
    """Response after uploading a resume."""
    message: str
    resume: ResumeResponse