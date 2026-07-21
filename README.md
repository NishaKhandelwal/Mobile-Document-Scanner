# 📄 Mobile Document Scanner

A modular, production-inspired document scanner built with **Python** and **OpenCV** that automatically detects documents, corrects perspective distortion, enhances image quality, extracts text using OCR, and exports scanned documents as PDF files.

The project is designed as a portfolio-quality implementation to demonstrate practical **Computer Vision**, **Image Processing**, **OCR Integration**, and **Modular Software Architecture** using Python.

---

## ✨ Features

### 📑 Document Scanning

- Automatic document boundary detection
- Intelligent contour scoring for document selection
- Perspective correction using four-point transformation
- Multiple scan modes:
  - Black & White
  - Grayscale
  - Color
- Adaptive thresholding for scanner-quality output

---

### 🖼️ Image Enhancement

- Adaptive CLAHE contrast enhancement
- Image quality-aware preprocessing
- Gaussian noise reduction
- Image sharpening
- Automatic shadow and illumination correction
- Morphological operations for improved edge detection

---

### 📊 Image Quality Analysis

- Blur detection
- Brightness analysis
- Contrast analysis
- Automatic preprocessing parameter adjustment

---

### 🔍 Optical Character Recognition (OCR)

- OCR using EasyOCR
- English language support
- Extract recognized text from scanned documents
- Modular OCR pipeline for future expansion

---

### 📄 PDF Export

- Export scanned documents as PDF
- Automatic page scaling
- Preserves document aspect ratio
- Clean PDF generation using ReportLab

---

### 🖥️ Desktop GUI

Built with Tkinter.

Features include:

- Open Image
- Live Preview
- Scan Document
- OCR
- Export PDF
- Save Scanned Image
- Status Bar
- User-friendly error dialogs

---

### 🏗️ Architecture Highlights

- Modular backend architecture
- Thin GUI with separated processing logic
- Configurable image processing pipeline
- Reusable scanner components
- Debug visualization for every processing stage

---

# 🛠️ Technologies Used

| Category | Technology |
|-----------|------------|
| Language | Python |
| Computer Vision | OpenCV |
| Numerical Computing | NumPy |
| Image Processing | scikit-image |
| OCR | EasyOCR |
| PDF Generation | ReportLab |
| GUI | Tkinter |
| Utilities | imutils |
| Image Display | Pillow |

---

# 📂 Project Structure

```text
Mobile-Document-Scanner/

├── assets/
├── history/
├── images/
│   ├── input/
│   └── output/
│
├── src/
│   ├── scanner.py
│   ├── document_detector.py
│   ├── transform.py
│   ├── quality.py
│   ├── ocr.py
│   ├── pdf_utils.py
│   └── gui.py
│
├── config.py
├── gui_main.py
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Mobile-Document-Scanner.git
cd Mobile-Document-Scanner
```

Create a virtual environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

Run the desktop application

```bash
python gui_main.py
```

Workflow

1. Open an image.
2. Scan the document.
3. Review the processed output.
4. Run OCR (optional).
5. Export the scan as PDF.
6. Save the scanned image.

---

# 🔄 Processing Pipeline

```
Input Image
      │
      ▼
Grayscale Conversion
      │
      ▼
Image Quality Analysis
      │
      ▼
Adaptive Enhancement
(CLAHE + Blur + Sharpen)
      │
      ▼
Edge Detection
      │
      ▼
Morphological Operations
      │
      ▼
Contour Scoring
      │
      ▼
Perspective Transformation
      │
      ▼
Shadow Removal
      │
      ▼
Scan Mode
(BW / Gray / Color)
      │
      ▼
OCR
      │
      ▼
PDF Export / Save Output
```

---

# 📸 Screenshots

Screenshots and a demo GIF will be added in a future update.

Planned screenshots:

- Home Screen
- Image Loaded
- Document Detection
- Final Scanned Output
- OCR Result
- PDF Export

---

# 🧪 Debug Dashboard

The scanner includes a built-in debugging dashboard for visualizing each stage of the processing pipeline.

Displays

- Original Image
- Enhanced Image
- Shadow Corrected Image
- Edge Detection
- Selected Contour
- Final Scan

This greatly simplifies tuning preprocessing parameters and debugging document detection.

---

# 📈 Project Status

| Module | Status |
|---------|--------|
| Project Structure | ✅ Complete |
| Scanner Pipeline | ✅ Complete |
| Perspective Transform | ✅ Complete |
| Contour Detection | ✅ Complete |
| Adaptive Enhancement | ✅ Complete |
| Shadow Removal | ✅ Complete |
| Image Quality Analysis | ✅ Complete |
| OCR | ✅ Complete |
| PDF Export | ✅ Complete |
| Desktop GUI | ✅ Complete |
| Save Integration | ✅ Complete |
| Error Handling | ✅ Complete |
| Documentation | ✅ Complete |

**Version 1 Status:** ✅ Complete

---

# 🚀 Future Enhancements (Version 2)

The current project focuses on a robust single-document scanning workflow.

Possible future improvements include:

- Searchable PDFs with embedded OCR text
- Batch document scanning
- Multi-page PDF generation
- Webcam / live document scanning
- Drag-and-drop image support
- Manual corner adjustment
- Automatic document cropping suggestions
- AI-assisted document detection
- Image rotation and deskew
- OCR text editing before export
- Cloud storage integration
- Web-based interface using Flask or FastAPI
- Cross-platform desktop packaging

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with

- Computer Vision
- Image Processing
- OpenCV
- OCR Integration
- PDF Generation
- Software Engineering
- Modular Python Architecture
- Object-Oriented Programming
- GUI Development
- Clean Code Principles

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Feel free to fork the repository and submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👩‍💻 Author

**Nisha Khandelwal**

Computer Science Engineering Student

This project was built as a portfolio project to explore practical applications of Computer Vision, OCR, and image processing using Python.

If you found this project useful, consider giving it a ⭐ on GitHub.
