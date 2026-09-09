from .TextReader import TextReader
from .BaseFileReader import FileReaderError
 
try:
    import docx  # python-docx
except ImportError as e:  # pragma: no cover
    docx = None
 
 
class Doc(TextReader):
    SUPPORTED_EXTENSIONS = {".docx", ".doc"}
 
    def read(self) -> str:
        if self.file_extension == ".doc":
            raise FileReaderError(
                "Định dạng .doc (binary cũ) chưa được hỗ trợ trực tiếp. "
                "Vui lòng convert sang .docx trước."
            )
        if docx is None:
            raise FileReaderError(
                "Thiếu thư viện 'python-docx'. Cài bằng: pip install python-docx"
            )
        try:
            document = docx.Document(str(self.file_path))
        except Exception as e:
            raise FileReaderError(f"Không thể đọc file docx '{self.file_path}': {e}") from e
        parts = [para.text for para in document.paragraphs if para.text.strip()]
 
        return "\n".join(parts)
 