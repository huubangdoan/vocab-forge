from pathlib import Path
from .BaseFileReader import BaseFileReader, FileReaderError
from .Txt import Txt
from .Doc import Doc
from .PDF import PDF
from .Excel import Excel

_EXTENSION_MAP = {
    ".txt": Txt,
    ".doc": Doc,
    ".docx": Doc,
    ".pdf": PDF,
    ".xlsx": Excel,
    ".xls": Excel,
    ".csv": Excel,
}


def get_reader(file_path: str, **kwargs) -> BaseFileReader:
    """
    Trả về instance reader phù hợp cho file_path.
    kwargs sẽ được truyền tiếp vào constructor của reader tương ứng
    (vd: sheet_name cho Excel, encoding cho Txt).
    """
    ext = Path(file_path).suffix.lower()
    reader_cls = _EXTENSION_MAP.get(ext)
    if reader_cls is None:
        raise FileReaderError(
            f"Không có reader nào hỗ trợ phần mở rộng '{ext}'. "
            f"Hỗ trợ: {sorted(_EXTENSION_MAP.keys())}"
        )
    return reader_cls(file_path, **kwargs)