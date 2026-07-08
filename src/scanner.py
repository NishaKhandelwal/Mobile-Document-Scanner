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
import cv2
from datetime import datetime
import imutils
import numpy as np
from skimage.filters import threshold_local

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
        self.edged = None
        self.contour_image = None

        # Final result
        self.scanned = None

        # Document contour
        self.document_contour = None

        # Resize ratio
        self.ratio = 1.0

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
        Image enhancement before edge detection.
        """

        if self.image is None:
            raise RuntimeError("Load an image first.")

        # Convert to grayscale

        self.gray = cv2.cvtColor(
            self.image,
            cv2.COLOR_BGR2GRAY
        )

        # CLAHE (better than equalizeHist)

        clahe = cv2.createCLAHE(
            clipLimit=config.CLAHE_CLIP_LIMIT,
            tileGridSize=config.CLAHE_GRID_SIZE
        )

        self.enhanced = clahe.apply(self.gray)

        # Noise reduction

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

        self.enhanced = cv2.addWeighted(
            self.enhanced,
            1.5,
            blurred,
            -0.5,
            0
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

        contours = cv2.findContours(
            self.edged.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        contours = imutils.grab_contours(contours)

        print(f"\nFound {len(contours)} contours")

        image_area = self.image.shape[0] * self.image.shape[1]

        debug = self.image.copy()

        contours = sorted(
            contours,
            key=cv2.contourArea,
            reverse=True
        )

        best_candidate = None

        for i, contour in enumerate(contours):

            area = cv2.contourArea(contour)

            candidate = score_contour(
                contour,
                image_area
            )

            if candidate is None:
                continue

            print(
                f"Contour {i+1} | "
                f"Area = {int(area)} | "
                f"Score = {candidate.score:.2f}"
            )

            color = (0, 255, 0)

            if candidate.score > 70:
                color = (0, 255, 255)

            if candidate.score > 85:
                color = (0, 0, 255)

            cv2.drawContours(
                debug,
                [candidate.contour],
                -1,
                color,
                2
            )

            x, y, w, h = cv2.boundingRect(candidate.contour)

            cv2.putText(
                debug,
                f"{candidate.score:.1f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

            if (
                best_candidate is None or
                candidate.score > best_candidate.score
            ):
                best_candidate = candidate

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

        print(
            f"\nSelected contour "
            f"(Score = {best_candidate.score:.2f})"
        )
        # --------------------------------------------------

    def scan(self):
        """
        Apply perspective transform and create
        a scanner-like black & white image.
        """

        if self.document_contour is None:
            raise RuntimeError("Document contour not found.")

        self.scanned = four_point_transform(
            self.original,
            self.document_contour.reshape(4, 2) * self.ratio
        )

        self.scanned = cv2.cvtColor(
            self.scanned,
            cv2.COLOR_BGR2GRAY
        )

        threshold = threshold_local(
            self.scanned,
            config.THRESHOLD_BLOCK_SIZE,
            offset=config.THRESHOLD_OFFSET,
            method="gaussian"
        )

        self.scanned = (
            self.scanned > threshold
        ).astype("uint8") * 255
        # --------------------------------------------------

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

        if self.scanned is None:
            raise RuntimeError("Nothing to display.")

        cv2.imshow("Scanned Document", self.scanned)

        cv2.waitKey(0)

        cv2.destroyAllWindows()
        # --------------------------------------------------

    def show_debug(self):

        if self.image is None:
            return

        original = self.image.copy()

        gray = cv2.cvtColor(
            self.gray,
            cv2.COLOR_GRAY2BGR
        )

        enhanced = cv2.cvtColor(
            self.enhanced,
            cv2.COLOR_GRAY2BGR
        )

        edges = cv2.cvtColor(
            self.edged,
            cv2.COLOR_GRAY2BGR
        )

        if self.contour_image is not None:
            contour = self.contour_image.copy()
        else:
            contour = original.copy()

        if self.scanned is not None:
            scanned = cv2.cvtColor(
                self.scanned,
                cv2.COLOR_GRAY2BGR
            )
        else:
            scanned = np.zeros_like(original)

        h, w = original.shape[:2]

        images = [
            original,
            gray,
            enhanced,
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
            "Gray",
            "Enhanced",
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

        cv2.imshow(
            "Document Scanner Pipeline",
            dashboard
        )

        cv2.waitKey(0)

        cv2.destroyAllWindows()