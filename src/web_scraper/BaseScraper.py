
import time
from abc import ABC, abstractmethod
 
import requests
 
 
class ScraperError(Exception):
    """Exception chung cho mọi lỗi liên quan đến việc scrape từ điển."""
    pass
 
 
class BaseScraper(ABC):
    #: Header mặc định, lớp con có thể override nếu trang cần header riêng
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        )
    }
 
    def __init__(self, delay_seconds: float = 1.0, timeout: int = 10):
        """
        delay_seconds: thời gian nghỉ giữa các request liên tiếp khi tra nhiều từ,
                       tránh spam / bị chặn IP.
        timeout: timeout (giây) cho mỗi request.
        """
        self.delay_seconds = delay_seconds
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
 
    # ------------------------------------------------------------------ #
    # Bắt buộc lớp con triển khai
    # ------------------------------------------------------------------ #
    @abstractmethod
    def build_url(self, word: str) -> str:
        """Trả về URL trang chi tiết của `word` trên trang từ điển này."""
        raise NotImplementedError
 
    @abstractmethod
    def parse(self, word: str, html: str) -> dict | None:
        """
        Parse HTML thô -> dict chuẩn:
            {"word": str, "definitions": str, "band": str,
             "description": str, "example": str}
        Trả về None nếu không tìm thấy nghĩa / cấu trúc trang không khớp.
        """
        raise NotImplementedError
 
    # ------------------------------------------------------------------ #
    # Logic dùng chung - lớp con KHÔNG cần override
    # ------------------------------------------------------------------ #
    def fetch_word(self, word: str) -> dict | None:
        """Tra 1 từ: gọi request -> parse -> trả dict hoặc None."""
        word = word.strip().lower()
        url = self.build_url(word)
 
        try:
            resp = self.session.get(url, timeout=self.timeout)
        except requests.RequestException as e:
            raise ScraperError(
                f"[{self.__class__.__name__}] Lỗi kết nối khi tra từ '{word}': {e}"
            ) from e
 
        if resp.status_code == 404:
            return None  # từ không tồn tại trên trang này
        if resp.status_code != 200:
            raise ScraperError(
                f"[{self.__class__.__name__}] Status {resp.status_code} cho từ '{word}'"
            )
 
        return self.parse(word, resp.text)
 
    def fetch_words(self, words: list[str]) -> dict[str, dict | None]:
        """
        Tra nhiều từ liên tiếp, có delay giữa mỗi request.
        Trả về dict {word: result_dict_or_None}. Lỗi từng từ không làm dừng cả batch.
        """
        results = {}
        for i, word in enumerate(words):
            try:
                results[word] = self.fetch_word(word)
            except ScraperError as e:
                print(f"[CẢNH BÁO] {e}")
                results[word] = None
 
            if i < len(words) - 1:
                time.sleep(self.delay_seconds)
 
        return results
 
    def close(self) -> None:
        self.session.close()
 
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(delay_seconds={self.delay_seconds})"
 