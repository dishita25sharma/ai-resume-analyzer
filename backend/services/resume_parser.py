"""
Resume Parser Service
Handles PDF parsing and text extraction using pdfplumber
"""

import pdfplumber
from pathlib import Path
from typing import List, Optional
from utils.logger import get_logger
from services.text_cleaner import TextCleaner

logger = get_logger(__name__)


class ResumeParser:
    """
    Service to extract text from PDF resume files
    """

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract text from all pages of a PDF file and clean it for LLM processing.

        Args:
            file_path: Path to the PDF file

        Returns:
            Combined, cleaned text from all pages suitable for LLM processing

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not a valid PDF or is corrupted
        """
        # Verify file exists
        path = Path(file_path)
        if not path.exists():
            logger.error(f"PDF file not found: {file_path}")
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        # Verify it's a PDF
        if path.suffix.lower() != ".pdf":
            logger.error(f"Invalid file type for {file_path}: {path.suffix}")
            raise ValueError(f"File must be a PDF. Got: {path.suffix}")

        try:
            logger.info(f"Starting text extraction from PDF: {path.name}")
            
            # Open PDF and extract text from all pages
            extracted_text = []

            with pdfplumber.open(file_path) as pdf:
                page_count = len(pdf.pages)
                logger.info(f"PDF loaded successfully. Total pages: {page_count}")
                
                # Extract text from each page
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        extracted_text.append(text)
                        logger.debug(f"Extracted text from page {page_num}/{page_count}")

                # Return combined text from all pages
                combined_text = "\n".join(extracted_text)

                if not combined_text.strip():
                    logger.error(f"No text could be extracted from {path.name}")
                    raise ValueError("No text could be extracted from the PDF")

                # Clean the extracted text for LLM processing
                logger.info(f"Cleaning extracted text from {path.name}")
                cleaned_text = TextCleaner.clean_resume_text(combined_text)
                
                # Get text statistics
                stats = TextCleaner.get_text_statistics(cleaned_text)
                logger.info(
                    f"Text extraction and cleaning completed for {path.name}. "
                    f"Characters: {stats['character_count']}, "
                    f"Words: {stats['word_count']}, "
                    f"Paragraphs: {stats['paragraph_count']}"
                )

                return cleaned_text

        except pdfplumber.exceptions.PDFException as e:
            logger.error(f"PDF parsing error for {path.name}: {str(e)}")
            raise ValueError(f"Error reading PDF file: {str(e)}")
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error while parsing {path.name}: {str(e)}")
            raise ValueError(f"Unexpected error while parsing PDF: {str(e)}")

    @staticmethod
    def get_page_count(file_path: str) -> int:
        """
        Get the number of pages in a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            Number of pages in the PDF

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not a valid PDF
        """
        path = Path(file_path)
        if not path.exists():
            logger.error(f"PDF file not found for page count: {file_path}")
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        try:
            with pdfplumber.open(file_path) as pdf:
                page_count = len(pdf.pages)
                logger.debug(f"Retrieved page count for {path.name}: {page_count} pages")
                return page_count
        except Exception as e:
            logger.error(f"Error getting page count for {path.name}: {str(e)}")
            raise ValueError(f"Error reading PDF file: {str(e)}")
