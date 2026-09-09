"""
vocabulary_finder.py
---------------------
Trích xuất các từ vựng tiếng Anh từ nội dung file (đọc qua BaseFileReader)
và tìm ra những từ CHƯA tồn tại trong database SQLite.
"""

import re
from reader.BaseFileReader import BaseFileReader
from .VocabularyDB import VocabularyDB

# Từ dừng (stopword) tiếng Anh phổ biến - loại bỏ để chỉ giữ lại từ vựng "có nghĩa".
# Có thể mở rộng danh sách này tùy nhu cầu.
DEFAULT_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "so", "of", "to",
    "in", "on", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below",
    "from", "up", "down", "out", "off", "over", "under", "again", "further",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "its", "our", "their", "this", "that",
    "these", "those", "as", "not", "no", "nor", "too", "very", "can",
    "will", "just", "should", "now", "s", "t", "d", "ll", "m", "re", "ve",
}


class VocabularyFinder:
    def __init__(self, db: VocabularyDB, stopwords: set[str] | None = None,
                 min_length: int = 2):
        self.db = db
        self.stopwords = stopwords if stopwords is not None else DEFAULT_STOPWORDS
        self.min_length = min_length
        # Chỉ chấp nhận token thuần chữ cái A-Z (không số, không ký tự đặc biệt)
        self._word_pattern = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

    # ------------------------------------------------------------------ #
    def extract_words_from_text(self, text: str) -> set[str]:
        """Tokenize + chuẩn hóa + lọc stopword từ 1 đoạn text bất kỳ."""
        if not text:
            return set()

        tokens = self._word_pattern.findall(text)
        words = set()
        for tok in tokens:
            w = tok.lower().strip("'")
            if len(w) < self.min_length:
                continue
            if w in self.stopwords:
                continue
            words.add(w)
        return words

    # ------------------------------------------------------------------ #
    def find_new_words(self, reader: BaseFileReader) -> set[str]:
        """
        Nhận 1 file reader bất kỳ (Doc, Txt, PDF, Excel...) kế thừa BaseFileReader,
        trích text -> tách từ -> trả về tập từ vựng CHƯA có trong database.
        """
        text = reader.extract_text()
        candidate_words = self.extract_words_from_text(text)
        existing_words = self.db.get_all_words()
        return candidate_words - existing_words

    def find_new_words_multi(self, readers: list[BaseFileReader]) -> dict:
        """
        Xử lý nhiều file cùng lúc.
        Trả về:
            {
                "per_file": {file_name: set(new_words), ...},
                "combined": set(new_words toàn bộ, đã gộp & loại trùng)
            }
        """
        existing_words = self.db.get_all_words()
        per_file = {}
        combined = set()

        for reader in readers:
            text = reader.extract_text()
            candidate_words = self.extract_words_from_text(text)
            new_words = candidate_words - existing_words
            per_file[reader.file_name] = new_words
            combined |= new_words

        return {"per_file": per_file, "combined": combined}

    # ------------------------------------------------------------------ #
    def save_new_words_to_db(self, new_words: set[str]) -> int:
        """
        Lưu các từ mới phát hiện vào DB dưới dạng placeholder
        (definitions/band/description/example để trống, xử lý/tra nghĩa sau).
        Trả về số từ thực sự được thêm mới.
        """
        return self.db.add_words_bulk(list(new_words))