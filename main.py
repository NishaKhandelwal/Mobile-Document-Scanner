from src.scanner import DocumentScanner
import config

def main(): 

    scanner = DocumentScanner()

    scanner.load_image("images/input/document.jpg")

    scanner.preprocess()

    scanner.detect_edges()

    scanner.find_document()

    scanner.scan()
    results = scanner.extract_text()
    print(results)
    scanner.visualize_ocr()

    if config.DEBUG:
        scanner.show_debug()

    scanner.save()

    scanner.show()


if __name__ == "__main__":
    main()