"""
pdf_utils.py

Utilities for exporting scanned documents as PDF files.
"""

import config
import os
import cv2
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class PDFExporter:
    """
    Export scanned images as PDF documents.
    """

    def export(self, image_path, pdf_path):
        """
        Export an image as a single-page PDF.
        """

        pdf = canvas.Canvas(
            pdf_path,
            pagesize=A4
        )

        page_width, page_height = A4

        margin = config.PDF_MARGIN

        available_width = page_width - (2 * margin)
        available_height = page_height - (2 * margin)

        image = ImageReader(image_path)

        img_width, img_height = image.getSize()

        scale = min(
            available_width / img_width,
            available_height / img_height
        )

        width = img_width * scale
        height = img_height * scale

        x = margin + (available_width - width) / 2
        y = margin + (available_height - height) / 2

        pdf.drawImage(
            image,
            x,
            y,
            width=width,
            height=height
        )

        pdf.save()