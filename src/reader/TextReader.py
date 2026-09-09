from abc import abstractmethod
from .BaseFileReader import BaseFileReader
 
 
class TextReader(BaseFileReader):
    @abstractmethod
    def read(self) -> str:
        raise NotImplementedError
 
    def extract_text(self) -> str:
        content = self.read()
        return content if content else ""