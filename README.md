# 📄 Mobile Document Scanner

A Python-based Mobile Document Scanner that uses **OpenCV** and **Computer Vision** techniques to automatically detect, crop, and enhance documents from images. The application converts photos of documents into clean, high-quality scanned copies, similar to popular mobile scanning apps.

---

## 🚀 Features

- 📷 Detects document boundaries automatically
- ✂️ Crops documents using contour detection
- 🔄 Corrects perspective distortion
- 🖤 Converts documents into clean black-and-white scans
- 📄 Produces scanner-like digital copies
- ⚡ Fast and efficient image processing

---

## 🛠️ Technologies Used

- Python
- OpenCV
- NumPy
- scikit-image
- imutils

---

## 📂 Project Structure

```
Mobile-Document-Scanner/
│
├── images/              # Sample input images
├── output/              # Scanned output images
├── scan.py              # Main application
├── transform.py         # Perspective transformation utilities
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/mobile-document-scanner.git
cd mobile-document-scanner
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the scanner by providing an image path.

```bash
python scan.py --image images/document.jpg
```

The processed scanned image will be displayed and can be saved for later use.

---

## 🔍 How It Works

The document scanner follows a simple image processing pipeline:

1. Load the input image.
2. Convert the image to grayscale.
3. Apply Gaussian Blur to reduce noise.
4. Detect edges using the Canny Edge Detector.
5. Find contours and identify the document boundary.
6. Perform a four-point perspective transform.
7. Apply adaptive thresholding for a clean scanned effect.

---

## 📸 Example Workflow

**Input Image**
- Photograph of a document captured from a mobile phone.

⬇️

**Processing**
- Edge Detection
- Contour Detection
- Perspective Correction
- Adaptive Thresholding

⬇️

**Output**
- High-quality scanned document.

---

## 💡 Future Enhancements

- Optical Character Recognition (OCR)
- PDF export
- Batch document scanning
- Automatic document cropping
- Mobile application integration
- Cloud storage support

---

## 🎯 Learning Outcomes

This project helped in understanding:

- Image Processing fundamentals
- Edge Detection
- Contour Detection
- Perspective Transformation
- Adaptive Thresholding
- OpenCV image manipulation
- Computer Vision workflows

---

## 👩‍💻 Author

**Nisha Khandelwal**

If you found this project helpful, consider giving it a ⭐ on GitHub!
