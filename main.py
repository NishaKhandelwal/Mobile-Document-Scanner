from src.scanner import DocumentScanner
import config

def main(): 

    scanner = DocumentScanner()

    scanner.load_image("images/input/document.jpg")

    scanner.preprocess()

    scanner.detect_edges()

    if config.DEBUG:
        scanner.show_debug()

    scanner.find_document()

    scanner.scan()

    scanner.save()

    scanner.show()


if __name__ == "__main__":
    main()