from src.scanner import DocumentScanner
import config
import cv2
def main(): 

    scanner = DocumentScanner()

    scanner.load_image("images/input/document.jpg")

    scanner.preprocess()

    scanner.detect_edges()

    scanner.find_document()

    scanner.scan()
    pdf_path = scanner.export_pdf()

    print(f"PDF saved to: {pdf_path}")
    scanner.extract_text()

    scanner.visualize_ocr()

    cv2.imshow(
        "OCR Visualization",
        scanner.ocr_visualization
    )

        

    if config.DEBUG:
        scanner.show_debug()

    scanner.save()

    scanner.show()


if __name__ == "__main__":
    main()