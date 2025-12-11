import fitz  # PyMuPDF
import logging
from typing import BinaryIO

logger = logging.getLogger(__name__)


class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails."""
    pass


def extract_text_from_pdf(file: BinaryIO) -> str:
    """
    Extract text content from a PDF file.

    Args:
        file: File-like object containing PDF data

    Returns:
        Extracted text as a string

    Raises:
        PDFExtractionError: If extraction fails
    """
    try:
        # Read file content
        pdf_bytes = file.read()

        # Open PDF from bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text_parts = []

        for page_num, page in enumerate(doc):
            try:
                text = page.get_text()
                if text.strip():
                    text_parts.append(text)
            except Exception as e:
                logger.warning(f"Failed to extract text from page {page_num}: {e}")
                continue

        doc.close()

        if not text_parts:
            raise PDFExtractionError("No text could be extracted from PDF")

        # Join all text with newlines
        full_text = "\n\n".join(text_parts)

        # Clean up the text
        full_text = clean_text(full_text)

        logger.info(f"Extracted {len(full_text)} characters from PDF")
        return full_text

    except fitz.FileDataError as e:
        raise PDFExtractionError(f"Invalid PDF file: {e}")
    except Exception as e:
        raise PDFExtractionError(f"Failed to extract text: {e}")


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing excessive whitespace.

    Args:
        text: Raw extracted text

    Returns:
        Cleaned text
    """
    import re

    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)

    # Replace multiple newlines with double newline
    text = re.sub(r'\n\s*\n', '\n\n', text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text