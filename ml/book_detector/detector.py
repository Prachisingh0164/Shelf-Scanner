"""
Book Detector — YOLOv8 + EasyOCR Pipeline
Detects book spines in images and extracts titles via OCR
"""

import os
import cv2
import numpy as np
from pathlib import Path


class BookDetector:
    """
    Book detection pipeline:
    1. YOLOv8 detects bounding boxes for books
    2. EasyOCR reads text from each bounding box
    """

    def __init__(self, model_path: str = None):
        self.model = None
        self.reader = None
        self._load_models(model_path)

    def _load_models(self, model_path: str = None):
        """Lazy-load YOLO and EasyOCR models."""
        try:
            from ultralytics import YOLO
            # Use custom weights if available, else pretrained COCO
            if model_path and Path(model_path).exists():
                self.model = YOLO(model_path)
            else:
                # yolov8n is pretrained on COCO; 'book' is class 84
                self.model = YOLO("yolov8n.pt")
            print("✅ YOLOv8 loaded")
        except ImportError:
            print("⚠️  ultralytics not installed. Run: pip install ultralytics")

        try:
            import easyocr
            self.reader = easyocr.Reader(["en"], gpu=False)
            print("✅ EasyOCR loaded")
        except ImportError:
            print("⚠️  easyocr not installed. Run: pip install easyocr")

    def detect_books(self, image_path: str) -> list:
        """
        Run YOLOv8 on image and return bounding boxes for detected books.
        Falls back to full-image OCR if YOLO is unavailable.
        """
        if self.model is None:
            return [{"bbox": None, "confidence": 1.0}]

        results = self.model(image_path, classes=[84])  # COCO class 84 = book
        boxes = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                boxes.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": round(conf, 3),
                })
        return boxes

    def extract_text(self, image_path: str, bbox: list = None) -> str:
        """
        Run EasyOCR on a bounding box region (or full image).
        Returns extracted text string.
        """
        if self.reader is None:
            return ""

        image = cv2.imread(image_path)
        if bbox:
            x1, y1, x2, y2 = bbox
            roi = image[y1:y2, x1:x2]
        else:
            roi = image

        results = self.reader.readtext(roi)
        text = " ".join([r[1] for r in results if r[2] > 0.4])
        return text.strip()

    def detect_and_read(self, image_path: str) -> dict:
        """
        Full pipeline: detect books → extract text from each.
        Returns dict with list of detected books.
        """
        boxes = self.detect_books(image_path)

        detected_books = []
        for i, box in enumerate(boxes):
            raw_text = self.extract_text(image_path, box.get("bbox"))
            detected_books.append({
                "id": i,
                "raw_text": raw_text,
                "title": raw_text,           # cleaned later by NLP pipeline
                "confidence": box["confidence"],
                "bbox": box.get("bbox"),
            })

        return {"detected_books": detected_books}
