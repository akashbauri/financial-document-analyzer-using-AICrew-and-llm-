import re, os
from PyPDF2 import PdfReader
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import sessionmaker
from models import Base, DocumentRecord, AnalysisRecord, engine
import openai

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        raise ValueError("Unsupported file format")
    return text

def analyze_text(text):
    values = [float(x.replace(",", "")) for x in re.findall(r"\$?([0-9,.]+)", text)]
    return {
        "num_currency_values": len(values),
        "sum_currency_values": sum(values) if values else 0,
        "max_value": max(values) if values else None,
        "min_value": min(values) if values else None
    }

def summarize_text(text):
    return f"Summary: Found {len(text.split())} words."

def llm_summary(text):
    prompt = f"Provide a concise financial analysis summary for this text:\n{text[:1000]}"
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a financial analyst."},
                      {"role": "user", "content": prompt}]
        )
        return resp.choices[0].message["content"]
    except Exception as e:
        return str(e)

def generate_report(file_path, metrics, summary, llm_sum):
    report_file = "report.pdf"
    c = canvas.Canvas(report_file, pagesize=letter)
    c.drawString(100, 750, f"Report for: {os.path.basename(file_path)}")
    c.drawString(100, 730, f"Metrics: {metrics}")
    c.drawString(100, 710, f"Summary: {summary}")
    if llm_sum:
        c.drawString(100, 690, f"LLM Summary: {llm_sum}")
    c.save()
    return report_file

def run_analysis(file_path, use_llm=False):
    session = Session()
    text = extract_text(file_path)
    metrics = analyze_text(text)
    summary = summarize_text(text)
    llm_sum = llm_summary(text) if use_llm else None
    report_file = generate_report(file_path, metrics, summary, llm_sum)

    # Save to DB
    doc = DocumentRecord(filename=file_path, content=text)
    session.add(doc)
    session.commit()

    analysis = AnalysisRecord(document_id=doc.id, metrics=str(metrics), summary=summary, llm_summary=llm_sum)
    session.add(analysis)
    session.commit()

    return report_file, metrics, summary, llm_sum
