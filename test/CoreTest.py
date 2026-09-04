import os
import sys

# 1. Mở đường dẫn trỏ về thư mục gốc dự án để Python nhìn thấy gói 'vocab_forge'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from vocab_forge.core.Vocabulary import Vocabulary
from vocab_forge.core.Trie.VocabularyTrie import VocabularyTrie 
from vocab_forge.core.reader.FileReaderFactory import FileReaderFactory
from vocab_forge.core.CambridgeScraper import CambridgeScraper

def run_vocab_forge_test():
    print("=== BAT DAU CHAY THU NGHIEM TANG CORE (VOCAB-FORGE) ===")
    
    # 1. Khởi tạo cấu trúc dữ liệu Trie (DSA) quản lý bộ nhớ từ vựng
    vocab_trie = VocabularyTrie()
    
    # 2. Xây dựng đường dẫn an toàn đến file mẫu nằm ở thư mục gốc 'data/sample.txt'
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = os.path.join(base_dir, "data", "sample.txt")
    
    if not os.path.exists(file_path):
        print(f"[LOI] Khong tim thay file tai {file_path}. Vui long tao file truoc!")
        return

    print(f"[INFO] Dang doc file tu duong dan: {file_path}")
    
    try:
        # 3. Sử dụng Design Pattern: Factory để chọn đúng Strategy đọc file
        reader = FileReaderFactory.get_reader(file_path)
        raw_words = reader.read_words(file_path)
        
        print(f"[INFO] Tim thay tong cong {len(raw_words)} dong trong file (co the co tu trung).")
        print("-" * 60)
        
        success_count = 0
        duplicate_count = 0
        
        for index, word in enumerate(raw_words, 1):
            print(f"\n[Tien trinh {index}/{len(raw_words)}] Dang xu ly tu: '{word}'")
            
            # 4. Kiểm tra trùng lặp bằng thuật toán Trie O(M)
            if vocab_trie.search(word):
                print(f"  [CANH BAO] Tu '{word}' DA TON TAI trong app. Bo qua khong them!")
                duplicate_count += 1
            else:
                print(f"  [TRA CUU] Tu moi! Dang ket noi Cambridge Dictionary de tra cuu...")
                # 5. Cào dữ liệu từ Cambridge
                vocab_obj = CambridgeScraper.fetch_word_info(word)
                
                # Thêm vào Trie
                is_inserted = vocab_trie.insert(vocab_obj)
                if is_inserted is None or is_inserted:
                    print(f"  [THANH CONG] Them thanh cong vao bo nhớ app:")
                    print(f"     Chi tiet: {vocab_obj}")
                    success_count += 1
                
        print("\n" + "=" * 60)
        print("BAO CAO KET QUA THUC THI:")
        print(f"   - Tong so tu doc tu file: {len(raw_words)}")
        print(f"   - So tu moi duoc them & tra cuu thành công: {success_count}")
        print(f"   - So tu trùng lặp bị loại bỏ: {duplicate_count}")
        print(f"   - Tổng số từ hiện có trong Trie: {success_count}")
        print("=" * 60)

    except Exception as e:
        print(f"[LOI] Da xay ra loi trong qua trinh chay: {e}")

if __name__ == "__main__":
    run_vocab_forge_test()