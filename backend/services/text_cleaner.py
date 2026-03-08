"""
Text Cleaner Module
Handles text normalization and cleaning for LLM processing
"""

import re
from typing import Optional


class TextCleaner:
    """
    Service to clean and normalize extracted text for LLM processing
    """

    @staticmethod
    def clean_resume_text(text: str) -> str:
        """
        Clean and normalize resume text for LLM processing.

        This function performs the following operations:
        1. Removes excessive whitespace
        2. Normalizes multiple spaces into single space
        3. Normalizes multiple line breaks
        4. Strips leading/trailing whitespace
        5. Returns clean text suitable for LLM processing

        Args:
            text: Raw extracted text from PDF

        Returns:
            Cleaned and normalized text

        Example:
            >>> raw = "John  Doe\\n\\n\\nSoftware  Engineer"
            >>> TextCleaner.clean_resume_text(raw)
            "John Doe\\nSoftware Engineer"
        """
        if not text or not isinstance(text, str):
            return ""

        # Step 1: Remove excessive whitespace (tabs, form feeds, etc.)
        text = re.sub(r'[\t\f\v\r]', ' ', text)

        # Step 2: Normalize multiple spaces into single space
        text = re.sub(r' +', ' ', text)

        # Step 3: Normalize multiple line breaks (preserve single line breaks)
        # Replace 3+ consecutive newlines with 2 newlines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Step 4: Remove spaces before line breaks
        text = re.sub(r' +\n', '\n', text)

        # Step 5: Remove spaces after line breaks
        text = re.sub(r'\n +', '\n', text)

        # Step 6: Strip leading and trailing whitespace
        text = text.strip()

        return text

    @staticmethod
    def clean_resume_text_aggressive(text: str) -> str:
        """
        More aggressive cleaning for specific use cases.

        This removes line breaks and creates a single paragraph,
        useful for certain LLM models that prefer continuous text.

        Args:
            text: Raw extracted text from PDF

        Returns:
            Single paragraph cleaned text
        """
        if not text or not isinstance(text, str):
            return ""

        # Clean using standard method first
        cleaned = TextCleaner.clean_resume_text(text)

        # Replace line breaks with spaces
        cleaned = re.sub(r'\n+', ' ', cleaned)

        # Final normalization
        cleaned = re.sub(r' +', ' ', cleaned)

        return cleaned.strip()

    @staticmethod
    def get_text_statistics(text: str) -> dict:
        """
        Get statistics about the cleaned text.

        Args:
            text: Cleaned resume text

        Returns:
            Dictionary with text statistics
        """
        if not text:
            return {
                "character_count": 0,
                "word_count": 0,
                "line_count": 0,
                "paragraph_count": 0
            }

        lines = text.split('\n')
        paragraphs = [p for p in lines if p.strip()]

        return {
            "character_count": len(text),
            "word_count": len(text.split()),
            "line_count": len(lines),
            "paragraph_count": len(paragraphs)
        }
