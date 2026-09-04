class Vocabulary:
    def __init__(self, word: str, definition: str, word_type: str = "", band: str = "", example: str = ""):
        self.word = word.lower().strip()
        self.definition = definition.strip()
        self.word_type = word_type.strip()
        self.band = band.upper().strip()  # Lưu cấp độ: B1, B2, C1, C2...
        self.example = example.strip()

    def to_dict(self) -> dict:
        """Chuyển đổi object sang dictionary để lưu trữ JSON hoặc SQLite."""
        return {
            "word": self.word,
            "definition": self.definition,
            "word_type": self.word_type,
            "band": self.band,
            "example": self.example
        }

    def __str__(self) -> str:
        band_str = f"[{self.band}]" if self.band else "[Unranked]"
        return f"{band_str} {self.word} ({self.word_type}): {self.definition} - VD: {self.example}"