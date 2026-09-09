from abc import ABC, abstractmethod
from pathlib import Path
class FileReaderError(Exception):
    pass
class BaseFileReader(ABC):
    SUPPORTED_EXTENSIONS: set[str] = set()
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._validate_file()

    @abstractmethod
    def read(self):
        """Đọc nội dung thô của file. Kiểu trả về tùy vào loại reader."""
        raise NotImplementedError
 
    @abstractmethod
    def extract_text(self) -> str:
        """Trả về toàn bộ nội dung dạng text thuần (str)."""
        raise NotImplementedError
    def _validate_file(self) -> None:
        if not self.file_path.exists():
            raise FileReaderError(f"File không tồn tại: {self.file_path}")
        if not self.file_path.is_file():
            raise FileReaderError(f"Đường dẫn không phải file: {self.file_path}")
 
        ext = self.file_path.suffix.lower()
        if self.SUPPORTED_EXTENSIONS and ext not in self.SUPPORTED_EXTENSIONS:
            raise FileReaderError(
                f"Phần mở rộng '{ext}' không được hỗ trợ bởi "
                f"{self.__class__.__name__}. Hỗ trợ: {self.SUPPORTED_EXTENSIONS}"
            )
    @property
    def file_extension(self) -> str:
        return self.file_path.suffix.lower()
 
    @property
    def file_name(self) -> str:
        return self.file_path.name
 
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(file_path='{self.file_path}')"
    