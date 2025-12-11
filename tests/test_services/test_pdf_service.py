import pytest
import io
from src.resume_matcher.services.pdf_service import (
    extract_text_from_pdf,
    clean_text,
    PDFExtractionError,
)


def test_clean_text_removes_extra_whitespace():
    text = "Hello    world\n\n\n\nTest"
    result = clean_text(text)
    assert "    " not in result
    assert result == "Hello world\n\nTest"


def test_clean_text_strips_edges():
    text = "   Hello world   "
    result = clean_text(text)
    assert result == "Hello world"


def test_extract_text_invalid_file():
    fake_file = io.BytesIO(b"not a pdf")
    with pytest.raises(PDFExtractionError):
        extract_text_from_pdf(fake_file)