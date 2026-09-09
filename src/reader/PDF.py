from .TextReader import TextReader
from .BaseFileReader import FileReaderError
 
try:
    import pdfplumber
except ImportError:  # pragma: no cover
    pdfplumber = None
 
 
class PDF(TextReader):
    SUPPORTED_EXTENSIONS = {".pdf"}
 
    def read(self) -> str:
        if pdfplumber is None:
            raise FileReaderError(
                "Thiếu thư viện 'pdfplumber'. Cài bằng: pip install pdfplumber"
            )
        parts = []
        try:
            with pdfplumber.open(str(self.file_path)) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        parts.append(text)
        except Exception as e:
            raise FileReaderError(f"Không thể đọc file pdf '{self.file_path}': {e}") from e
 
        return "\n".join(parts)
 