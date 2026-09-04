from .BaseFileReader import BaseFileReader
class TxtFileReader(BaseFileReader):
    def read_words(self, file_path: str) -> list[str]:
        words = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                clean_word = line.strip()
                if clean_word:
                    words.append(clean_word)
        return words