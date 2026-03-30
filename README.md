# 📄 Auto Image Orientation & PDF Generator (CNN)

Dự án này sử dụng Mạng nơ-ron tích chập (Convolutional Neural Network - CNN) để tự động nhận diện hướng của các bức ảnh tài liệu chụp bằng điện thoại (bị xoay ngang, lộn ngược), tự động xoay chúng về đúng chiều thẳng đứng và ghép tất cả lại thành một file PDF duy nhất để nộp bài.

## ✨ Tính năng nổi bật
- **Tự động sinh dữ liệu (Data Augmentation):** Chỉ cần cung cấp ảnh gốc ở góc 0°, script sẽ tự động nội suy và sinh ra bộ dataset với các góc (0°, 90°, 180°, 270°).
- **Phân loại ảnh thông minh:** Sử dụng kiến trúc CNN xây dựng bằng TensorFlow/Keras để dự đoán góc xoay của ảnh với độ chính xác cao (> 97%).
- **Xử lý EXIF tự động:** Khắc phục triệt để lỗi hiển thị "ảo giác" trên Windows bằng cách đọc thẻ EXIF của ảnh gốc trước khi xử lý.
- **Xuất PDF chuẩn hóa:** Tự động sắp xếp ảnh theo thứ tự số (1, 2, 3...) và xuất ra một file `submission_final.pdf` gọn gàng.

## 🛠 Cấu trúc thư mục

\`\`\`text
Auto-Image-Orientation-CNN/
│
├── dataset/                # (Tự động sinh) Thư mục chứa dữ liệu huấn luyện
├── input_images/           # Nơi chứa các ảnh bài tập cần xử lý (VD: 1.jpg, 2.jpg)
├── output/                 # (Tự động sinh) Nơi xuất file PDF cuối cùng
├── models/                 # (Tự động sinh) Nơi lưu file mô hình .keras
│
├── raw_0_degree_images/    # Nơi chứa ảnh gốc nằm thẳng để sinh dataset
│
├── generate_dataset.py     # Script tự động tạo dữ liệu huấn luyện (Clean Code)
├── train_cnn.py            # Cấu trúc mạng CNN và quá trình huấn luyện
├── orientation_classifier.py # Module dự đoán góc xoay bằng mô hình đã học
├── pdf_generator.py        # Module xử lý ảnh và ghép PDF bằng Pillow
└── main.py                 # File thực thi chính điều phối toàn bộ luồng
\`\`\`

## 🚀 Hướng dẫn cài đặt

**1. Yêu cầu hệ thống:**
- Python 3.11 hoặc 3.12 (Khuyến nghị dùng Môi trường ảo - Virtual Environment).
- Hệ điều hành: Windows / macOS / Linux.

**2. Cài đặt các thư viện cần thiết:**
Mở Terminal, kích hoạt môi trường ảo và chạy lệnh sau:
\`\`\`bash
pip install tensorflow pillow numpy matplotlib
\`\`\`

## 💡 Hướng dẫn sử dụng

Dự án được chia làm 2 giai đoạn: Huấn luyện AI và Sử dụng thực tế.

### Giai đoạn 1: Huấn luyện mô hình (Chỉ làm 1 lần)
1. Bỏ từ 50-100 tấm ảnh chụp tài liệu **đúng chiều (thẳng đứng)** vào thư mục `raw_0_degree_images/`.
2. Chạy lệnh sinh dữ liệu tự động:
   \`\`\`bash
   python generate_dataset.py
   \`\`\`
   *(Máy sẽ tự tạo ra hàng trăm ảnh bị lộn xộn ở các góc khác nhau trong thư mục `dataset/`)*
3. Chạy lệnh huấn luyện mô hình CNN:
   \`\`\`bash
   python train_cnn.py
   \`\`\`
   *(Sau khi chạy xong ~10 Epochs, mô hình sẽ được lưu tại `models/orientation_model.keras`)*

### Giai đoạn 2: Sử dụng thực tế
1. Bỏ các ảnh bạn vừa chụp bài tập (có thể bị ngang, ngược lộn xộn) vào thư mục `input_images/`. 
   *Lưu ý: Đặt tên file theo thứ tự trang (VD: `1.jpg`, `2.jpg`, `3.png`...).*
2. Chạy file thực thi chính:
   \`\`\`bash
   python main.py
   \`\`\`
3. Vào thư mục `output/` để lấy file `submission_final.pdf`

## 📌 Công nghệ sử dụng
- **Python 3.11**
- **Deep Learning Framework:** TensorFlow, Keras
- **Image Processing:** Pillow (PIL)
- **File System:** `pathlib`, `glob`