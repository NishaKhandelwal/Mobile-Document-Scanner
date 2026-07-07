# config.py

# Resize height for processing
RESIZE_HEIGHT = 500

# Gaussian Blur
BLUR_KERNEL = (5, 5)

# Canny Edge Detection
CANNY_LOW = 75
CANNY_HIGH = 200

# Adaptive Threshold
THRESHOLD_BLOCK_SIZE = 11
THRESHOLD_OFFSET = 10

# Output Directory
OUTPUT_DIR = "images/output"

# Morphology

KERNEL_SIZE = (3, 3)

DILATE_ITERATIONS = 1

ERODE_ITERATIONS = 1


# Debug

DEBUG = True