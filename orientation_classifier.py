import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image # type: ignore

class OrientationModel:
    def __init__(self, model_path):
        # Tải mô hình đã được huấn luyện từ trước
        self.model = tf.keras.models.load_model(model_path)
        
        # Ánh xạ từ index dự đoán sang góc cần xoay (để trả về 0 độ)
        self.rotation_map = {
            0: 0,
            1: 90, 
            2: 180,
            3: -90
        }

    def predict_rotation(self, image_path):
        # Thay đổi kích thước ảnh cho phù hợp với đầu vào của CNN 
        img = image.load_img(image_path, target_size=(128, 128))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        # Dự đoán
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        
        return self.rotation_map[predicted_class]