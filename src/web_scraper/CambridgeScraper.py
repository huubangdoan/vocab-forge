import re
from bs4 import BeautifulSoup

from .BaseScraper import BaseScraper


def clean_text(text: str) -> str:
    """Chuẩn hoá khoảng trắng: gộp nhiều space thành 1, bỏ space thừa trước dấu câu."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return text


class CambridgeScraper(BaseScraper):
    BASE_URL = "https://dictionary.cambridge.org/dictionary/english/{word}"

    DEBUG = False

    def build_url(self, word: str) -> str:
        return self.BASE_URL.format(word=word)

    def parse(self, word: str, html: str) -> dict | None:
        soup = BeautifulSoup(html, "html.parser")

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

        # ---- description (pos) ----
        pos_el = (
            entry_body.select_one(".pos.dpos")
            or entry_body.select_one("span.pos")
            or entry_body.select_one(".dpos")
            or first_block.select_one(".pos")
        )
        description = clean_text(pos_el.get_text(" ", strip=True)) if pos_el else ""

        # ---- band ----
        band_el = (
            first_block.select_one("span.epp-xref")
            or first_block.select_one(".dxref-w")
            or first_block.select_one(".def-info .epp-xref")
        )
        band = clean_text(band_el.get_text(" ", strip=True)) if band_el else ""

        # ---- definitions ----
        all_defs = []
        for block in def_blocks[:3]:
            d = (
                block.select_one("div.ddef_d.db")
                or block.select_one("div.def")
                or block.select_one(".ddef_d")
            )
            if d:
                text = clean_text(d.get_text(" ", strip=True)).rstrip(":")
                if text and text not in all_defs:
                    all_defs.append(text)

        # ---- example ----
        example_el = (
            first_block.select_one(".examp .eg")
            or first_block.select_one(".dexamp .deg")
            or first_block.select_one(".examp")
            or first_block.select_one(".deg")
        )
        example = clean_text(example_el.get_text(" ", strip=True)) if example_el else ""

        if not example:
            for block in def_blocks[1:]:
                ex = block.select_one(".examp .eg") or block.select_one(".deg")
                if ex:
                    example = clean_text(ex.get_text(" ", strip=True))
                    break

        return {
            "word": word,
            "definitions": " | ".join(all_defs),
            "band": band,
            "description": description,
            "example": example,
        }