"""
cli.py
------
Toàn bộ logic của chương trình dòng lệnh: parse argument, đọc file,
tìm từ mới, scrape Cambridge, lưu DB, in kết quả.

main.py chỉ gọi main() ở đây, không chứa logic gì cả.
"""

import argparse
import sys

from reader.ReaderFactory import get_reader
from database.VocabularyDB import VocabularyDB
from database.VocabularyFinder import VocabularyFinder
from reader.BaseFileReader import FileReaderError
from web_scraper.CambridgeScraper import CambridgeScraper
from web_scraper.BaseScraper import ScraperError


# ------------------------------------------------------------------ #
# Argument parsing
# ------------------------------------------------------------------ #
def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="find new words in the following file."
    )
    parser.add_argument("files", nargs="+", help="list of scanning file(.txt/.docx/.pdf/.xlsx/.csv)")
    parser.add_argument("--db", default="vocabulary.db", help="link SQLite database")
    parser.add_argument("--save", action="store_true",
                         help="save database")
    parser.add_argument("--scrape", action="store_true",
                         help="auto store")
    parser.add_argument("--delay", type=float, default=1.0,
                         help="deylay to keep safe")
    return parser


# ------------------------------------------------------------------ #
# Các bước xử lý
# ------------------------------------------------------------------ #
def load_readers(file_paths: list[str]) -> list:
    readers = []
    for path in file_paths:
        try:
            readers.append(get_reader(path))
        except FileReaderError as e:
            print(f"[error] {e}", file=sys.stderr)
    return readers


def print_scan_result(db: VocabularyDB, result: dict) -> None:
    for file_name, new_words in result["per_file"].items():
        print(f"--- {file_name} ---")
        if new_words:
            for w in sorted(new_words):
                print(f"  + {w}")
        else:
            print("  (no new words)")
        print()

    print(f"=== Total: {len(result['combined'])} NewWord (no duplicated) ===")
    for w in sorted(result["combined"]):
        print(f"  {w}")


def save_placeholder(finder: VocabularyFinder, combined_words: set) -> None:
    added = finder.save_new_words_to_db(combined_words)
    print(f"\nsaved {added} in "
          f"definitions/band/description/example sau).")


def scrape_and_save(db: VocabularyDB, combined_words: set, delay: float) -> None:
    print(f"\nis finding {len(combined_words)} on Cambridge Dictionary...")
    scraper = CambridgeScraper(delay_seconds=delay)
    try:
        entries = scraper.fetch_words(sorted(combined_words))
    except ScraperError as e:
        print(f"[error] {e}", file=sys.stderr)
        entries = {}
    finally:
        scraper.close()

    added, not_found = 0, []
    for word, entry in entries.items():
        if entry is None:
            not_found.append(word)
            continue
        db.add_word(
            word=entry["word"],
            definitions=entry["definitions"],
            band=entry["band"],
            description=entry["description"],
            example=entry["example"],
        )
        added += 1
        print(f"  [OK] {word} [{entry['band'] or '—'}]: {entry['definitions'][:60]}...")

    print(f"\nsave {added} to database.")
    if not_found:
        print(f"can't find Cambridge: {', '.join(not_found)}")


# ------------------------------------------------------------------ #
# Entry point
# ------------------------------------------------------------------ #
def run(args: argparse.Namespace) -> None:
    db = VocabularyDB(args.db)
    finder = VocabularyFinder(db)

    readers = load_readers(args.files)
    if not readers:
        print("invalid file")
        return

    result = finder.find_new_words_multi(readers)
    print_scan_result(db, result)

    if args.scrape and result["combined"]:
        scrape_and_save(db, result["combined"], args.delay)
    elif args.save and result["combined"]:
        save_placeholder(finder, result["combined"])


def run_files(
    files: list[str],
    db_path: str = "vocabulary.db",
    save: bool = False,
    scrape: bool = False,
    delay: float = 1.0,
) -> None:
    """
    Chạy pipeline trực tiếp với list file khai báo sẵn trong code,
    KHÔNG cần gõ qua terminal / argparse. Dùng khi muốn chạy bằng nút
    Run trong IDE (VD: VSCode) thay vì gõ lệnh.

    Ví dụ dùng trong main.py:
        run_files(
            files=["bai1.pdf", "bai2.docx"],
            db_path="vocabulary.db",
            save=True,
        )
    """
    args = argparse.Namespace(
        files=files, db=db_path, save=save, scrape=scrape, delay=delay
    )
    run(args)


def main() -> None:
    args = build_arg_parser().parse_args()
    run(args)