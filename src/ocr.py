"""
ocr.py

OCR functionality using EasyOCR.
"""

import easyocr
import cv2


class OCRProcessor:
    """
    Extract text from scanned document images using EasyOCR.
    """

    def __init__(self):
        """
        Initialize the EasyOCR reader.

        Supported languages:
        - English
        - Gujarati
        """

        self.reader = easyocr.Reader(
            ["en", "gu"]
        )

    def extract_text(self, image):
        """
        Perform OCR on a scanned document.

        Parameters
        ----------
        image : numpy.ndarray
            Scanned document image.

        Returns
        -------
        list
            EasyOCR results in the form:
            [(bounding_box, text, confidence), ...]
        """

        if image is None:
            raise ValueError("Input image cannot be None.")

        # EasyOCR accepts both grayscale and color images.
        if len(image.shape) == 3:
            image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

        return self.reader.readtext(image)