"""
pdf_utils.py

Utilities for exporting scanned documents as PDF files.
"""

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

import config


class PDFExporter:
    """
    Export scanned images as PDF documents.
    """

    def __init__(self):
        """
        Initialize the PDF exporter.
        """

        os.makedirs(
            config.OUTPUT_DIR,
            exist_ok=True
        )

    def export(self, image_path, pdf_path):
        """
        Export an image as a single-page PDF.

        Parameters
        ----------
        image_path : str
            Path to the scanned image.

        pdf_path : str
            Output PDF path.
        """

        pdf = canvas.Canvas(
            pdf_path,
            pagesize=A4
        )

        page_width, page_height = A4

        image = ImageReader(image_path)

        img_width, img_height = image.getSize()

        scale = min(
            page_width / img_width,
            page_height / img_height
        )

        width = img_width * scale
        height = img_height * scale

        x = (page_width - width) / 2
        y = (page_height - height) / 2

        pdf.drawImage(
            image,
            x,
            y,
            width=width,
            height=height
        )

        pdf.save()