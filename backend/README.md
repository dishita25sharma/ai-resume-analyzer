# AI Resume Analyzer - Backend

Backend API for the AI Resume Analyzer application built with FastAPI and pdfplumber.

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── api/
│   ├── __init__.py
│   └── resume_routes.py    # Resume API endpoints
├── services/
│   ├── __init__.py
│   └── resume_parser.py    # PDF parsing and text extraction
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## File Responsibilities

### `main.py`
- **Purpose**: FastAPI application initialization and configuration
- **Responsibilities**:
  - Creates the FastAPI app instance
  - Configures CORS middleware for cross-origin requests
  - Registers API routers (resume routes)
  - Provides health check and root endpoints
  - Entry point for running the server

### `api/resume_routes.py`
- **Purpose**: API endpoint definitions and HTTP request handling
- **Responsibilities**:
  - Defines the `POST /api/upload-resume` endpoint
  - Handles file validation (type, size)
  - Manages file upload and temporary storage
  - Calls the resume parser service
  - Returns structured API responses with error handling

### `services/resume_parser.py`
- **Purpose**: Core business logic for PDF processing
- **Responsibilities**:
  - Extracts text from PDF files using pdfplumber
  - Provides `extract_text_from_pdf()` method for text extraction
  - Provides `get_page_count()` method for metadata
  - Handles PDF-specific errors and validation
  - Returns clean, processed text content

## API Request Flow

```
User Request
    ↓
POST /api/upload-resume (main.py router)
    ↓
resume_routes.upload_resume() (api/resume_routes.py)
    ├─ Validate file type (.pdf only)
    ├─ Validate file size (max 10MB)
    ├─ Save file temporarily
    ↓
ResumeParser.get_page_count() (services/resume_parser.py)
    ↓
ResumeParser.extract_text_from_pdf() (services/resume_parser.py)
    ├─ Open PDF with pdfplumber
    ├─ Extract text from each page
    ├─ Combine and return text
    ↓
Return JSON Response (api/resume_routes.py)
    ↓
User receives extracted content + metadata
```

## Setup Instructions

### 1. Install Dependencies

Navigate to the backend directory and install required packages:

```bash
cd backend
pip install -r requirements.txt
```

**Dependencies**:
- `fastapi` - Modern web framework for building APIs
- `uvicorn` - ASGI server to run FastAPI
- `pdfplumber` - PDF text extraction library
- `pydantic` - Data validation using Python type hints
- `python-multipart` - Required for file upload handling

### 2. Run the Server

Start the FastAPI development server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3. Verify the Server

Open your browser and visit:
- API Root: http://localhost:8000/
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Testing the API

### Using curl

**1. Upload a Resume:**

```bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -H "accept: application/json" \
  -F "file=@/path/to/resume.pdf"
```

**Example Response:**
```json
{
  "success": true,
  "filename": "resume.pdf",
  "page_count": 2,
  "extracted_text": "John Doe\nSoftware Engineer\n...",
  "message": "Resume successfully processed"
}
```

### Using Postman

1. **Open Postman** and create a new request
2. **Set request type** to `POST`
3. **Enter URL**: `http://localhost:8000/api/upload-resume`
4. **Go to Body tab** → Select `form-data`
5. **Add key**: `file` (type: `File`)
6. **Select a PDF file** from your computer
7. **Click Send**

### Using Python

```python
import requests

# Upload resume
with open('/path/to/resume.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/upload-resume', files=files)

# Print response
print(response.json())
```

### Using JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/upload-resume', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

## API Endpoints

### POST /api/upload-resume

Upload and process a resume PDF.

**Request**:
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body**: 
  - `file` (required): PDF file

**Response** (Success - 200):
```json
{
  "success": true,
  "filename": "resume.pdf",
  "page_count": 2,
  "extracted_text": "Full text content from resume...",
  "message": "Resume successfully processed"
}
```

**Response** (Error - 400):
```json
{
  "detail": "Invalid file type. Please upload a PDF file."
}
```

**Response** (Error - 413):
```json
{
  "detail": "File too large. Maximum size is 10MB, got 15.50MB"
}
```

## Error Handling

The API handles the following error scenarios:

| Error | Status Code | Reason |
|-------|------------|--------|
| Invalid file type | 400 | File is not a PDF |
| File too large | 413 | Exceeds 10MB limit |
| Invalid PDF | 400 | PDF is corrupted or empty |
| No text extracted | 400 | PDF contains no extractable text |
| Internal error | 500 | Unexpected server error |

## Future Extensions

This architecture is designed for easy extension:

1. **AI Processing**: Add LLM analysis in a new service (`services/llm_analyzer.py`)
2. **Database**: Store parsed resumes and analysis results
3. **Authentication**: Add user authentication to `/api/auth/` routes
4. **Async Processing**: Use Celery for background resume analysis
5. **Caching**: Cache extracted text for frequently uploaded resumes

## Notes

- Uploaded files are stored in temporary directories and automatically cleaned up
- The maximum file size is limited to 10MB for security
- CORS is currently open (`allow_origins=["*"]`) - configure this for production
- The API uses synchronous file operations; consider async operations for high traffic

---

For questions or issues, please refer to the main project README.
