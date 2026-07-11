import config
from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class ContourCandidate:

    contour: np.ndarray

    approx: np.ndarray

    score: float


import config
import cv2
import numpy as np
from dataclasses import dataclass


@dataclass
class ContourCandidate:
    contour: np.ndarray
    approx: np.ndarray
    score: float


def score_contour(contour, image_area):

    area = cv2.contourArea(contour)

    print(f"\nArea: {area:.2f}")

    if area < image_area * config.MIN_DOCUMENT_AREA:
        print("Rejected: Area too small")
        return None

    perimeter = cv2.arcLength(contour, True)

    approx = cv2.approxPolyDP(
        contour,
        config.POLYGON_APPROX_EPSILON * perimeter,
        True
    )

    print(f"Corners: {len(approx)}")

    if len(approx) != 4:
        print("Rejected: Not 4 corners")
        return None

    x, y, w, h = cv2.boundingRect(approx)

    aspect_ratio = w / float(h)
    rectangularity = area / (w * h)
    area_score = area / image_area
    ratio_score = 1 - abs(1.4 - aspect_ratio)

    print(f"Aspect Ratio : {aspect_ratio:.2f}")
    print(f"Rectangularity : {rectangularity:.2f}")

    score = (
        area_score * 2 +
        rectangularity +
        ratio_score
    )

    print(f"Score : {score:.2f}")

    return ContourCandidate(
        contour=contour,
        approx=approx,
        score=score
    )