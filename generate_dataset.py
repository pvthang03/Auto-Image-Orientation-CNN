from pathlib import Path
from PIL import Image

# 1. Định nghĩa Hằng số (Constants)
DATASET_DIR = Path("dataset")
RAW_IMAGES_DIR = Path("raw_0_degree_images")
ANGLES = [0, 90, 180, 270]
TARGET_SIZE = (128, 128)
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

def setup_directories(base_dir: Path, angles: list[int]) -> None:
    """Tạo các thư mục con tương ứng với từng góc xoay."""
    for angle in angles:
        (base_dir / str(angle)).mkdir(parents=True, exist_ok=True)

def get_image_paths(source_dir: Path, extensions: set[str]) -> list[Path]:
    """Quét và trả về danh sách các file ảnh hợp lệ (không phân biệt hoa/thường)."""
    if not source_dir.exists():
        return []
    
    # pathlib giúp lấy đuôi file (.suffix) và chuyển về chữ thường để so sánh dễ dàng
    return [
        file_path for file_path in source_dir.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in extensions
    ]

def process_and_augment_images(image_paths: list[Path], dest_dir: Path, angles: list[int]) -> None:
    """Đọc ảnh gốc, xoay ra các góc, resize và lưu vào đúng thư mục."""
    print("Bắt đầu sinh dữ liệu, vui lòng đợi...")
    
    for idx, img_path in enumerate(image_paths):
        try:
            # Dùng 'with' để đảm bảo file ảnh luôn được đóng sau khi xử lý xong
            with Image.open(img_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                for angle in angles:
                    rotated_img = img.rotate(-angle, expand=True) 
                    
                    # Dùng dấu / của pathlib để nối đường dẫn cực kỳ trực quan
                    save_path = dest_dir / str(angle) / f"img_{idx}_{angle}.jpg"
                    rotated_img.resize(TARGET_SIZE).save(save_path)
                    
        except Exception as e:
            print(f"⚠️ Lỗi khi xử lý ảnh {img_path.name}: {e}")

def main():
    print(f"Đang quét thư mục '{RAW_IMAGES_DIR}'...")
    
    # Khởi tạo thư mục
    setup_directories(DATASET_DIR, ANGLES)
    
    # Lấy danh sách ảnh
    raw_images = get_image_paths(RAW_IMAGES_DIR, ALLOWED_EXTENSIONS)
    print(f"Tìm thấy: {len(raw_images)} ảnh gốc!")

    # Kiểm tra đầu vào và thực thi
    if not raw_images:
        print("-" * 50)
        print("❌ LỖI: Không có ảnh nào được tìm thấy!")
        print("Hãy kiểm tra lại:")
        print(f"1. Thư mục '{RAW_IMAGES_DIR}' đã nằm cùng chỗ với file code chưa?")
        print("2. Đuôi ảnh của bạn có phải là .HEIC (iPhone) không? (Nếu có, hãy chuyển sang jpg/png).")
        print("-" * 50)
    else:
        process_and_augment_images(raw_images, DATASET_DIR, ANGLES)
        print("✅ Đã tạo xong dataset thành công! Hãy mở thư mục dataset ra kiểm tra.")

if __name__ == "__main__":
    main()