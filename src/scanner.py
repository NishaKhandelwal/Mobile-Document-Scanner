"""
scanner.py

Contains the complete document scanning pipeline.

Responsibilities
----------------
1. Load image
2. Preprocess image
3. Detect document
4. Correct perspective
5. Apply scanner filters
6. Save scanned output
"""
import cv2
import imutils
import numpy as np
from skimage.filters import threshold_local

from src.transform import four_point_transform
import config


class DocumentScanner:

    def __init__(self):
        self.image = None
        self.original = None
        self.gray = None
        self.edged = None
        self.document_contour = None
        self.scanned = None
        self.ratio = 1
def load_image(self, image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    self.original = image.copy()

    self.ratio = image.shape[0] / config.RESIZE_HEIGHT

    self.image = imutils.resize(
        image,
        height=config.RESIZE_HEIGHT
    )
def preprocess(self):

    self.gray = cv2.cvtColor(
        self.image,
        cv2.COLOR_BGR2GRAY
    )

    # Improve contrast

    self.gray = cv2.equalizeHist(self.gray)

    self.gray = cv2.GaussianBlur(
        self.gray,
        config.GAUSSIAN_KERNEL,
        0
    )
def detect_edges(self):

    self.edged = cv2.Canny(

        self.gray,

        config.CANNY_LOW,

        config.CANNY_HIGH

    )

    kernel = np.ones(

        config.KERNEL_SIZE,

        np.uint8

    )

    self.edged = cv2.dilate(

        self.edged,

        kernel,

        iterations=config.DILATE_ITERATIONS

    )

    self.edged = cv2.erode(

        self.edged,

        kernel,

        iterations=config.ERODE_ITERATIONS

    )
def find_document(self):

    contours = cv2.findContours(
        self.edged.copy(),
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = imutils.grab_contours(contours)

    contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True
    )[:5]

    for contour in contours:

        perimeter = cv2.arcLength(contour, True)

        approx = cv2.approxPolyDP(
            contour,
            0.02 * perimeter,
            True
        )

        if len(approx) == 4:

            self.document_contour = approx

            return

    raise RuntimeError(
    "Unable to detect document. Try another image."
)
def scan(self):

    self.scanned = four_point_transform(

        self.original,

        self.document_contour.reshape(4, 2) * self.ratio

    )

    self.scanned = cv2.cvtColor(
        self.scanned,
        cv2.COLOR_BGR2GRAY
    )

    T = threshold_local(

        self.scanned,

        config.THRESHOLD_BLOCK_SIZE,

        offset=config.THRESHOLD_OFFSET,

        method="gaussian"

    )

    self.scanned = (

        self.scanned > T

    ).astype("uint8") * 255
def save(self, filename="scanned_document.jpg"):

    output_path = f"{config.OUTPUT_DIR}/{filename}"

    cv2.imwrite(
        output_path,
        self.scanned
    )

    print(f"Saved to {output_path}")
def show(self):

    cv2.imshow("Original", self.original)

    cv2.imshow("Scanned", self.scanned)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
def show_debug(self):

    cv2.imshow("Original", self.image)

    cv2.imshow("Gray", self.gray)

    cv2.imshow("Edges", self.edged)

    cv2.waitKey(0)

    cv2.destroyAllWindows()