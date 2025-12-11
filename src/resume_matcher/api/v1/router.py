from fastapi import APIRouter

from .resumes import router as resumes_router
from .jobs import router as jobs_router
from .matches import router as matches_router

api_router = APIRouter()

api_router.include_router(resumes_router)
api_router.include_router(jobs_router)
api_router.include_router(matches_router)