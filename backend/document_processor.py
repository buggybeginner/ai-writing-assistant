# backend/document_processor.py

import PyPDF2
import docx
import io

class DocumentProcessor:

    def read_txt(self, uploaded_file):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    def read_pdf(self, uploaded_file):
        text = ""
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text

    def read_docx(self, uploaded_file):
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        return "\n".join(p.text for p in doc.paragraphs)
