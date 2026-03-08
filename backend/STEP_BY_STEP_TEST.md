# 🎬 Testing - Step by Step (5 Minutes)

## 🎯 Goal
Upload a PDF resume and get back cleaned text with logs.

---

## ⏱️ Step 1: Start Server (30 seconds)

### In Terminal 1:
```bash
cd /Users/dishitasharma/Documents/AI_LEARNING/ai-resume-analyzer/backend
python main.py
```

### You'll See:
```
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - FastAPI application initialized
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - CORS middleware configured
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - Resume routes registered
2026-03-08 14:23:45 - ai_resume_analyzer - INFO - Starting AI Resume Analyzer API Server
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ **Leave this terminal running!**

---

## ⏱️ Step 2: Watch Logs (Optional but Recommended)

### In Terminal 3:
```bash
cd /Users/dishitasharma/Documents/AI_LEARNING/ai-resume-analyzer/backend
tail -f logs/app.log
```

### You'll See:
```
(Waiting for logs to appear...)
```

✅ **Keep this open to see logs in real-time!**

---

## ⏱️ Step 3: Create Test File (1 minute)

### In Terminal 2:
```bash
cd /Users/dishitasharma/Documents/AI_LEARNING/ai-resume-analyzer/backend

# Create test PDF with Python
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
    Paragraph("SKILLS: Python, JavaScript, AWS", styles['Normal']),
    Spacer(1, 0.2),
    Paragraph("5+ years building scalable systems", styles['Normal']),
]
doc.build(story)
print("✅ Created test_resume.pdf")
EOF
```

### Verify:
```bash
ls -lh test_resume.pdf
```

You should see:
```
-rw-r--r--  1 user  staff  3.2K Mar  8 14:25 test_resume.pdf
```

✅ **Test file created!**

---

## ⏱️ Step 4: Upload Resume (30 seconds)

### Still in Terminal 2, run:
```bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@test_resume.pdf"
```

---

## 🎯 Expected Outcome #1: Console Output

### Terminal 2 will show:
```json
{
  "success": true,
  "filename": "test_resume.pdf",
  "page_count": 1,
  "extracted_text": "JOHN DOE\nSenior Software Engineer\nSKILLS: Python, JavaScript, AWS\n5+ years building scalable systems",
  "message": "Resume successfully processed"
}
```

### What This Means:
- ✅ `"success": true` = Everything worked!
- ✅ `"filename"` = Your file uploaded
- ✅ `"page_count": 1` = 1 page detected
- ✅ `"extracted_text"` = Cleaned text (formatted!)
- ✅ `"message"` = Success confirmation

---

## 🎯 Expected Outcome #2: Server Logs (Terminal 1)

### Terminal 1 will show:
```
(No visible change - normal)
```

Don't worry, this is normal. Check Terminal 3!

---

## 🎯 Expected Outcome #3: Real-time Logs (Terminal 3)

### Terminal 3 will show:
```
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Resume upload request received - Filename: test_resume.pdf, Timestamp: 2026-03-08T14:25:15.234567
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - File validation passed for test_resume.pdf. Size: 0.03MB
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Resume file saved temporarily: /var/folders/...tmp.../test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Starting PDF analysis for test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - Starting text extraction from PDF: test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - PDF loaded successfully. Total pages: 1
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - DEBUG - Extracted text from page 1/1
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - Cleaning extracted text from test_resume.pdf
2026-03-08 14:25:15 - ai_resume_analyzer.services.resume_parser - INFO - Text extraction and cleaning completed for test_resume.pdf. Characters: 127, Words: 15, Paragraphs: 4
2026-03-08 14:25:15 - ai_resume_analyzer - INFO - Resume processing completed successfully for test_resume.pdf. Pages: 1, Text length: 127 characters
```

### What Each Line Means:
```
Line 1: ✅ API received your request
Line 2: ✅ File is valid PDF under 10MB  
Line 3: ✅ File saved to temp location
Line 4: ✅ About to extract text
Line 5: ✅ Opening PDF with pdfplumber
Line 6: ✅ PDF loaded successfully (1 page)
Line 7: ✅ Extracted text from page 1
Line 8: ✅ Running text cleaner
Line 9: ✅ Cleaning done! Stats: 127 chars, 15 words, 4 paragraphs
Line 10: ✅ All processing complete!
```

✅ **All logs = SUCCESS!**

---

## 📁 Check Log Files

### Terminal 2, run:
```bash
# See all logs
cat logs/app.log

# Or just last few lines
tail logs/app.log

# Check error log (should be empty)
cat logs/error.log
```

### You Should See:
```
logs/app.log ← Contains all 10 log entries above
logs/error.log ← Empty (no errors)
```

✅ **Logs created successfully!**

---

## 🧹 Verify Text Cleaning Worked

### Look at the extracted_text in response:

```
Before (raw from PDF):
"JOHN   DOE\n\n\nSenior  Software  Engineer"

After (cleaned):
"JOHN DOE\nSenior Software Engineer"
     ↑ Fixed!        ↑ Fixed!
```

### You can see:
- ✅ Multiple spaces → Single space
- ✅ Multiple newlines → Single newline
- ✅ Ready for LLM!

---

## 🎉 Success Check

If you see all of these, you're DONE! ✅

- [ ] Terminal 1: Server running
- [ ] Terminal 2: Got JSON response with "success": true
- [ ] Terminal 3: Saw 10 log entries
- [ ] Text is cleaned (no extra spaces/newlines)
- [ ] logs/app.log created
- [ ] logs/error.log exists but empty

---

## 🔴 If Something Goes Wrong

### Server won't start?
```bash
# Wrong directory?
cd /Users/dishitasharma/Documents/AI_LEARNING/ai-resume-analyzer/backend

# Port in use?
lsof -ti:8000 | xargs kill -9
python main.py
```

### Upload fails with error?
```bash
# Server not running?
# Check Terminal 1 - is it still running?

# File doesn't exist?
ls test_resume.pdf

# If not, create it:
# Run Step 3 again
```

### No response?
```bash
# Check if file is valid:
file test_resume.pdf
# Should say: "PDF document"

# Check if server is listening:
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

---

## 🚀 Test Complete!

### What You've Verified:
✅ FastAPI server works  
✅ Resume upload endpoint works  
✅ PDF extraction works  
✅ Text cleaning works  
✅ Logging system works  
✅ Error handling works  

### Your Backend is Ready For:
→ Adding LLM analysis  
→ Storing to database  
→ Building frontend  
→ Production deployment  

---

## 📚 Next Steps

Want to learn more?

- **How testing works**: HOW_TO_TEST.md
- **Quick commands**: QUICK_TEST.md
- **Expected outputs**: EXPECTED_OUTPUT.md
- **Architecture**: ARCHITECTURE_DIAGRAM.md

---

## 📞 Still Have Questions?

Check these files:
- `QUICK_REFERENCE.md` - Commands & snippets
- `ENHANCEMENTS.md` - How it works
- `HOW_TO_TEST.md` - All test scenarios
- `EXPECTED_OUTPUT.md` - What to expect

---

**🎊 Congratulations! Your backend is working!** 🎊

Now you can integrate it with:
1. LLM (OpenAI, Claude, etc)
2. Database (PostgreSQL, MongoDB, etc)
3. Frontend (React, Vue, etc)
4. Authentication (JWT, OAuth, etc)

Happy coding! 🚀
