# Financial Document Analyzer (Fixed)

## Overview
This project analyzes financial documents (PDF, DOCX) to extract key values and summaries.
It was originally buggy, but has been debugged and improved.

### Fixes
- Fixed broken imports and missing functions
- Fixed file handling (PyPDF2 issues)
- Improved prompts for LLM
- Added error handling for robustness

### Bonus Features
- Added Celery + Redis queue worker for concurrent analysis
- Added SQLite + SQLAlchemy database for storing results

## Usage
```bash
pip install -r requirements.txt
python financial_analyzer.py
```

To run Celery worker:
```bash
celery -A tasks worker --loglevel=info
```

## API
- `run_analysis(file_path, use_llm=False)`: Run analysis on a document
- Returns: (report.pdf, metrics_dict, summary, llm_summary)

## Outputs
- `report.pdf` → Analysis report
- `analysis.db` → Database storing documents and analyses
