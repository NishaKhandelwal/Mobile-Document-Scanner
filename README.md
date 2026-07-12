# 📄 Mobile Document Scanner

A modular, production-inspired document scanner built with **Python** and **OpenCV**. The application automatically detects documents, corrects perspective distortion, enhances image quality, extracts text using OCR, and exports scanned documents as PDF files.

Designed as a portfolio project to demonstrate practical computer vision techniques, clean software architecture, and modular Python development.

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

### 🖼️ Image Enhancement
- CLAHE contrast enhancement
- Adaptive preprocessing based on image quality
- Gaussian noise reduction
- Image sharpening
- Shadow and illumination correction
- Morphological operations for improved edge detection

### 📊 Image Quality Analysis
- Blur detection
- Brightness analysis
- Contrast analysis
- Automatic preprocessing parameter adjustment

### 🔍 OCR
- Text extraction using EasyOCR
- English language support
- OCR visualization with detected text bounding boxes

### 📄 PDF Export
- Export scanned documents as PDF
- Automatic page scaling while preserving aspect ratio
- Configurable margins

### 🛠️ Developer Features
- Modular project architecture
- Configurable processing pipeline
- Debug dashboard showing every processing stage
- Automatic output generation

---

# 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| Language | Python |
| Computer Vision | OpenCV |
| Numerical Computing | NumPy |
| Image Processing | scikit-image |
| OCR | EasyOCR |
| PDF Generation | ReportLab |
| Utilities | imutils |

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
│   ├── transform.py
│   ├── document_detector.py
│   ├── quality.py
│   ├── ocr.py
│   ├── pdf_utils.py
│   └── gui.py
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Mobile-Document-Scanner.git

cd Mobile-Document-Scanner
```

Create a virtual environment (recommended):

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

Place an image inside

```
images/input/
```

Run

```bash
python main.py
```

The application will

- Detect the document
- Correct perspective
- Enhance the scan
- Extract text
- Export PDF
- Save the scanned output

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
PDF Export
```

---

# 📸 Debug Dashboard

The project includes a built-in debug dashboard that displays every stage of the processing pipeline.

It visualizes:

- Original image
- Enhanced image
- Illumination corrected image
- Edge detection
- Selected contour
- Final scanned output

This makes debugging and tuning preprocessing parameters much easier.

---

# 📄 Current Project Status

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
| GUI | 🚧 In Progress |
| Testing | 🚧 In Progress |
| Documentation | 🚧 In Progress |

---

# 🚀 Roadmap

### Completed

- ✅ Modular architecture
- ✅ Perspective correction
- ✅ Adaptive enhancement
- ✅ Intelligent contour scoring
- ✅ Multiple scan modes
- ✅ OCR integration
- ✅ PDF export
- ✅ Shadow correction

### Planned

- Searchable PDFs
- Desktop GUI
- Batch scanning
- Webcam support
- Unit tests
- GitHub Actions CI

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with

- Computer Vision
- Image Processing
- OpenCV
- OCR Integration
- PDF Generation
- Modular Python Architecture
- Object-Oriented Programming
- Software Engineering Best Practices

---

# 👩‍💻 Author

**Nisha Khandelwal**

If you found this project useful, consider giving it a ⭐ on GitHub.
