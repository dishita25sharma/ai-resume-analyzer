# ⚡ Quick Reference Card

## 🚀 Start Server
```bash
cd backend
python main.py
```

## 📤 Upload Resume
```bash
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@resume.pdf"
```

## 📋 Response Format
```json
{
  "success": true,
  "filename": "resume.pdf",
  "page_count": 2,
  "extracted_text": "John Doe\nSoftware Engineer\n...",
  "message": "Resume successfully processed"
}
```

## 📊 View Logs
```bash
# Real-time (recommended)
tail -f logs/app.log

# Errors only
cat logs/error.log

# Last 50 lines
tail -50 logs/app.log

# Search for specific file
grep "resume.pdf" logs/app.log
```

## 🧹 Text Cleaning
```python
from services.text_cleaner import TextCleaner

# Clean text
cleaned = TextCleaner.clean_resume_text(raw_text)

# Get statistics
stats = TextCleaner.get_text_statistics(cleaned)
print(stats)
# {'character_count': 5000, 'word_count': 890, ...}

# Aggressive cleaning (single paragraph)
single_para = TextCleaner.clean_resume_text_aggressive(raw_text)
```

## 📝 Logging
```python
from utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Information")     # Console + app.log
logger.warning("Warning")      # Console + app.log
logger.error("Error")          # Console + app.log + error.log
logger.debug("Debug info")     # app.log only
```

## 🏗️ Architecture Layers
```
API Layer       → api/resume_routes.py
Business Logic  → services/resume_parser.py
Data Processing → services/text_cleaner.py
Infrastructure  → utils/logger.py
```

## ✅ API Endpoints
```
GET  /                    → API info
GET  /health              → Health check
POST /api/upload-resume   → Upload & process
```

## 📁 Key Files
```
services/text_cleaner.py  → TextCleaner class
services/resume_parser.py → ResumeParser class
utils/logger.py           → AppLogger class
api/resume_routes.py      → API endpoints
main.py                   → FastAPI app
```

## 🔧 Configuration
```python
# In utils/logger.py:
logger.setLevel(logging.INFO)  # Change log level
# Outputs: Console, logs/app.log, logs/error.log
```

## 📈 Performance Tips
```
- Text cleaning: ~100ms per resume
- PDF extraction: 0.5-2s per page
- Max file size: 10MB
- Supports: Most modern PDFs
```

## 🧪 Test Upload
```bash
# Create test PDF (any method)
# Then upload
curl -X POST "http://localhost:8000/api/upload-resume" \
  -F "file=@test.pdf"

# Watch logs
tail -f logs/app.log
```

## ❌ Error Handling
```
400 → Invalid input (wrong file type, too large)
404 → File not found
500 → Server error

All errors logged to logs/error.log
```

## 📚 Documentation Files
```
COMPLETE_IMPLEMENTATION.md  ← Full overview
ENHANCEMENT_SUMMARY.md      ← Quick summary
ENHANCEMENTS.md            ← Detailed guide
ARCHITECTURE_DIAGRAM.md     ← Visual flows
TESTING_GUIDE.md           ← Testing instructions
README.md                  ← Original setup
```

## 🎯 Next: LLM Integration
```python
# After cleaning, send to LLM:
from openai import OpenAI

cleaned_text = TextCleaner.clean_resume_text(extracted_text)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": f"Analyze: {cleaned_text}"}
    ]
)
```

## 📊 Module Dependencies
```
main.py
├── api/resume_routes.py
│   ├── utils/logger.py        ← Logging
│   └── services/resume_parser.py
│       ├── utils/logger.py
│       └── services/text_cleaner.py
└── utils/logger.py
```

## 🔍 Debugging Commands
```bash
# Find all INFO logs
grep "INFO" logs/app.log

# Count requests
grep "upload request" logs/app.log | wc -l

# Find slowest request
grep "completed successfully" logs/app.log | tail -1

# Monitor real-time
watch -n 1 'wc -l logs/app.log logs/error.log'
```

## 💡 Pro Tips
1. Always check logs first when debugging
2. Use aggressive cleaning for single-paragraph output
3. Monitor logs/error.log in production
4. TextCleaner works independently from resume_parser
5. Logger is reusable across all modules

## 🎓 Key Concepts
- **Text Cleaning**: Normalize whitespace & line breaks
- **Logging**: Record all operations for debugging/monitoring
- **Modular Design**: Each module has single responsibility
- **Error Handling**: Comprehensive exception logging
- **Production Ready**: Rotating logs, error handling, validation

---

**Everything you need to know on one page!**
