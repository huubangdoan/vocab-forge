from bs4 import BeautifulSoup

from .BaseScraper import BaseScraper


class CambridgeScraper(BaseScraper):
    BASE_URL = "https://dictionary.cambridge.org/dictionary/english/{word}"

    # Bật lên True để in ra HTML thật của block đầu tiên khi debug
    DEBUG = False

    def build_url(self, word: str) -> str:
        return self.BASE_URL.format(word=word)

    def parse(self, word: str, html: str) -> dict | None:
        """
        Cambridge hay đổi HTML nên mình dùng nhiều selector dự phòng
        cho từng phần tử, thử lần lượt cho tới khi có kết quả.
        """
        soup = BeautifulSoup(html, "html.parser")

        # Khối chứa 1 "entry" hoàn chỉnh (gồm pos + các def-block con)
        entry_body = (
            soup.select_one(".pr.entry-body__el")
            or soup.select_one(".entry-body__el")
            or soup
        )

        def_blocks = (
            entry_body.select("div.def-block")
            or entry_body.select(".def-block")
            or soup.select("div.def-block")
        )

        if self.DEBUG:
            print(f"[DEBUG] {word}: found {len(def_blocks)} def_blocks")
            if def_blocks:
                print(def_blocks[0].prettify()[:1500])

        if not def_blocks:
            return None

        first_block = def_blocks[0]

        # ---- description (từ loại: noun, verb, adj...) ----
        # Ưu tiên tìm NGAY TRONG entry_body (gần first_block), tránh lấy
        # nhầm pos của 1 entry khác nằm sau trong trang.
        pos_el = (
            entry_body.select_one(".pos.dpos")
            or entry_body.select_one("span.pos")
            or entry_body.select_one(".dpos")
            or first_block.select_one(".pos")
        )
        description = pos_el.get_text(strip=True) if pos_el else ""

        # ---- band/level (A1..C2) ----
        band_el = (
            first_block.select_one("span.epp-xref")
            or first_block.select_one(".dxref-w")
            or first_block.select_one(".def-info .epp-xref")
        )
        band = band_el.get_text(strip=True) if band_el else ""

        # ---- definitions ----
        all_defs = []
        for block in def_blocks[:3]:
            d = (
                block.select_one("div.ddef_d.db")
                or block.select_one("div.def")
                or block.select_one(".ddef_d")
            )
            if d:
                text = d.get_text(strip=True).rstrip(":")
                if text and text not in all_defs:
                    all_defs.append(text)

        # ---- example ----
        # Cambridge thường lồng: div.examp.dexamp > span.eg.deg
        example_el = (
            first_block.select_one(".examp .eg")
            or first_block.select_one(".dexamp .deg")
            or first_block.select_one(".examp")
            or first_block.select_one(".deg")
        )
        example = example_el.get_text(strip=True) if example_el else ""

        # Nếu vẫn không có example ở block đầu, thử tìm ở các block sau
        if not example:
            for block in def_blocks[1:]:
                ex = block.select_one(".examp .eg") or block.select_one(".deg")
                if ex:
                    example = ex.get_text(strip=True)
                    break

        return {
            "word": word,
            "definitions": " | ".join(all_defs),
            "band": band,
            "description": description,
            "example": example,
        }