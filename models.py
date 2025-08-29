from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///analysis.db")

class DocumentRecord(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    content = Column(Text)

class AnalysisRecord(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, nullable=False)
    metrics = Column(Text)
    summary = Column(Text)
    llm_summary = Column(Text)
