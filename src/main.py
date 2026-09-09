

from cli import run_files

if __name__ == "__main__":
    run_files(
        files=[r"data\sample.txt"],   # <-- truyền file cần quét vào đây
        db_path="vocabulary.db",
        save=True,
        scrape=True,
    )