from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class JobBase(BaseModel):
    """Base schema for job data."""
    title: str = Field(..., min_length=1, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    description: str = Field(..., min_length=10)


class JobCreate(JobBase):
    """Schema for creating a job."""
    pass


class JobUpdate(BaseModel):
    """Schema for updating a job."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    company: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, min_length=10)


class JobResponse(JobBase):
    """Schema for job responses."""
    id: int
    created_at: datetime
    has_embedding: bool = False

    class Config:
        from_attributes = True


class JobDetail(JobResponse):
    """Detailed job response."""
    description_preview: str = Field(..., description="First 500 chars")

    class Config:
        from_attributes = True