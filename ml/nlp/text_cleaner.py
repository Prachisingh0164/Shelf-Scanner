"""
Text Cleaner — NLP preprocessing for OCR output
Cleans and normalizes extracted book titles.
"""

import re


def clean_title(raw_text: str) -> str:
    """
    Clean OCR-extracted text to produce a readable book title.
    
    Steps:
    1. Remove special characters (keep letters, numbers, spaces, hyphens)
    2. Fix common OCR errors (0→O, 1→I, etc.)
    3. Title-case the result
    4. Strip excess whitespace
    """
    if not raw_text:
        return ""

    text = raw_text

    # Common OCR substitutions
    ocr_fixes = {
        r"\b0\b": "O",
        r"\b1\b": "I",
        r"\|": "I",
        r"@": "a",
    }
    for pattern, replacement in ocr_fixes.items():
        text = re.sub(pattern, replacement, text)

    # Remove non-printable / special chars except hyphens and apostrophes
    text = re.sub(r"[^a-zA-Z0-9\s\-\']", " ", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Title case
    text = text.title()

    return text
