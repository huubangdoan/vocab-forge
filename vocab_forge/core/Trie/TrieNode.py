from vocab_forge.core.Vocabulary import Vocabulary
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.data: Vocabulary = None  # Lưu trữ thông tin chi tiết của từ

class VocabularyTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, vocab: 'Vocabulary') -> bool:
        """Thêm từ vào Trie. Trả về True nếu thêm thành công, False nếu đã tồn tại."""
        node = self.root
        word = vocab.word
        
        # Kiểm tra trùng lặp trước khi thêm
        if self.search(word):
            return False 

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.data = vocab
        return True

    def search(self, word: str) -> bool:
        """Kiểm tra từ vựng đã tồn tại trong app hay chưa (O(M) với M là độ dài từ)."""
        node = self.root
        for char in word.lower().strip():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def get_vocab(self, word: str) -> 'Vocabulary':
        """Lấy thông tin chi tiết của từ vựng nếu có."""
        node = self.root
        for char in word.lower().strip():
            if char not in node.children:
                return None
            node = node.children[char]
        return node.data if node.is_end_of_word else None