"""
scanner.py

Document Scanner using OpenCV.

Pipeline
--------
1. Load Image
2. Preprocess Image
3. Detect Edges
4. Detect Document
5. Perspective Transform
6. Enhance Scan
7. Save Output
"""

import os
from src.ocr import OCRProcessor
import cv2
from datetime import datetime
import imutils
import numpy as np
from skimage.filters import threshold_local
from src.quality import (
    ImageQuality,
    enhancement_parameters
)
from src.document_detector import score_contour
import config
from src.transform import four_point_transform
from src.document_detector import score_contour


class DocumentScanner:
    """
    Main document scanner class.
    """

    def __init__(self):

        # Original image
        self.original = None

        # Working image (resized)
        self.image = None

        # Processing stages
        self.gray = None
        self.enhanced = None
        self.corrected=None
        self.edged = None
        self.contour_image = None

        # Final result
        self.scanned = None

        # Document contour
        self.document_contour = None

        # Resize ratio
        self.ratio = 1.0
        self.quality = None
        # OCR processor
        self.ocr = OCRProcessor()

        # Latest OCR result
        self.ocr_result = None
        self.ocr_visualization = None

    # --------------------------------------------------

    def load_image(self, image_path):
        """
        Load an image from disk.
        """

        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Image not found:\n{image_path}"
            )

        image = cv2.imread(image_path)

        if image is None:
            raise RuntimeError(
                "OpenCV could not read the image."
            )

        self.original = image.copy()

        self.ratio = image.shape[0] / config.RESIZE_HEIGHT

        self.image = imutils.resize(
            image,
            height=config.RESIZE_HEIGHT
        )

    # --------------------------------------------------

    def preprocess(self):
            """
            Enhance the image before document detection.
            """

            if self.image is None:
                raise RuntimeError("Load an image first.")

            # Convert to grayscale
            self.gray = cv2.cvtColor(
                self.image,
                cv2.COLOR_BGR2GRAY
            )

            quality = ImageQuality(self.gray)

            report = quality.get_report()

            params = enhancement_parameters(report)

            clahe = cv2.createCLAHE(

                clipLimit=params["clip_limit"],

                tileGridSize=config.CLAHE_GRID_SIZE
            )

            self.enhanced = clahe.apply(self.gray)

            # Reduce noise
            self.enhanced = cv2.GaussianBlur(
                self.enhanced,
                config.GAUSSIAN_KERNEL,
                0
            )

            # Sharpen image
            blurred = cv2.GaussianBlur(
                self.enhanced,
                (0, 0),
                3
            )

            amount = params["sharpen"]

            self.enhanced = cv2.addWeighted(
                self.enhanced,
                amount,
                blurred,
                -(amount - 1),
                0
            )

            # Analyze image quality
            self.quality = ImageQuality(
                self.enhanced
            )
    # --------------------------------------------------

    def detect_edges(self):
        """
        Detect document edges using adaptive Canny.
        """

        if self.enhanced is None:
            raise RuntimeError("Run preprocess() first.")

        # Automatic Canny Thresholds

        median = np.median(self.enhanced)

        lower = int(max(0, 0.66 * median))
        upper = int(min(255, 1.33 * median))

        self.edged = cv2.Canny(
            self.enhanced,
            lower,
            upper
        )

        # Morphological Closing
        # Helps connect broken document borders

        kernel = np.ones((7, 7), np.uint8)

        self.edged = cv2.dilate(
            self.edged,
            kernel,
            iterations=2
        )

        self.edged = cv2.erode(
            self.edged,
            kernel,
            iterations=2
        )

        cv2.imwrite("images/output/debug_gray.jpg", self.enhanced)
        cv2.imwrite("images/output/debug_edges.jpg", self.edged)
            # --------------------------------------------------
        cv2.imwrite("images/output/debug_edges.jpg", self.edged)
        cv2.imwrite("images/output/debug_gray.jpg", self.enhanced)

    def find_document(self):
            """
            Detect the document using contour scoring.
            """

            contours = cv2.findContours(
                self.edged.copy(),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            contours = imutils.grab_contours(contours)

            print(f"\nFound {len(contours)} contours")

            # Sort largest first
            contours = sorted(
                contours,
                key=cv2.contourArea,
                reverse=True
            )

            image_area = self.image.shape[0] * self.image.shape[1]

            best_candidate = None

            debug = self.image.copy()

            # Evaluate every contour
            for i, contour in enumerate(contours):

                area = cv2.contourArea(contour)

                print(f"Contour {i+1}: area = {int(area)}")

                candidate = score_contour(
                    contour,
                    image_area
                )

                color = (0, 0, 255)

                if candidate is not None:

                    color = (0, 255, 0)

                    if (
                        best_candidate is None or
                        candidate.score > best_candidate.score
                    ):
                        best_candidate = candidate

                cv2.drawContours(
                    debug,
                    [contour],
                    -1,
                    color,
                    2
                )

            self.contour_image = debug

            cv2.imwrite(
                "images/output/debug_contours.jpg",
                debug
            )

            if best_candidate is None:
                raise RuntimeError(
                    "Unable to detect document."
                )

            self.document_contour = best_candidate.approx

            print("\nSelected Document")

            print(
                f"Score : {best_candidate.score:.2f}"
            )

            print(
                f"Area  : {int(cv2.contourArea(best_candidate.contour))}"
            )

            cv2.drawContours(
                self.contour_image,
                [self.document_contour],
                -1,
                (255, 0, 0),
                4
            )

    def scan(self):
        """
        Apply perspective transform and create
        a scanner-like black & white image.
        """

        warped = four_point_transform(
            self.original,
            self.document_contour.reshape(4, 2) * self.ratio
        )
        if len(warped.shape) == 3:
            gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        else:
            gray = warped.copy()

       # Convert to grayscale for quality analysis
        if len(warped.shape) == 3:
            gray = cv2.cvtColor(
                warped,
                cv2.COLOR_BGR2GRAY
            )
        else:
            gray = warped.copy()

        quality = ImageQuality(gray)

        # Apply shadow removal only when enabled and the document is dark.
        if (
            config.ENABLE_SHADOW_REMOVAL and
            quality.brightness < config.LOW_BRIGHTNESS
        ):
            self.corrected = self.remove_shadows(warped)
        else:
            self.corrected = gray

        mode = config.SCAN_MODE.lower()

        if mode == "color":

            self.scanned = warped

        elif mode == "gray":

            self.scanned = self.corrected

        else:

            threshold = threshold_local(
                self.corrected,
                config.THRESHOLD_BLOCK_SIZE,
                offset=config.THRESHOLD_OFFSET,
                method="gaussian"
            )

            self.scanned = (
                self.corrected > threshold
            ).astype("uint8") * 255
        print(f"Scan Mode: {config.SCAN_MODE.upper()}")   
        # --------------------------------------------------
    def extract_text(self):
        """
        Extract text from the scanned document.

        Returns
        -------
        list
            EasyOCR results.
        """

        if self.scanned is None:
            raise RuntimeError(
                "Run scan() before OCR."
            )

        self.ocr_result = self.ocr.extract_text(
            self.scanned
        )

        return self.ocr_result
    def visualize_ocr(self):
        """
        Draw OCR detections on the scanned image.
        """

        if self.scanned is None:
            raise RuntimeError(
                "Run scan() before OCR visualization."
            )

        if not self.ocr_result:
            self.ocr_visualization = self.scanned.copy()
            return self.ocr_visualization

        if len(self.scanned.shape) == 2:
            image = cv2.cvtColor(
                self.scanned,
                cv2.COLOR_GRAY2BGR
            )
        else:
            image = self.scanned.copy()

        for result in self.ocr_result:

            bbox = result["bbox"]
            text = result["text"]
            confidence = result["confidence"]

            points = np.array(
                bbox,
                dtype=np.int32
            )

            cv2.polylines(
                image,
                [points],
                True,
                (0, 255, 0),
                2
            )

            x = int(points[0][0])
            y = int(points[0][1]) - 10

            cv2.putText(
                image,
                f"{text} ({confidence:.2f})",
                (x, max(y, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2
            )

        self.ocr_visualization = image

        return image
    def remove_shadows(self, image):
        """
        Correct uneven illumination in a scanned document.

        A large Gaussian blur estimates the background illumination.
        The original image is then normalized against this background
        using OpenCV's divide operation.

        Parameters
        ----------
        image : numpy.ndarray
            Perspective-corrected document image.

        Returns
        -------
        numpy.ndarray
            Grayscale image with more uniform illumination.
        """

        # Convert to grayscale if required
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Estimate illumination background
        background = cv2.GaussianBlur(
            gray,
            config.BACKGROUND_BLUR_KERNEL,
            0
        )

        # Normalize illumination
        self.corrected = cv2.divide(
            gray,
            background,
            scale=255
        )

        # Stretch intensity range
        self.corrected = cv2.normalize(
            self.corrected,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        return self.corrected
    def save(self, filename=None):
        """
        Save scanned document.
        """

        if self.scanned is None:
            raise RuntimeError("Nothing to save.")

        os.makedirs(
            config.OUTPUT_DIR,
            exist_ok=True
        )

        if filename is None:

            filename = (
                datetime.now().strftime(
                    "scan_%Y%m%d_%H%M%S.jpg"
                )
            )

        output_path = os.path.join(
            config.OUTPUT_DIR,
            filename
        )

        cv2.imwrite(
            output_path,
            self.scanned
        )

        print(f"\n✓ Saved successfully")
        print(output_path)
        # --------------------------------------------------

    def show(self):

        cv2.imshow(
            "Original",
            self.original
        )

        cv2.imshow(
            "Scanned",
            self.scanned
        )

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # --------------------------------------------------

    def show_debug(self):
        """
        Display the complete document scanner processing pipeline.
        """

        if self.image is None:
            return

        original = self.image.copy()

        enhanced = cv2.cvtColor(
            self.enhanced,
            cv2.COLOR_GRAY2BGR
        )

        edges = cv2.cvtColor(
            self.edged,
            cv2.COLOR_GRAY2BGR
        )

        if self.corrected is not None:
            corrected = cv2.cvtColor(
                self.corrected,
                cv2.COLOR_GRAY2BGR
            )
        else:
            corrected = np.zeros_like(original)

        if self.contour_image is not None:
            contour = self.contour_image.copy()
        else:
            contour = original.copy()

        if self.scanned is not None:

            if len(self.scanned.shape) == 2:
                scanned = cv2.cvtColor(
                    self.scanned,
                    cv2.COLOR_GRAY2BGR
                )
            else:
                scanned = self.scanned.copy()

        else:
            scanned = np.zeros_like(original)

        h, w = original.shape[:2]

        images = [
            original,
            enhanced,
            corrected,
            edges,
            contour,
            scanned
        ]

        images = [
            cv2.resize(img, (w, h))
            for img in images
        ]

        labels = [
            "Original",
            "Enhanced",
            "Corrected",
            "Edges",
            "Contour",
            "Final Scan"
        ]

        for img, text in zip(images, labels):

            cv2.putText(
                img,
                text,
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        top = np.hstack(images[:3])
        bottom = np.hstack(images[3:])

        dashboard = np.vstack((top, bottom))

        if self.quality:

            report = self.quality.get_report()

            cv2.putText(
                dashboard,
                f"Blur: {report['blur']}",
                (20, dashboard.shape[0] - 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.putText(
                dashboard,
                f"Brightness: {report['brightness']}",
                (20, dashboard.shape[0] - 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.putText(
                dashboard,
                f"Contrast: {report['contrast']}",
                (20, dashboard.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.putText(
                dashboard,
                "Adaptive Enhancement",
                (dashboard.shape[1] - 260, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

        cv2.imshow(
            "Document Scanner Pipeline",
            dashboard
        )

        cv2.waitKey(0)
        cv2.destroyAllWindows()