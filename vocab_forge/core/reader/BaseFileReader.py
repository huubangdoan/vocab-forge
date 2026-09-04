from abc import ABC, abstractmethod

class BaseFileReader(ABC):
    @abstractmethod
    def read_words(self, file_path: str) -> list[str]:
        pass