"""
Resume API Routes
Handles HTTP endpoints for resume upload and processing
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from services.resume_parser import ResumeParser
from utils.logger import get_logger

logger = get_logger(__name__)

# Initialize router
router = APIRouter()

# Response models
class ResumeExtractionResponse(BaseModel):
    """Response model for resume extraction"""
    success: bool
    filename: str
    page_count: int
    extracted_text: str
    message: str


class ErrorResponse(BaseModel):
    """Response model for errors"""
    success: bool
    error: str


@router.post("/upload-resume", response_model=ResumeExtractionResponse)
async def upload_resume(file: UploadFile = File(...)) -> ResumeExtractionResponse:
    """
    Upload and process a resume PDF file.

    This endpoint:
    1. Accepts a PDF file upload
    2. Saves it temporarily
    3. Extracts text using the resume parser service
    4. Returns the extracted content

    Args:
        file: Uploaded PDF file

    Returns:
        ResumeExtractionResponse with extracted text and metadata

    Raises:
        HTTPException: If file validation or processing fails
    """
    
    # Log the resume upload request
    request_timestamp = datetime.now().isoformat()
    logger.info(f"Resume upload request received - Filename: {file.filename}, Timestamp: {request_timestamp}")

    # Validate file type
    if not file.filename.endswith(".pdf"):
        logger.warning(f"Invalid file type uploaded: {file.filename}. Expected PDF.")
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a PDF file."
        )

    # Validate file size (limit to 10MB)
    max_file_size = 10 * 1024 * 1024  # 10MB in bytes
    file_content = await file.read()
    file_size_mb = len(file_content) / (1024 * 1024)
    
    if len(file_content) > max_file_size:
        logger.warning(f"File size exceeded for {file.filename}: {file_size_mb:.2f}MB (max 10MB)")
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is 10MB, got {file_size_mb:.2f}MB"
        )

    logger.info(f"File validation passed for {file.filename}. Size: {file_size_mb:.2f}MB")

    # Create temporary directory and file
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded file temporarily
            temp_file_path = os.path.join(temp_dir, file.filename)

            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(file_content)

            logger.info(f"Resume file saved temporarily: {temp_file_path}")

            # Parse the resume
            parser = ResumeParser()

            # Get page count
            logger.info(f"Starting PDF analysis for {file.filename}")
            page_count = parser.get_page_count(temp_file_path)

            # Extract text
            logger.info(f"Beginning text extraction for {file.filename}")
            extracted_text = parser.extract_text_from_pdf(temp_file_path)

            logger.info(
                f"Resume processing completed successfully for {file.filename}. "
                f"Pages: {page_count}, Text length: {len(extracted_text)} characters"
            )

            # Return success response
            return ResumeExtractionResponse(
                success=True,
                filename=file.filename,
                page_count=page_count,
                extracted_text=extracted_text,
                message="Resume successfully processed"
            )

    except ValueError as e:
        logger.error(f"Validation error processing {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except FileNotFoundError as e:
        logger.error(f"File not found error for {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error processing {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    finally:
        # Clean up file pointer if needed
        await file.close()
        logger.debug(f"File pointer closed for {file.filename}")
