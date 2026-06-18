import cv2
import numpy as np
import imutils
from skimage.filters import threshold_local
from transform import four_point_transform

# Load image
image = cv2.imread("images/receipt.jpg")

if image is None:
    print("Image not found!")
    exit()

ratio = image.shape[0] / 500.0
orig = image.copy()

image = imutils.resize(image, height=500)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Blur image
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Detect edges
edged = cv2.Canny(gray, 75, 200)

print("STEP 1: Edge Detection")

cv2.imshow("Edges", edged)

# Find contours
cnts = cv2.findContours(
    edged.copy(),
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_SIMPLE
)

cnts = imutils.grab_contours(cnts)

cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

screenCnt = None

for c in cnts:

    peri = cv2.arcLength(c, True)

    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    print("Document not detected.")
    exit()

print("STEP 2: Document Found")

cv2.drawContours(image, [screenCnt], -1, (0,255,0), 2)

cv2.imshow("Outline", image)


warped = four_point_transform(
    orig,
    screenCnt.reshape(4,2) * ratio
)

warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

T = threshold_local(
    warped,
    11,
    offset=10,
    method="gaussian"
)

warped = (warped > T).astype("uint8") * 255

print("STEP 3: Scan Complete")

cv2.imshow("Original", orig)
cv2.imshow("Scanned", warped)

cv2.imwrite("output/scanned_document.jpg", warped)

cv2.waitKey(0)
cv2.destroyAllWindows()