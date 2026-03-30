import os
import glob
from orientation_classifier import OrientationModel
from pdf_generator import process_and_create_pdf

def main():
    # 1. Đường dẫn cấu hình
    input_folder = "input_images"
    output_pdf = "output/submission_final.pdf"
    model_path = "models/orientation_model.keras" 

    # 2. TÌM TẤT CẢ CÁC LOẠI ẢNH (JPG, PNG, JPEG)
    image_paths = []
    for ext in ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.PNG'):
        image_paths.extend(glob.glob(os.path.join(input_folder, ext)))
    
    # Loại bỏ file trùng lặp do Windows đọc cả đuôi hoa/thường
    image_paths = list(set(image_paths))
    
    if not image_paths:
        print("Không tìm thấy ảnh nào trong thư mục input_images!")
        return

    # 3. SẮP XẾP TÊN FILE CHUẨN XÁC THEO SỐ
    # Lệnh lambda sẽ bóc tách đuôi .png ra, lấy phần số nguyên 
    try:
        image_paths.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    except ValueError:
        print("Lưu ý: Tên file có chứa chữ cái, sẽ được sắp xếp theo bảng chữ cái mặc định.")
        image_paths.sort()

    # 4. Khởi tạo mô hình CNN 
    print("Đang tải mô hình CNN...")
    classifier = OrientationModel(model_path) 

    angles_to_rotate = []
    
    # 5. Quét từng ảnh để tìm hướng (Problem 1)
    for path in image_paths:
        angle = classifier.predict_rotation(path) 
        angles_to_rotate.append(angle)

    # 6. Xoay và tạo PDF (Problem 2)
    print("Đang tạo PDF...")
    process_and_create_pdf(image_paths, angles_to_rotate, output_pdf)

if __name__ == "__main__":
    main()