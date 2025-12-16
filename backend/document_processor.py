# backend/document_processor.py

import os
from typing import List
import PyPDF2
import docx


class DocumentProcessor:
    def __init__(self):
        pass

    def read_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def read_pdf(self, file_path: str) -> str:
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def read_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def process_file(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".txt":
            return self.read_txt(file_path)
        elif ext == ".pdf":
            return self.read_pdf(file_path)
        elif ext == ".docx":
            return self.read_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def process_multiple(self, file_paths: List[str]) -> str:
        combined_text = ""
        for path in file_paths:
            combined_text += self.process_file(path) + "\n"
        return combined_text
