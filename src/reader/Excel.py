import pandas as pd
from .TableReader import TableReader
from .BaseFileReader import FileReaderError
 
 
class Excel(TableReader):
    SUPPORTED_EXTENSIONS = {".xlsx", ".xls", ".csv"}
 
    def __init__(self, file_path: str, sheet_name=0):
        """
        sheet_name: tên/ index sheet muốn đọc (mặc định sheet đầu tiên).
                    Truyền sheet_name=None để đọc TẤT CẢ sheet -> trả về dict[str, DataFrame].
                    (Chỉ áp dụng cho .xlsx/.xls, .csv luôn chỉ có 1 "sheet")
        """
        self.sheet_name = sheet_name
        super().__init__(file_path)
 
    def read(self):
        try:
            if self.file_extension == ".csv":
                return pd.read_csv(self.file_path)
            return pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        except Exception as e:
            raise FileReaderError(f"Không thể đọc file excel '{self.file_path}': {e}") from e
 
    def extract_text(self) -> str:
        data = self.read()
 
        # Khi sheet_name=None, pandas trả về dict {sheet_name: DataFrame}
        if isinstance(data, dict):
            texts = []
            for _sheet, df in data.items():
                if df is None or df.empty:
                    continue
                cells = df.astype(str).values.flatten().tolist()
                headers = [str(c) for c in df.columns]
                texts.append(" ".join(headers + cells))
            return " ".join(texts)
 
        if data is None or data.empty:
            return ""
        cells = data.astype(str).values.flatten().tolist()
        headers = [str(c) for c in data.columns]
        return " ".join(headers + cells)
 