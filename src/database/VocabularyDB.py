import sqlite3
from contextlib import contextmanager
from pathlib import Path


class VocabularyDB:
    def __init__(self, db_path: str = "vocabulary.db"):
        self.db_path = Path(db_path)
        self._init_schema()

    # ------------------------------------------------------------------ #
    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS vocabulary (
                    word        TEXT PRIMARY KEY,
                    definitions TEXT,
                    band        TEXT,
                    description TEXT,
                    example     TEXT
                )
                """
            )

    # ------------------------------------------------------------------ #
    # Query
    # ------------------------------------------------------------------ #
    def get_all_words(self) -> set[str]:
        """Trả về tập hợp toàn bộ từ (lowercase) hiện có trong database."""
        with self._connect() as conn:
            rows = conn.execute("SELECT word FROM vocabulary").fetchall()
        return {r[0].lower() for r in rows}

    def word_exists(self, word: str) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM vocabulary WHERE word = ?", (word.lower(),)
            ).fetchone()
        return row is not None

    def count(self) -> int:
        with self._connect() as conn:
            return conn.execute("SELECT COUNT(*) FROM vocabulary").fetchone()[0]

    # ------------------------------------------------------------------ #
    # Insert / Update
    # ------------------------------------------------------------------ #
    def add_word(
        self,
        word: str,
        definitions: str = "",
        band: str = "",
        description: str = "",
        example: str = "",
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO vocabulary (word, definitions, band, description, example)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(word) DO UPDATE SET
                    definitions = excluded.definitions,
                    band = excluded.band,
                    description = excluded.description,
                    example = excluded.example
                """,
                (word.lower().strip(), definitions, band, description, example),
            )

    def add_words_bulk(self, words: list[str]) -> int:
        words = sorted({w.lower().strip() for w in words if w.strip()})
        with self._connect() as conn:
            cur = conn.executemany(
                "INSERT OR IGNORE INTO vocabulary (word) VALUES (?)", # tự động bỏ qua trùng
                [(w,) for w in words],
            )
            return cur.rowcount

    def delete_word(self, word: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM vocabulary WHERE word = ?", (word.lower(),))