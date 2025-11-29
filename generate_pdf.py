import uuid
import qrcode
import os
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data.db")
QR_DIR = os.path.join(BASE_DIR, "static", "qr")
PDF_DIR = os.path.join(BASE_DIR, "static", "pdf")
os.makedirs(QR_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def generate_document(title, applicant, status="Approved"):
    # create unique ID
    doc_id = str(uuid.uuid4())

    # insert to DB
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    issue_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    pdf_filename = f"{doc_id}.pdf"
    pdf_path = os.path.join("static", "pdf", pdf_filename)

    cur.execute("""INSERT INTO documents (doc_id, title, applicant, issue_date, status, pdf_path)
                   VALUES (?, ?, ?, ?, ?, ?)""", (doc_id, title, applicant, issue_date, status, pdf_path))
    conn.commit()
    conn.close()

    # generate qr
    qr_data = f"http://localhost:5000/verify?id={doc_id}"
    qr_path = os.path.join(QR_DIR, f"{doc_id}.png")
    img = qrcode.make(qr_data)
    img.save(qr_path)

    # create pdf
    abs_pdf_path = os.path.join(BASE_DIR, pdf_path)
    c = canvas.Canvas(abs_pdf_path, pagesize=A4)
    width, height = A4

    # Title and details
    c.setFont('Helvetica-Bold', 16)
    c.drawString(50, height - 80, title)
    c.setFont('Helvetica', 12)
    c.drawString(50, height - 110, f"Document ID: {doc_id}")
    c.drawString(50, height - 130, f"Applicant: {applicant}")
    c.drawString(50, height - 150, f"Issue Date: {issue_date}")
    c.drawString(50, height - 170, f"Status: {status}")

    # draw QR
    c.drawImage(qr_path, width - 170, height - 220, width=120, height=120)

    # footer
    c.setFont('Helvetica-Oblique', 8)
    c.drawString(50, 40, 'Scan the QR code to verify this document at http://localhost:5000/verify')

    c.showPage()
    c.save()

    print('Generated:', abs_pdf_path)
    return doc_id, pdf_path

if __name__ == '__main__':
    # quick test
    generate_document('Land Registration Certificate', 'Test Applicant', 'Approved')
