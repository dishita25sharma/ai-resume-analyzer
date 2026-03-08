# ⚡ Quick Test Commands

## 🚀 Start Everything

### Terminal 1: Run Server
```bash
cd /Users/dishitasharma/Documents/AI_LEARNING/ai-resume-analyzer/backend
python main.py
```

**Expected**: Logs show server started on http://0.0.0.0:8000

---

### Terminal 2: Watch Logs (Optional)
```bash
cd backend
tail -f logs/app.log
```

**Expected**: You'll see logs appear as you make requests

---

## 📝 Create Test File (One Time)

```bash
cd backend

# Create a simple test PDF with Python
python3 << 'EOF'
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("test_resume.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = [
    Paragraph("JOHN DOE", styles['Heading1']),
    Paragraph("Senior Software Engineer", styles['Normal']),
    Spacer(1, 0.2),
    Paragraph("EXPERIENCE", styles['Heading2']),
    Paragraph("- 5 years Python development", styles['Normal']),
    Paragraph("- Built scalable REST APIs", styles['Normal']),
]
doc.build(story)
print("✅ Created test_resume.pdf")
EOF

# Verify it exists
ls -lh test_resume.pdf
```

---

## 🧪 Quick Test Commands

### Test 1: Check if server is running
```bash
curl http://localhost:8000/
```
**Expected Output**: 
```json
{
  "message": "Welcome to AI Resume Analyzer API",
  "version": "0.1.0",
  "endpoints": {...}
}
```

---

### Test 2: Health check
```bash
curl http://localhost:8000/health
```
**Expected Output**:
```json
{"status": "healthy"}
```

---

### Test 3: Upload resume (THE MAIN TEST!)
```bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@test_resume.pdf"
```

**Expected Output**:
```json
{
  "success": true,
  "filename": "test_resume.pdf",
  "page_count": 1,
  "extracted_text": "JOHN DOE\nSenior Software Engineer\n...",
  "message": "Resume successfully processed"
}
```

✅ **KEY POINTS TO CHECK**:
- `success` is `true`
- `filename` is your file name
- `page_count` shows number of pages
- `extracted_text` contains cleaned text (no extra spaces/line breaks)
- `message` says "successfully processed"

---

### Test 4: Error test - Invalid file type
```bash
echo "Not a PDF" > test.txt
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@test.txt"
```

**Expected Output**:
```json
{
  "detail": "Invalid file type. Please upload a PDF file."
}
```

---

### Test 5: Error test - File too large
```bash
dd if=/dev/zero bs=1M count=11 of=large.pdf
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@large.pdf"
```

**Expected Output**:
```json
{
  "detail": "File too large. Maximum size is 10MB, got 11.00MB"
}
```

---

## 📊 Test with Python Script

### Option A: Simple Test
```python
import requests

# Upload file
with open('test_resume.pdf', 'rb') as f:
    resp = requests.post(
        'http://localhost:8000/api/upload-resume',
        files={'file': f}
    )

# Print result
print("✅ Status:", resp.status_code)
print("📄 Filename:", resp.json()['filename'])
print("📄 Pages:", resp.json()['page_count'])
print("📄 Text length:", len(resp.json()['extracted_text']))
print("\n📝 Extracted text:")
print(resp.json()['extracted_text'][:200])
```

Save as `quick_test.py` and run:
```bash
python quick_test.py
```

---

### Option B: Full Test Suite
```bash
# Copy and paste all at once:

python3 << 'EOF'
import requests
import json

BASE = "http://localhost:8000"

print("\n" + "="*60)
print("TESTING AI RESUME ANALYZER")
print("="*60)

# Test 1
print("\n✅ Test 1: Health Check")
r = requests.get(f"{BASE}/health")
print(f"   Status: {r.status_code}")
print(f"   Response: {r.json()}")

# Test 2
print("\n✅ Test 2: API Root")
r = requests.get(f"{BASE}/")
print(f"   Status: {r.status_code}")
print(f"   Message: {r.json()['message']}")

# Test 3
print("\n✅ Test 3: Upload Resume")
with open('test_resume.pdf', 'rb') as f:
    r = requests.post(f"{BASE}/api/upload-resume", files={'file': f})

if r.status_code == 200:
    data = r.json()
    print(f"   Status: {r.status_code} ✅ SUCCESS")
    print(f"   Filename: {data['filename']}")
    print(f"   Pages: {data['page_count']}")
    print(f"   Text length: {len(data['extracted_text'])} chars")
    print(f"   Text preview: {data['extracted_text'][:100]}...")
else:
    print(f"   Status: {r.status_code} ❌ FAILED")
    print(f"   Error: {r.json()}")

print("\n" + "="*60)
print("✅ All tests completed!")
print("="*60 + "\n")
EOF
```

---

## 📊 Check Logs

### View all logs
```bash
cat logs/app.log
```

### View last 20 lines
```bash
tail -20 logs/app.log
```

### Count total uploads
```bash
grep -c "upload request received" logs/app.log
```

### Find errors
```bash
grep "ERROR" logs/app.log
```

### Real-time log watching
```bash
tail -f logs/app.log
```
(Press Ctrl+C to stop)

---

## 🧹 Text Cleaning Test

```bash
python3 << 'EOF'
from services.text_cleaner import TextCleaner

# Raw text with issues
raw = "John   Doe\n\n\nSoftware Engineer"

print("Raw:", repr(raw))
print("Cleaned:", repr(TextCleaner.clean_resume_text(raw)))

# Expected:
# Raw: 'John   Doe\n\n\nSoftware Engineer'
# Cleaned: 'John Doe\nSoftware Engineer'
EOF
```

---

## 🎯 What Should Happen

### Terminal 1 (Server Running):
```
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - FastAPI application initialized
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - CORS middleware configured
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - Resume routes registered
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - Starting AI Resume Analyzer API Server
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2 (When you upload):
```
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Resume upload request received - Filename: test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - File validation passed for test_resume.pdf. Size: 0.04MB
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Resume file saved temporarily: /tmp/...
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Starting PDF analysis for test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - Starting text extraction from PDF
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - PDF loaded successfully. Total pages: 1
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - Text extraction and cleaning completed. Characters: 150, Words: 25, Paragraphs: 3
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Resume processing completed successfully for test_resume.pdf
```

### Terminal 3 (Your Request):
```json
{
  "success": true,
  "filename": "test_resume.pdf",
  "page_count": 1,
  "extracted_text": "JOHN DOE\nSenior Software Engineer\nEXPERIENCE\n- 5 years Python development\n- Built scalable REST APIs",
  "message": "Resume successfully processed"
}
```

---

## ✅ Quick Verification Checklist

- [ ] Server starts without errors
- [ ] `curl http://localhost:8000/` returns JSON
- [ ] `curl http://localhost:8000/health` returns `{"status": "healthy"}`
- [ ] Upload returns `"success": true`
- [ ] Response has `filename`, `page_count`, `extracted_text`
- [ ] Text is cleaned (no extra spaces)
- [ ] `logs/app.log` file exists and has content
- [ ] `logs/error.log` file exists (should be empty)
- [ ] Invalid file returns 400 error
- [ ] Large file returns 413 error

---

## 🚨 Troubleshooting

### Error: "Connection refused"
**Problem**: Server not running
**Solution**: 
```bash
cd backend
python main.py
```

### Error: "Module not found: utils.logger"
**Problem**: Not in correct directory
**Solution**: 
```bash
cd /Users/dishitasharma/Documents/AI_LEARNING/ai-resume-analyzer/backend
python main.py
```

### Error: "No test_resume.pdf"
**Problem**: Test file doesn't exist
**Solution**: Create it first (see above)

### Error: "Address already in use"
**Problem**: Port 8000 is busy
**Solution**: 
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
# Then start server again
python main.py
```

---

## 🎉 You're Ready!

**Quick 2-minute test:**
```bash
# Terminal 1
cd backend && python main.py

# Wait 3 seconds, then Terminal 2
cd backend && curl -X POST http://localhost:8000/api/upload-resume -F "file=@test_resume.pdf"

# Should see JSON response with success=true ✅
```

Done! 🎊
