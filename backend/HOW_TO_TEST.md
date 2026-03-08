# 🧪 Testing Guide - Step by Step

## ✅ Prerequisites

Make sure you have:
- Python 3.8+ installed
- Dependencies installed: `pip install -r requirements.txt`
- A PDF file to test with (or we'll help you create one)

---

## 🚀 Test 1: Start the Server

### Step 1.1: Open Terminal
```bash
cd /Users/dishitasharma/Documents/AI_LEARNING/ai-resume-analyzer/backend
python main.py
```

### Expected Output:
```
2026-03-08 14:23:00 - ai_resume_analyzer - INFO - FastAPI application initialized
2026-03-08 14:23:00 - ai_resume_analyzer - INFO - CORS middleware configured
2026-03-08 14:23:00 - ai_resume_analyzer - INFO - Resume routes registered
2026-03-08 14:23:00 - ai_resume_analyzer - INFO - Starting AI Resume Analyzer API Server
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ **What this means**: Server is running successfully and ready to accept requests!

### Verification
Open browser: http://localhost:8000/docs
- You should see the FastAPI Swagger UI with API documentation

---

## 🎯 Test 2: Test Without File (Error Test)

### Step 2.1: Open New Terminal
```bash
# In a NEW terminal (don't close the server terminal)
curl -X POST "http://localhost:8000/api/upload-resume"
```

### Expected Output:
```json
{"detail":[{"type":"missing","loc":["body","file"],"msg":"Field required","input":{}}]}
```

✅ **What this means**: API correctly validates that file is required

---

## 📄 Test 3: Create a Test PDF

### Option A: Using Python (Recommended)
```bash
# In your new terminal, create a test PDF
python3 << 'EOF'
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Create PDF with sample resume text
pdf_text = """
JOHN DOE
Senior Software Engineer

EXPERIENCE
Software Engineer at Tech Company
- 5 years of Python development
- Led team of 3 developers
- Built scalable REST APIs

SKILLS
Languages: Python, JavaScript, Java
Databases: PostgreSQL, MongoDB
Tools: Docker, Kubernetes, AWS
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("test_resume.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

for line in pdf_text.split('\n'):
    if line.strip():
        story.append(Paragraph(line, styles['Normal']))
    story.append(Spacer(1, 0.2))

doc.build(story)
print("✅ Created test_resume.pdf")
EOF
```

### Option B: Manual - Download a Sample
Or download any resume PDF and name it `test_resume.pdf`

### Verify the file exists:
```bash
ls -lh test_resume.pdf
```

Should output something like:
```
-rw-r--r--  1 user  staff  4.2K Mar  8 14:23 test_resume.pdf
```

---

## 🚀 Test 4: Upload the Resume

### Step 4.1: Upload Command
```bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -H "accept: application/json" \
  -F "file=@test_resume.pdf"
```

### Expected Response (JSON):
```json
{
  "success": true,
  "filename": "test_resume.pdf",
  "page_count": 1,
  "extracted_text": "JOHN DOE\nSenior Software Engineer\n\nEXPERIENCE\nSoftware Engineer at Tech Company\n- 5 years of Python development\n- Led team of 3 developers\n- Built scalable REST APIs\n\nSKILLS\nLanguages: Python, JavaScript, Java\nDatabases: PostgreSQL, MongoDB\nTools: Docker, Kubernetes, AWS",
  "message": "Resume successfully processed"
}
```

✅ **What this means**: 
- File uploaded successfully
- Text extracted and cleaned
- Ready for LLM processing

---

## 📊 Test 5: Check the Logs (IMPORTANT!)

### In a NEW Terminal:
```bash
# Watch logs in real-time
tail -f logs/app.log
```

### You should see logs like:
```
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Resume upload request received - Filename: test_resume.pdf, Timestamp: 2026-03-08T14:25:15.234567
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - File validation passed for test_resume.pdf. Size: 0.04MB
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Resume file saved temporarily: /var/folders/...tmp.../test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Starting PDF analysis for test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - Starting text extraction from PDF: test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - PDF loaded successfully. Total pages: 1
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - DEBUG - Extracted text from page 1/1
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - Cleaning extracted text from test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - Text extraction and cleaning completed for test_resume.pdf. Characters: 247, Words: 28, Paragraphs: 5
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Resume processing completed successfully for test_resume.pdf. Pages: 1, Text length: 247 characters
```

✅ **What each log means**:
- **Upload request received** - API got the request
- **File validation passed** - File is PDF and under 10MB
- **File saved temporarily** - Safe to process
- **Starting text extraction** - PDF opening
- **PDF loaded successfully** - PDF is valid
- **Extracted text from page** - Text grabbed from each page
- **Cleaning extracted text** - TextCleaner running
- **Text extraction completed** - Statistics generated
- **Processing completed successfully** - All done!

---

## 🔍 Test 6: Check Error Log

### In another terminal:
```bash
cat logs/error.log
```

### Expected Output:
```
(empty - no errors occurred)
```

✅ **What this means**: No errors logged - everything worked!

---

## 🧪 Test 7: Text Cleaning Verification

Create test script: `test_text_cleaning.py`

```python
from services.text_cleaner import TextCleaner

print("\n" + "="*60)
print("TEXT CLEANING TEST")
print("="*60)

# Raw text with issues
raw = "John   Doe\n\n\nSoftware   Engineer\n\nExperienced in Python and JavaScript"

print("\n✏️ RAW TEXT:")
print(repr(raw))

# Clean it
cleaned = TextCleaner.clean_resume_text(raw)

print("\n✅ CLEANED TEXT:")
print(repr(cleaned))

# Get stats
stats = TextCleaner.get_text_statistics(cleaned)

print("\n📊 STATISTICS:")
print(f"  Characters: {stats['character_count']}")
print(f"  Words: {stats['word_count']}")
print(f"  Lines: {stats['line_count']}")
print(f"  Paragraphs: {stats['paragraph_count']}")

print("\n" + "="*60)
```

### Run it:
```bash
cd backend
python test_text_cleaning.py
```

### Expected Output:
```
============================================================
TEXT CLEANING TEST
============================================================

✏️ RAW TEXT:
'John   Doe\n\n\nSoftware   Engineer\n\nExperienced in Python and JavaScript'

✅ CLEANED TEXT:
'John Doe\nSoftware Engineer\nExperienced in Python and JavaScript'

📊 STATISTICS:
  Characters: 68
  Words: 11
  Lines: 3
  Paragraphs: 3

============================================================
```

✅ **What this shows**:
- Multiple spaces become single spaces (John   Doe → John Doe)
- Multiple line breaks become single line break (\n\n\n → \n)
- Statistics are calculated correctly

---

## 🔴 Test 8: Error Cases

### Test 8.1: Invalid File Type

```bash
# Create a text file
echo "This is not a PDF" > test.txt

# Try to upload
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@test.txt"
```

### Expected Response:
```json
{
  "detail": "Invalid file type. Please upload a PDF file."
}
```

### Expected Logs:
```
2026-03-08 14:26:00 - ai_resume_analyzer - INFO - Resume upload request received - Filename: test.txt
2026-03-08 14:26:00 - ai_resume_analyzer - WARNING - Invalid file type uploaded: test.txt. Expected PDF.
```

✅ **What this means**: Validation caught the invalid file type!

---

### Test 8.2: File Too Large

```bash
# Create a file larger than 10MB
dd if=/dev/zero bs=1M count=11 of=large.pdf

# Try to upload
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@large.pdf"
```

### Expected Response:
```json
{
  "detail": "File too large. Maximum size is 10MB, got 11.00MB"
}
```

### Expected Logs:
```
2026-03-08 14:27:00 - ai_resume_analyzer - INFO - Resume upload request received - Filename: large.pdf
2026-03-08 14:27:00 - ai_resume_analyzer - WARNING - File size exceeded for large.pdf: 11.00MB (max 10MB)
```

✅ **What this means**: File size validation works!

---

## 📱 Test 9: Using Postman (Alternative to curl)

### Step 1: Open Postman
1. Download from postman.com (if you don't have it)

### Step 2: Create Request
- Method: POST
- URL: `http://localhost:8000/api/upload-resume`

### Step 3: Add File
- Go to Body tab
- Select `form-data`
- Add key: `file`
- Value: Select `test_resume.pdf` file
- Click Send

### Expected Response:
Same JSON as Test 4 ✅

---

## 🐍 Test 10: Using Python Script

Create: `test_api.py`

```python
import requests
import json
from pathlib import Path

print("\n" + "="*60)
print("API TESTING WITH PYTHON")
print("="*60)

BASE_URL = "http://localhost:8000"

# Test 1: Health check
print("\n1️⃣ Testing health endpoint...")
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Root endpoint
print("\n2️⃣ Testing root endpoint...")
response = requests.get(f"{BASE_URL}/")
data = response.json()
print(f"Status: {response.status_code}")
print(f"Message: {data['message']}")
print(f"Version: {data['version']}")

# Test 3: Upload resume
print("\n3️⃣ Testing resume upload...")
resume_path = Path("test_resume.pdf")

if resume_path.exists():
    with open(resume_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/api/upload-resume", files=files)
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data['success']}")
    print(f"Filename: {data['filename']}")
    print(f"Pages: {data['page_count']}")
    print(f"Text length: {len(data['extracted_text'])} characters")
    print(f"Message: {data['message']}")
    print(f"\nExtracted text preview:")
    print(data['extracted_text'][:200] + "...")
else:
    print(f"File not found: {resume_path}")

print("\n" + "="*60)
print("✅ All tests completed!")
print("="*60)
```

### Run it:
```bash
python test_api.py
```

### Expected Output:
```
============================================================
API TESTING WITH PYTHON
============================================================

1️⃣ Testing health endpoint...
Status: 200
Response: {'status': 'healthy'}

2️⃣ Testing root endpoint...
Status: 200
Message: Welcome to AI Resume Analyzer API
Version: 0.1.0

3️⃣ Testing resume upload...
Status: 200
Success: True
Filename: test_resume.pdf
Pages: 1
Text length: 247 characters
Message: Resume successfully processed

Extracted text preview:
JOHN DOE
Senior Software Engineer

EXPERIENCE
...

============================================================
✅ All tests completed!
============================================================
```

---

## 📈 Test 11: Performance Test

Create: `test_performance.py`

```python
import requests
import time
from pathlib import Path

print("\n" + "="*60)
print("PERFORMANCE TEST")
print("="*60)

BASE_URL = "http://localhost:8000"
resume_path = Path("test_resume.pdf")

if not resume_path.exists():
    print("❌ test_resume.pdf not found!")
    exit(1)

# Test multiple uploads
print("\nUploading resume 3 times to measure performance...\n")

times = []
for i in range(1, 4):
    with open(resume_path, 'rb') as f:
        files = {'file': f}
        
        start = time.time()
        response = requests.post(f"{BASE_URL}/api/upload-resume", files=files)
        elapsed = time.time() - start
        
        times.append(elapsed)
        
        data = response.json()
        print(f"Request {i}: {elapsed:.3f}s - {data['page_count']} pages, {len(data['extracted_text'])} chars")

avg_time = sum(times) / len(times)
print(f"\n📊 Average response time: {avg_time:.3f}s")
print(f"⚡ Performance: {'✅ GOOD' if avg_time < 1.0 else '⚠️ SLOW'}")

print("\n" + "="*60)
```

### Run it:
```bash
python test_performance.py
```

### Expected Output:
```
============================================================
PERFORMANCE TEST
============================================================

Uploading resume 3 times to measure performance...

Request 1: 0.245s - 1 pages, 247 chars
Request 2: 0.238s - 1 pages, 247 chars
Request 3: 0.241s - 1 pages, 247 chars

📊 Average response time: 0.241s
⚡ Performance: ✅ GOOD

============================================================
```

✅ **What this means**: Response time is under 1 second - excellent!

---

## 📊 Test 12: Analyze Logs

### View all logs:
```bash
cat logs/app.log
```

### Count requests:
```bash
grep "upload request received" logs/app.log | wc -l
```

### Find all errors:
```bash
grep "ERROR" logs/app.log
```

### Search for specific file:
```bash
grep "test_resume.pdf" logs/app.log
```

### Watch logs in real-time while testing:
```bash
# Terminal 1: Start watching logs
tail -f logs/app.log

# Terminal 2: Make a request
curl -X POST "http://localhost:8000/api/upload-resume" -F "file=@test_resume.pdf"

# You'll see logs appear in Terminal 1 in real-time!
```

---

## ✅ Complete Testing Checklist

Use this to verify everything works:

### Server Tests
- [ ] Server starts without errors
- [ ] Console shows startup logs
- [ ] http://localhost:8000/docs shows API docs
- [ ] Health endpoint returns healthy

### API Tests
- [ ] GET / returns welcome message
- [ ] GET /health returns status
- [ ] POST /api/upload-resume with valid PDF returns success
- [ ] Response contains filename, page_count, extracted_text
- [ ] Text is cleaned (normalized)

### Error Handling Tests
- [ ] Uploading non-PDF returns 400
- [ ] Uploading >10MB returns 413
- [ ] Missing file parameter returns error

### Logging Tests
- [ ] Console shows INFO logs during upload
- [ ] logs/app.log file is created
- [ ] logs/error.log file is created (empty if no errors)
- [ ] Upload logs include filename and timestamps
- [ ] Processing logs show page count and statistics

### Performance Tests
- [ ] Response time < 1 second for typical PDF
- [ ] Text cleaning is fast
- [ ] Multiple requests work correctly

### Text Cleaning Tests
- [ ] Multiple spaces normalized to single space
- [ ] Multiple line breaks normalized
- [ ] Leading/trailing whitespace removed
- [ ] Statistics calculated correctly

---

## 🎯 Summary of Expected Behaviors

| Test | Expected | Status |
|------|----------|--------|
| Server starts | Shows startup logs | ✅ |
| Health check | Returns 200 + healthy | ✅ |
| Valid upload | Returns 200 + JSON | ✅ |
| Invalid file | Returns 400 | ✅ |
| Large file | Returns 413 | ✅ |
| Logs created | Files in logs/ directory | ✅ |
| Text cleaned | Whitespace normalized | ✅ |
| Performance | < 1 second | ✅ |

---

## 🚀 You're Ready to Test!

Follow the tests above and verify everything works. Start with:

```bash
# Terminal 1
cd backend && python main.py

# Terminal 2
cd backend && python test_api.py

# Terminal 3 (optional)
tail -f logs/app.log
```

All tests should pass! ✅

---

**Next**: Once testing is complete, you can:
1. Add LLM analysis to the extracted text
2. Store results in a database
3. Add user authentication
4. Deploy to production

Good luck with testing! 🎉
