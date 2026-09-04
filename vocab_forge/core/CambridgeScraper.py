import requests
from bs4 import BeautifulSoup
from .Vocabulary import Vocabulary
class CambridgeScraper:
    BASE_URL = "https://dictionary.cambridge.org/dictionary/english/"
    
    @classmethod
    def fetch_word_info(cls, word: str) -> Vocabulary:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        formatted_word = word.lower().strip()
        try:
            response = requests.get(f"{cls.BASE_URL}{formatted_word}", headers=headers, timeout=5)
            if response.status_code != 200:
                return Vocabulary(word=word, definition="no found this word")

            soup = BeautifulSoup(response.text, 'html.parser')

            pos_elem = soup.find('span', class_='pos')
            word_type = pos_elem.text if pos_elem else ""

            band_elem = soup.find('span', class_='epp-xref')
            band = band_elem.text.strip() if band_elem else "B2"

            # 4. Lấy nghĩa đầu tiên # cần coi lại
            def_elem = soup.find('div', class_='def')
            definition = def_elem.text.strip() if def_elem else "is updating"

            # 5. Lấy câu ví dụ thực tế
            ex_elem = soup.find('span', class_='eg')
            example = ex_elem.text.strip() if ex_elem else ""

            return Vocabulary(
                word=word,
                definition=definition,
                word_type=word_type,
                band=band,
                example=example
            )
        except Exception as e:
            return Vocabulary(word=word, definition="error connection Cambridge", example=str(e))