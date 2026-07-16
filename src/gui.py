"""
gui.py

Tkinter GUI for the Mobile Document Scanner.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from src.scanner import DocumentScanner
from PIL import Image
from PIL import ImageTk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

class ScannerGUI:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "Mobile Document Scanner"
        )

        self.root.geometry("1200x800")

        self.root.minsize(
            1000,
            700
        )
        self.image_path = None
        self.preview_image = None
        self.scanner = DocumentScanner()
        self.scanned_image = None
        self.root.columnconfigure(
            0,
            weight=1
        )

        self.root.rowconfigure(
            2,
            weight=1
        )

        self.create_widgets()

    def create_widgets(self):

        title = ttk.Label(
            self.root,
            text="📄 Mobile Document Scanner",
            font=("Segoe UI", 22, "bold")
        )

        title.grid(
            row=0,
            column=0,
            pady=(20, 5)
        )

        subtitle = ttk.Label(
            self.root,
            text="Computer Vision Based Document Scanner",
            font=("Segoe UI", 11)
        )

        subtitle.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        preview_frame = ttk.LabelFrame(
            self.root,
            text="Document Preview",
            padding=15
        )

        preview_frame.grid(
            row=2,
            column=0,
            padx=20,
            pady=10,
            sticky="nsew"
        )

        preview_frame.columnconfigure(
            0,
            weight=1
        )

        preview_frame.rowconfigure(
            0,
            weight=1
        )

        self.preview = tk.Label(
            preview_frame,
            text="📄\n\nNo Image Selected\n\nClick 'Open Image' to begin",
            font=("Segoe UI", 18),
            justify="center",
            bg="#F5F5F5",
            relief="ridge",
            bd=2
        )

        self.preview.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        toolbar = ttk.Frame(
            self.root
        )

        toolbar.grid(
            row=3,
            column=0,
            pady=15
        )

        ttk.Button(
            toolbar,
            text="Open Image",
            width=15,
            command=self.open_image
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        ttk.Button(
            toolbar,
            text="Scan",
            width=15,
            command=self.scan_document
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Button(
            toolbar,
            text="OCR",
            width=15,
            command=self.run_ocr
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        ttk.Button(
            toolbar,
            text="Export PDF",
            width=15,
            command=self.export_pdf
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        ttk.Button(
            toolbar,
            text="Save",
            width=15
        ).grid(
            row=0,
            column=4,
            padx=5
        )

        ttk.Button(
            toolbar,
            text="Exit",
            width=15,
            command=self.root.destroy
        ).grid(
            row=0,
            column=5,
            padx=5
        )

        self.status = ttk.Label(
            self.root,
            text="Status : Ready",
            relief="sunken",
            anchor="w"
        )

        self.status.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=5,
            pady=(10, 5)
        )
    def open_image(self):
        """
        Open an image from disk and display it.
        """

        path = filedialog.askopenfilename(

            title="Select Document",

            filetypes=[

                ("Images", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")

            ]

        )

        if not path:
            return

        self.image_path = path

        self.display_image(path)

        self.status.config(

            text="Status : Image Loaded"

        )


    def display_image(self, path):
        """
        Display an image inside the preview area.
        """

        image = Image.open(path)

        image.thumbnail(

            (900, 520)

        )

        self.preview_image = ImageTk.PhotoImage(image)

        self.preview.config(

            image=self.preview_image,

            text=""

        )
    def scan_document(self):
        """
        Scan the selected document using the existing
        DocumentScanner pipeline.
        """

        if self.image_path is None:

            self.status.config(
                text="Status : Select an image first."
            )

            return

        try:

            self.scanner.load_image(
                self.image_path
            )

            self.scanner.preprocess()

            self.scanner.detect_edges()

            self.scanner.find_document()

            self.scanner.scan()

            self.scanned_image = self.scanner.scanned

            self.display_scanned_image()

            self.status.config(
                text="Status : Document scanned successfully."
            )

        except Exception as error:

            self.status.config(
                text=f"Status : {error}"
            )
    def display_scanned_image(self):
        """
        Display the scanned document.
        """

        image = self.scanned_image

        if len(image.shape) == 2:

            image = Image.fromarray(image)

        else:

            image = Image.fromarray(image[:, :, ::-1])

        image.thumbnail(
            (900, 520)
        )

        self.preview_image = ImageTk.PhotoImage(image)

        self.preview.config(

            image=self.preview_image,

            text=""

        )
    def export_pdf(self):
        """
        Export the scanned document as a PDF.
        """

        if self.scanner.scanned is None:

            self.status.config(
                text="Status : Scan a document first."
            )

            return

        try:

            pdf_path = self.scanner.export_pdf()

            self.status.config(
                text=f"Status : PDF saved to {pdf_path}"
            )

        except Exception as error:

            self.status.config(
                text=f"Status : {error}"
            )
    def run_ocr(self):
        """
        Extract text from the scanned document.
        """

        if self.scanner.scanned is None:

            self.status.config(
                text="Status : Scan a document first."
            )

            return

        try:

            results = self.scanner.extract_text()

            if not results:

                messagebox.showinfo(
                    "OCR Result",
                    "No text detected."
                )

            else:

                text = "\n".join(results)

                messagebox.showinfo(
                    "OCR Result",
                    text
                )

            self.status.config(
                text="Status : OCR completed."
            )

        except Exception as error:

            self.status.config(
                text=f"Status : {error}"
            )

    def run(self):

        self.root.mainloop()