from .TxtFileReader import TxtFileReader
from .CsvFileReader import CsvFileReader
from .ExcelFileReader import ExcelFileReader
from .WordFileReader import WordFileReader
from .BaseFileReader import BaseFileReader
import os
class FileReaderFactory:
    @staticmethod
    def get_reader(file_path: str) -> BaseFileReader:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.txt':
            return TxtFileReader()
        elif ext in ['.csv']:
            return CsvFileReader()
        elif ext in ['.xlsx', '.xls']:
            return ExcelFileReader()
        elif ext in ['.docx']:
            return WordFileReader()
        else:
            raise ValueError(f"dinh dang file text '{ext}' chua duoc ho tro!")