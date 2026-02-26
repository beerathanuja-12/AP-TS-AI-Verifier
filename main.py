from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import os
from preprocess import preprocess_image

app = FastAPI(title="AI Document Verification API")

# Enable CORS (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EasyOCR Reader globally
reader = easyocr.Reader(['en'], gpu=False)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Document Verification API. Use /verify to upload an image."}


@app.post("/verify")
async def verify_document(file: UploadFile = File(...)):
    try:
        # 1️⃣ Save uploaded file
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # 2️⃣ Preprocess image
        processed_img = preprocess_image(temp_path)

        # 3️⃣ Run OCR with paragraph grouping
        results = reader.readtext(
            processed_img,
            detail=1,
            paragraph=True
        )

        extracted_data = []
        total_confidence = 0.0

        for (bbox, text, prob) in results:
            clean_text = text.strip()

            if clean_text:  # Ignore empty text
                extracted_data.append({
                    "text": clean_text,
                    "confidence": round(float(prob) * 100, 2)
                })
                total_confidence += float(prob)

        avg_confidence = (
            total_confidence / len(extracted_data)
            if extracted_data else 0.0
        )

        avg_percentage = round(avg_confidence * 100, 2)

        # Remove temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return {
            "filename": file.filename,
            "status": "success",
            "extracted_text": " ".join(
                [item["text"] for item in extracted_data]
            ),
            "details": extracted_data,
          import re

full_text = " ".join([item["text"] for item in extracted_data])

# Extract Name (Capital words pattern)
name_match = re.search(r'\b[A-Z]{3,}(?:\s[A-Z]{3,})+\b', full_text)
name = name_match.group(0) if name_match else "Not Detected"

# Extract Student ID pattern (example pattern like 25KNIA61D2)
id_match = re.search(r'\b\d{2}[A-Z]{3,}\d+\b', full_text)
student_id = id_match.group(0) if id_match else "Not Detected"

# Extract Phone number
phone_match = re.search(r'\b\d{10}\b', full_text)
phone = phone_match.group(0) if phone_match else "Not Detected"

# Extract Institute
institute_match = re.search(r'NRI\s+Institute\s+of\s+Technology', full_text, re.IGNORECASE)
institute = institute_match.group(0) if institute_match else "Not Detected"

return {
    "filename": file.filename,
    "status": "success",
    "detected_fields": {
        "Institute": institute,
        "Name": name,
        "Student ID": student_id,
        "Phone": phone
    },
    "average_confidence": avg_percentage,
    "is_reliable": avg_percentage > 60
}

    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)