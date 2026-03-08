# Testing Guide - Enhanced Backend

## Running the Enhanced Backend

### Prerequisites
- Python 3.8+
- Dependencies installed (`pip install -r requirements.txt`)

### Start the Server

```bash
cd backend
python main.py
```

Expected output:
```
2026-03-08 14:23:00 - ai_resume_analyzer - INFO - FastAPI application initialized
2026-03-08 14:23:00 - ai_resume_analyzer - INFO - CORS middleware configured
2026-03-08 14:23:00 - ai_resume_analyzer - INFO - Resume routes registered
2026-03-08 14:23:00 - ai_resume_analyzer - INFO - Starting AI Resume Analyzer API Server
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## Test 1: Basic Resume Upload

### Using curl

```bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -H "accept: application/json" \
  -F "file=@/path/to/your/resume.pdf"
```

### Expected Response

```json
{
  "success": true,
  "filename": "resume.pdf",
  "page_count": 2,
  "extracted_text": "John Doe\nSoftware Engineer\n...",
  "message": "Resume successfully processed"
}
```

### Expected Logs

Terminal 1 (Server):
```
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - Resume upload request received - Filename: resume.pdf, Timestamp: 2026-03-08T14:23:45.123456
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - File validation passed for resume.pdf. Size: 0.50MB
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - Resume file saved temporarily: /tmp/xyz123/resume.pdf
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - Starting PDF analysis for resume.pdf
2026-03-08 14:23:45 - ai_resume_analyzer.services.resume_parser - INFO - Starting text extraction from PDF: resume.pdf
2026-03-08 14:23:45 - ai_resume_analyzer.services.resume_parser - INFO - PDF loaded successfully. Total pages: 2
2026-03-08 14:23:46 - ai_resume_analyzer.services.resume_parser - DEBUG - Extracted text from page 1/2
2026-03-08 14:23:46 - ai_resume_analyzer.services.resume_parser - DEBUG - Extracted text from page 2/2
2026-03-08 14:23:46 - ai_resume_analyzer.services.resume_parser - INFO - Cleaning extracted text from resume.pdf
2026-03-08 14:23:46 - ai_resume_analyzer.services.resume_parser - INFO - Text extraction and cleaning completed for resume.pdf. Characters: 5000, Words: 890, Paragraphs: 12
2026-03-08 14:23:46 - ai_resume_analyzer - INFO - Resume processing completed successfully for resume.pdf. Pages: 2, Text length: 5000 characters
```

### Check Logs

Terminal 2:
```bash
# Watch app log in real-time
tail -f logs/app.log

# View error log (should be empty for success)
cat logs/error.log
```

---

## Test 2: Text Cleaning Verification

### Create a test script: `test_text_cleaner.py`

```python
from services.text_cleaner import TextCleaner

# Test 1: Basic cleaning
print("=" * 60)
print("Test 1: Basic Text Cleaning")
print("=" * 60)

raw_text = """John   Doe


Senior   Software   Engineer  


Experience
-   Python
-   JavaScript  
-   AWS  """

print("RAW TEXT:")
print(repr(raw_text))
print("\n" + "-" * 60 + "\n")

cleaned = TextCleaner.clean_resume_text(raw_text)
print("CLEANED TEXT:")
print(repr(cleaned))
print("\n" + "-" * 60 + "\n")

# Test 2: Statistics
print("TEXT STATISTICS:")
stats = TextCleaner.get_text_statistics(cleaned)
for key, value in stats.items():
    print(f"  {key}: {value}")
print("\n" + "-" * 60 + "\n")

# Test 3: Aggressive cleaning
print("Test 2: Aggressive Cleaning (single paragraph)")
print("-" * 60)

aggressive = TextCleaner.clean_resume_text_aggressive(raw_text)
print("AGGRESSIVE CLEANED:")
print(repr(aggressive))
print("\n" + "-" * 60 + "\n")

# Test 4: Empty/None handling
print("Test 3: Edge Cases")
print("-" * 60)

empty = TextCleaner.clean_resume_text("")
print(f"Empty string result: {repr(empty)}")

none_result = TextCleaner.clean_resume_text(None)
print(f"None result: {repr(none_result)}")

spaces_only = TextCleaner.clean_resume_text("   \n\n   ")
print(f"Spaces only result: {repr(spaces_only)}")
```

### Run the test

```bash
cd backend
python test_text_cleaner.py
```

### Expected Output

```
============================================================
Test 1: Basic Text Cleaning
============================================================
RAW TEXT:
'John   Doe\n\n\nSenior   Software   Engineer  \n\nExperience\n-   Python\n-   JavaScript  \n-   AWS  '

------------------------------------------------------------

CLEANED TEXT:
'John Doe\nSenior Software Engineer\nExperience\n- Python\n- JavaScript\n- AWS'

------------------------------------------------------------
TEXT STATISTICS:
  character_count: 87
  word_count: 15
  line_count: 6
  paragraph_count: 4

------------------------------------------------------------
Test 2: Aggressive Cleaning (single paragraph)
------------------------------------------------------------
AGGRESSIVE CLEANED:
'John Doe Senior Software Engineer Experience - Python - JavaScript - AWS'

------------------------------------------------------------
Test 3: Edge Cases
------------------------------------------------------------
Empty string result: ''
None result: ''
Spaces only result: ''
```

---

## Test 3: Error Handling Tests

### Test 3.1: Invalid File Type

```bash
# Create a text file
echo "This is not a PDF" > test.txt

# Try to upload it
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@test.txt"
```

### Expected Response

```json
{
  "detail": "Invalid file type. Please upload a PDF file."
}
```

### Expected Logs

```
2026-03-08 14:24:15 - ai_resume_analyzer - INFO - Resume upload request received - Filename: test.txt
2026-03-08 14:24:15 - ai_resume_analyzer - WARNING - Invalid file type uploaded: test.txt. Expected PDF.
```

### Test 3.2: File Too Large

```bash
# Create a large file (>10MB)
dd if=/dev/zero bs=1M count=11 of=large.pdf

# Try to upload it
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@large.pdf"
```

### Expected Response

```json
{
  "detail": "File too large. Maximum size is 10MB, got 11.00MB"
}
```

### Expected Logs

```
2026-03-08 14:24:30 - ai_resume_analyzer - INFO - Resume upload request received - Filename: large.pdf
2026-03-08 14:24:30 - ai_resume_analyzer - WARNING - File size exceeded for large.pdf: 11.00MB (max 10MB)
```

### Test 3.3: Non-existent File (Simulated)

Create a test script: `test_parser_errors.py`

```python
from services.resume_parser import ResumeParser
from utils.logger import get_logger

logger = get_logger(__name__)

parser = ResumeParser()

# Test 1: File not found
print("Test 1: File not found")
print("-" * 60)
try:
    parser.extract_text_from_pdf("/nonexistent/file.pdf")
except FileNotFoundError as e:
    print(f"Caught error: {e}")

print("\n" + "-" * 60)

# Test 2: Invalid file type
print("Test 2: Invalid file type")
print("-" * 60)
try:
    parser.extract_text_from_pdf("test.txt")
except ValueError as e:
    print(f"Caught error: {e}")
```

### Run the test

```bash
python test_parser_errors.py
```

### Expected Output

```
Test 1: File not found
------------------------------------------------------------
Caught error: PDF file not found: /nonexistent/file.pdf

------------------------------------------------------------
Test 2: Invalid file type
------------------------------------------------------------
Caught error: File must be a PDF. Got: .txt
```

### Expected Logs

```
2026-03-08 14:24:45 - test_parser_errors - INFO - Starting text extraction from PDF: /nonexistent/file.pdf
2026-03-08 14:24:45 - services.resume_parser - ERROR - PDF file not found: /nonexistent/file.pdf
2026-03-08 14:24:45 - test_parser_errors - INFO - Starting text extraction from PDF: test.txt
2026-03-08 14:24:45 - services.resume_parser - ERROR - Invalid file type for test.txt: .txt
```

---

## Test 4: Log File Inspection

### View All Logs

```bash
# View last 50 lines of app log
tail -50 logs/app.log

# View all errors
cat logs/error.log

# Count log entries
wc -l logs/app.log

# Search for specific filename
grep "resume.pdf" logs/app.log

# Show only INFO level
grep "INFO" logs/app.log

# Show only ERROR level
grep "ERROR" logs/app.log
```

### Example Log Analysis

```bash
# Find slowest requests (by timestamp difference)
grep "upload request received\|completed successfully" logs/app.log

# Count successful vs failed
echo "Successful:"
grep "completed successfully" logs/app.log | wc -l
echo "Failed:"
grep "ERROR\|WARNING" logs/app.log | wc -l

# Find all files processed
grep -o "Filename: [^,]*" logs/app.log | sort | uniq -c
```

---

## Test 5: Integration Test (Python)

Create: `test_integration.py`

```python
import requests
import json
from pathlib import Path
import time

BASE_URL = "http://localhost:8000"

def test_upload_resume(file_path):
    """Test uploading a resume"""
    print(f"\nTesting upload of: {file_path}")
    print("-" * 60)
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/upload-resume", files=files)
        elapsed_time = time.time() - start_time
    
    print(f"Status Code: {response.status_code}")
    print(f"Time Elapsed: {elapsed_time:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Filename: {data['filename']}")
        print(f"Pages: {data['page_count']}")
        print(f"Text Length: {len(data['extracted_text'])} characters")
        print(f"Message: {data['message']}")
        
        # Show first 200 chars of extracted text
        print(f"\nExtracted Text Preview:")
        print(data['extracted_text'][:200] + "...\n")
    else:
        print(f"Error: {response.json()}")

def test_health_check():
    """Test health check endpoint"""
    print("\nTesting health check endpoint")
    print("-" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_root_endpoint():
    """Test root endpoint"""
    print("\nTesting root endpoint")
    print("-" * 60)
    
    response = requests.get(f"{BASE_URL}/")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Message: {data['message']}")
    print(f"Version: {data['version']}")
    print(f"Endpoints:")
    for endpoint, path in data['endpoints'].items():
        print(f"  - {endpoint}: {path}")

if __name__ == "__main__":
    print("=" * 60)
    print("AI Resume Analyzer - Integration Tests")
    print("=" * 60)
    
    # Test endpoints
    test_health_check()
    test_root_endpoint()
    
    # Test upload (if file exists)
    resume_path = Path("/path/to/resume.pdf")
    if resume_path.exists():
        test_upload_resume(str(resume_path))
    else:
        print(f"\nSkipping upload test - {resume_path} not found")
    
    print("\n" + "=" * 60)
    print("Integration tests completed!")
    print("=" * 60)
```

### Run the integration test

```bash
python test_integration.py
```

---

## Test 6: Performance Monitoring via Logs

### Create a log analysis script: `analyze_logs.py`

```python
import re
from datetime import datetime
from pathlib import Path

def analyze_app_logs():
    """Analyze app.log for insights"""
    
    log_file = Path("logs/app.log")
    
    if not log_file.exists():
        print("No logs found. Run the server first.")
        return
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    print("\n" + "=" * 60)
    print("LOG ANALYSIS")
    print("=" * 60)
    
    # Count by level
    print("\nLog Level Distribution:")
    levels = {}
    for line in lines:
        for level in ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']:
            if level in line:
                levels[level] = levels.get(level, 0) + 1
                break
    
    for level in sorted(levels.keys()):
        print(f"  {level}: {levels[level]}")
    
    # Find all uploaded files
    print("\nUploaded Files:")
    uploaded = set()
    for line in lines:
        match = re.search(r'Filename: ([^,\s]+)', line)
        if match:
            uploaded.add(match.group(1))
    
    for filename in sorted(uploaded):
        print(f"  - {filename}")
    
    # Summary statistics
    print("\nRequest Statistics:")
    requests = [line for line in lines if "Resume upload request received" in line]
    successful = [line for line in lines if "processing completed successfully" in line]
    errors = [line for line in lines if "ERROR" in line]
    
    print(f"  Total Requests: {len(requests)}")
    print(f"  Successful: {len(successful)}")
    print(f"  Errors: {len(errors)}")
    print(f"  Success Rate: {len(successful)/len(requests)*100:.1f}%" if requests else "  N/A")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    analyze_app_logs()
```

### Run the analysis

```bash
python analyze_logs.py
```

---

## Checklist for Testing

- [ ] Server starts without errors
- [ ] Console shows startup logs
- [ ] Health endpoint returns 200
- [ ] API docs available at `/docs`
- [ ] Can upload valid PDF
- [ ] Response contains cleaned text
- [ ] Text cleaning works correctly
- [ ] Statistics are accurate
- [ ] Invalid file types rejected
- [ ] Large files rejected with 413
- [ ] Logs written to `logs/app.log`
- [ ] Errors logged to `logs/error.log`
- [ ] Performance is acceptable (<5s per resume)
- [ ] Multiple requests logged sequentially
- [ ] Error messages are clear and helpful

---

## Troubleshooting

### Q: "logs directory not found"
**A**: Run the server once, it creates the directory automatically.

### Q: "Module not found: utils.logger"
**A**: Make sure you're running from the `backend/` directory.

### Q: Logs not appearing in console
**A**: Check the logging level in `utils/logger.py`. Make sure it's not set to CRITICAL.

### Q: Very slow response time
**A**: Check the PDF complexity and size. Large/complex PDFs take longer to process.

---

This comprehensive testing suite verifies both the text cleaning functionality and logging system work correctly together!
