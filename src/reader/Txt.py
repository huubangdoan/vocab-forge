from .TextReader import TextReader
from .BaseFileReader import FileReaderError
 
 
class Txt(TextReader):
    SUPPORTED_EXTENSIONS = {".txt"}
 
    def __init__(self, file_path: str, encoding: str = "utf-8"):
        self.encoding = encoding
        super().__init__(file_path)
 
    def read(self) -> str:
        try:
            with open(self.file_path, "r", encoding=self.encoding, errors="ignore") as f:
                return f.read()
        except Exception as e:
            raise FileReaderError(f"Không thể đọc file txt '{self.file_path}': {e}") from e
 