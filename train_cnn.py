import tensorflow as tf
from tensorflow.keras import layers, models # type: ignore
import matplotlib.pyplot as plt

# 1. Thiết lập tham số
IMG_HEIGHT = 128
IMG_WIDTH = 128
BATCH_SIZE = 32
DATASET_DIR = "dataset"

# 2. Load dữ liệu từ thư mục
print("Đang tải dữ liệu...")
train_ds = tf.keras.utils.image_dataset_from_directory(
  DATASET_DIR,
  validation_split=0.2, 
  subset="training",
  seed=123,
  image_size=(IMG_HEIGHT, IMG_WIDTH),
  batch_size=BATCH_SIZE,
  class_names=['0', '90', '180', '270']
)

val_ds = tf.keras.utils.image_dataset_from_directory(
  DATASET_DIR,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(IMG_HEIGHT, IMG_WIDTH),
  batch_size=BATCH_SIZE,
  class_names=['0', '90', '180', '270']
)

# 3. Xây dựng cấu trúc mạng CNN
model = models.Sequential([
  layers.Rescaling(1./255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)), # Chuẩn hóa pixel về [0, 1]
  
  # Khối đặc trưng 1
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  
  # Khối đặc trưng 2
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  
  # Khối đặc trưng 3
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  
  # Bộ phân loại
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(4, activation='softmax') # 4 đầu ra tương ứng với 4 góc độ
])

# 4. Biên dịch mô hình
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['accuracy'])

# 5. Bắt đầu huấn luyện
print("Bắt đầu huấn luyện...")
epochs = 20 # Số vòng lặp qua toàn bộ dữ liệu (bạn có thể tăng lên 15-20 nếu chưa chính xác)
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

# 6. Lưu mô hình để sau này dùng
model.save('models/orientation_model.keras')
print("Đã lưu mô hình tại models/orientation_model.keras")