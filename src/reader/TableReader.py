from abc import abstractmethod
import pandas as pd
from .BaseFileReader import BaseFileReader
class TableReader(BaseFileReader):
    @abstractmethod
    def read(self) -> pd.DataFrame:
        raise NotImplementedError
 
    def extract_text(self) -> str:
        df = self.read()
        if df is None or df.empty:
            return ""
        # Ép toàn bộ dữ liệu (kể cả header) về string rồi nối lại thành 1 văn bản
        cells = df.astype(str).values.flatten().tolist()
        headers = [str(c) for c in df.columns]
        return " ".join(headers + cells)
 
