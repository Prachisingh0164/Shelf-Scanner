"""
Scanner Route — /api/scan
Handles image upload, YOLO detection, OCR extraction
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../ml"))
from book_detector.detector import BookDetector
from ml.nlp.text_cleaner import clean_title

router = APIRouter()

# Initialize detector (loaded once at startup)
detector = None

def get_detector():
    global detector
    if detector is None:
        detector = BookDetector()
    return detector


@router.post("/")
async def scan_bookshelf(image: UploadFile = File(...)):
    """
    Upload a bookshelf image.
    Returns detected books with titles and bounding boxes.
    """
    # Validate file type
    if image.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WEBP images are supported.")

    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}_{image.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    try:
        det = get_detector()
        results = det.detect_and_read(file_path)

        # Clean OCR titles
        for book in results["detected_books"]:
            book["title"] = clean_title(book.get("raw_text", ""))

        return JSONResponse({
            "success": True,
            "image_id": file_id,
            "file_path": f"/uploads/{file_id}_{image.filename}",
            "book_count": len(results["detected_books"]),
            "detected_books": results["detected_books"],
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

    finally:
        # Optionally clean up file after processing
        pass


@router.post("/demo")
async def demo_scan():
    """
    Returns demo results without requiring a real image.
    Useful for testing the frontend.
    """
    return {
        "success": True,
        "image_id": "demo",
        "book_count": 4,
        "detected_books": [
            {"title": "Atomic Habits", "confidence": 0.94, "bbox": [10, 20, 100, 300]},
            {"title": "The Psychology of Money", "confidence": 0.89, "bbox": [110, 20, 200, 300]},
            {"title": "Sapiens", "confidence": 0.92, "bbox": [210, 20, 300, 300]},
            {"title": "Deep Work", "confidence": 0.87, "bbox": [310, 20, 400, 300]},
        ],
    }
