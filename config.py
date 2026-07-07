"""
config.py

Global configuration file for the Mobile Document Scanner.
All configurable parameters are kept here.
"""

# ==========================================================
# IMAGE RESIZING
# ==========================================================

# Images are resized to this height before processing.
# Larger values improve accuracy but increase processing time.
RESIZE_HEIGHT = 500


# ==========================================================
# PREPROCESSING
# ==========================================================

# Gaussian Blur kernel size
# Must be odd numbers.
GAUSSIAN_KERNEL = (5, 5)

# CLAHE (Contrast Limited Adaptive Histogram Equalization)
CLAHE_CLIP_LIMIT = 2.0
CLAHE_GRID_SIZE = (8, 8)


# ==========================================================
# EDGE DETECTION
# ==========================================================

# Adaptive Canny computes thresholds automatically,
# but these act as fallback values if needed.
CANNY_LOW = 75
CANNY_HIGH = 200


# ==========================================================
# MORPHOLOGICAL OPERATIONS
# ==========================================================

# Kernel used for Morphological Closing
MORPH_KERNEL = (5, 5)


# ==========================================================
# DOCUMENT DETECTION
# ==========================================================

# Ignore contours smaller than 20% of the image area.
MIN_DOCUMENT_AREA = 0.03

# Approximation accuracy for contour simplification.
POLYGON_APPROX_EPSILON = 0.03


# ==========================================================
# SCAN ENHANCEMENT
# ==========================================================

# Adaptive Threshold parameters
THRESHOLD_BLOCK_SIZE = 11
THRESHOLD_OFFSET = 10


# ==========================================================
# OUTPUT SETTINGS
# ==========================================================

OUTPUT_DIR = "images/output"

DEFAULT_OUTPUT_PREFIX = "scan"


# ==========================================================
# DEBUG
# ==========================================================

# Show processing pipeline dashboard.
DEBUG = True


# ==========================================================
# SUPPORTED IMAGE TYPES
# ==========================================================

SUPPORTED_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
)