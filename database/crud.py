from .models import SessionLocal, PdfData


def add_pdf(filename: str, filepath: str, content_summary: str):
    db = SessionLocal()
    pdf = PdfData(filename=filename, filepath=filepath, content_summary=content_summary)
    db.add(pdf)
    db.commit()
    db.refresh(pdf)
    db.close()
    return pdf


def get_all_pdfs():
    db = SessionLocal()
    pdfs = db.query(PdfData).all()
    db.close()
    return pdfs


def get_pdf_by_id(pdf_id: int):
    db = SessionLocal()
    pdf = db.query(PdfData).filter(PdfData.id == pdf_id).first()
    db.close()
    return pdf
