from .BaseFileReader import BaseFileReader
import pandas as pd
class ExcelFileReader(BaseFileReader):
    def read_words(self, file_path: str) -> list[str]:
        """Đọc file Excel (.xlsx, .xls) dùng Pandas, lấy cột đầu tiên chứa từ vựng."""
        df = pd.read_excel(file_path)
        # Lấy dữ liệu ở cột đầu tiên, chuyển thành list và lọc bỏ giá trị rỗng
        words = df.iloc[:, 0].dropna().astype(str).tolist()
        return [w.strip() for w in words if w.strip()]