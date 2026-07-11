"""
ocr.py

OCR functionality using EasyOCR.
"""

import easyocr


class OCRProcessor:
    """
    Wrapper around EasyOCR.

    Provides a clean interface for extracting
    structured text from scanned documents.
    """

    def __init__(self):
        """
        Initialize the EasyOCR reader.
        """

        self.reader = easyocr.Reader(
            ["en"]
        )

    def extract_text(self, image):
        """
        Perform OCR on an image.

        Parameters
        ----------
        image : numpy.ndarray
            Image to process.

        Returns
        -------
        list
            OCR results as structured dictionaries.
        """

        raw_results = self.reader.readtext(image)

        results = []

        for bbox, text, confidence in raw_results:

            results.append({

                "text": text,

                "confidence": round(
                    float(confidence),
                    3
                ),

                "bbox": bbox

            })

        return results