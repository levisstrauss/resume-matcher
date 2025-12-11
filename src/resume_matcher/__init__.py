# from .services.pdf_service import extract_text_from_pdf, PDFExtractionError
# from .services.embedding_service import get_embedding, get_embeddings_batch, EmbeddingError
# from .resume_service import (
#     create_resume,
#     get_resume,
#     get_resume_or_404,
#     get_resumes,
#     delete_resume,
#     regenerate_embedding,
#     ResumeNotFoundError,
# )
# from .job_service import (
#     create_job,
#     get_job,
#     get_job_or_404,
#     get_jobs,
#     update_job,
#     delete_job,
#     JobNotFoundError,
# )
# from .match_service import (
#     find_matching_jobs,
#     find_matching_resumes,
#     MatchError,
# )
#
# __all__ = [
#     "extract_text_from_pdf",
#     "PDFExtractionError",
#     "get_embedding",
#     "get_embeddings_batch",
#     "EmbeddingError",
#     "create_resume",
#     "get_resume",
#     "get_resume_or_404",
#     "get_resumes",
#     "delete_resume",
#     "regenerate_embedding",
#     "ResumeNotFoundError",
#     "create_job",
#     "get_job",
#     "get_job_or_404",
#     "get_jobs",
#     "update_job",
#     "delete_job",
#     "JobNotFoundError",
#     "find_matching_jobs",
#     "find_matching_resumes",
#     "MatchError",
# ]


from .services.pdf_service import extract_text_from_pdf, PDFExtractionError
from .services.embedding_service import get_embedding, get_embeddings_batch, EmbeddingError
from .services.resume_service import (  # <--- Changed to .services.resume_service
    create_resume,
    get_resume,
    get_resume_or_404,
    get_resumes,
    delete_resume,
    regenerate_embedding,
    ResumeNotFoundError,
)
from .services.job_service import (     # <--- Changed to .services.job_service
    create_job,
    get_job,
    get_job_or_404,
    get_jobs,
    update_job,
    delete_job,
    JobNotFoundError,
)
from .services.match_service import (   # <--- Changed to .services.match_service
    find_matching_jobs,
    find_matching_resumes,
    MatchError,
)

__all__ = [
    "extract_text_from_pdf",
    "PDFExtractionError",
    "get_embedding",
    "get_embeddings_batch",
    "EmbeddingError",
    "create_resume",
    "get_resume",
    "get_resume_or_404",
    "get_resumes",
    "delete_resume",
    "regenerate_embedding",
    "ResumeNotFoundError",
    "create_job",
    "get_job",
    "get_job_or_404",
    "get_jobs",
    "update_job",
    "delete_job",
    "JobNotFoundError",
    "find_matching_jobs",
    "find_matching_resumes",
    "MatchError",
]