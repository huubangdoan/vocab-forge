from .BaseFileReader import BaseFileReader
from docx import Document
class WordFileReader(BaseFileReader):
    def read_words(self, file_path: str) -> list[str]:
        """Đọc file Word (.docx), trích xuất từ vựng từ các đoạn văn bản."""
        doc = Document(file_path)
        words = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                # Giả định mỗi dòng hoặc mỗi đoạn là một từ vựng
                words.app