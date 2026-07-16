"""
gui.py

Tkinter GUI for the Mobile Document Scanner.
"""

import tkinter as tk
from tkinter import ttk


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
            width=15
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        ttk.Button(
            toolbar,
            text="Scan",
            width=15
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Button(
            toolbar,
            text="OCR",
            width=15
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        ttk.Button(
            toolbar,
            text="Export PDF",
            width=15
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

    def run(self):

        self.root.mainloop()