import cv2
import easyocr
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
reader = easyocr.Reader(['en']) # AI model load chestunnam

# API to handle image upload
@app.route('/validate', methods=['POST'])
def validate_doc():
    if 'image' not in request.files:
        return jsonify({"error": "No image"}), 400
    
    # Image save cheyadam
    file = request.files['image']
    path = f"uploads/{file.filename}"
    file.save(path)

    # 1. OCR - Text Extraction
    results = reader.readtext(path, detail=0)
    text = " ".join(results).upper()

    # 2. Validation (Basic Example: Aadhaar checking)
    # Check if there are 12 digits
    digits = re.findall(r'\d', text)
    is_valid = len(digits) == 12

    return jsonify({
        "extracted_text": text,
        "is_valid": is_valid,
        "message": "Valid Document ✅" if is_valid else "Invalid Format ❌"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)