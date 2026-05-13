import logging
from typing import Tuple, Optional
from PyPDF2 import PdfReader
import io

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Handles PDF text extraction"""

    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes, max_pages: int = 100) -> Tuple[str, int]:
        """
        Extract text from PDF file bytes

        Args:
            file_bytes: PDF file content as bytes
            max_pages: Maximum number of pages to process

        Returns:
            Tuple of (extracted_text, num_pages)

        Raises:
            ValueError: If PDF is invalid or empty
            Exception: If extraction fails
        """
        try:
            # Create PDF reader from bytes
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PdfReader(pdf_file)

            # Check if PDF has pages
            num_pages = len(pdf_reader.pages)
            if num_pages == 0:
                raise ValueError("PDF file has no pages")

            # Limit pages to process
            pages_to_process = min(num_pages, max_pages)
            logger.info(f"Processing {pages_to_process} of {num_pages} pages")

            # Extract text from all pages
            extracted_text = []
            for page_num in range(pages_to_process):
                try:
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        extracted_text.append(text)
                except Exception as page_error:
                    logger.warning(f"Error extracting text from page {page_num + 1}: {str(page_error)}")
                    continue

            # Combine all extracted text
            full_text = "\n".join(extracted_text)

            # Clean up text
            full_text = PDFProcessor._clean_text(full_text)

            if not full_text or len(full_text.strip()) < 10:
                raise ValueError("No readable text found in PDF")

            logger.info(f"Successfully extracted {len(full_text)} characters from PDF")
            return full_text, num_pages

        except ValueError as ve:
            logger.error(f"ValueError extracting PDF: {str(ve)}")
            raise ValueError(f"PDF extraction error: {str(ve)}")
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean extracted text

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text
        """
        # Remove multiple spaces
        text = " ".join(text.split())

        # Remove multiple newlines
        text = "\n".join(line.strip() for line in text.split("\n") if line.strip())

        # Remove special characters but keep space and common punctuation
        import re
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

        return text.strip()

    @staticmethod
    def validate_pdf_file(filename: str) -> bool:
        """
        Validate if file is PDF

        Args:
            filename: Name of file

        Returns:
            True if valid PDF filename
        """
        return filename.lower().endswith('.pdf') and '.' in filename
