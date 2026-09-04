import csv
from .BaseFileReader import BaseFileReader
class CsvFileReader(BaseFileReader):
    def read_words(self, file_path: str) -> list[str]:
        words = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    words.append(row[0].strip()) # Lấy cột đầu tiên làm từ vựng
        return words