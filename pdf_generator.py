from PIL import Image, ImageOps 

def process_and_create_pdf(image_paths, orientations, output_pdf_path):
    processed_images = []
    
    for img_path, angle in zip(image_paths, orientations):
        img = Image.open(img_path)
        
        img = ImageOps.exif_transpose(img) 
        
        img = img.convert('RGB')
        
        if angle != 0:
            img = img.rotate(angle, expand=True) 
            
        processed_images.append(img)
        print(f"Đã xử lý: {img_path} (Xoay {angle} độ)")

    # Lưu thành file PDF
    if processed_images:
        # Lấy ảnh đầu tiên làm trang 1, sau đó nối các ảnh còn lại vào
        processed_images[0].save(
            output_pdf_path, 
            save_all=True, 
            append_images=processed_images[1:],
            resolution=100.0
        )
        print(f"Đã xuất file PDF thành công tại: {output_pdf_path}")