import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Performs basic image preprocessing for better OCR results.
    """
    # 1. Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or invalid format")

    # 2. Resize (optional, but can help if images are too small/large)
    # We'll maintain aspect ratio
    height, width = img.shape[:2]
    max_dim = 1000
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        img = cv2.resize(img, None, fx=2.0, fy=2.0)
    # 3. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 4. Noise Removal (Median Blur)
    denoised = cv2.medianBlur(gray, 3)

    # 5. Thresholding (Binarization)
    # Otsu's thresholding automatically calculates the best threshold value
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

if __name__ == "__main__":
    # Test preprocessing
    try:
        processed = preprocess_image("test_sample.jpg")
        cv2.imwrite("processed_sample.jpg", processed)
        print("Preprocessing complete. Saved as processed_sample.jpg")
    except Exception as e:
        print(f"Error: {e}")
