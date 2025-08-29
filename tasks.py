from celery import Celery
from financial_analyzer import run_analysis

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def analyze_document_task(file_path, use_llm=False):
    return run_analysis(file_path, use_llm)
