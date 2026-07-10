from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class ContourCandidate:

    contour: np.ndarray

    approx: np.ndarray

    score: float


def score_contour(contour, image_area):
    """
    Score how likely a contour is to be a document.

    Higher score = better document candidate.
    """

    area = cv2.contourArea(contour)

    # Ignore very small contours
    if area < image_area * 0.10:
        return None

    perimeter = cv2.arcLength(
        contour,
        True
    )

    approx = cv2.approxPolyDP(
        contour,
        0.02 * perimeter,
        True
    )

    # Documents should have four corners
    if len(approx) != 4:
        return None

    x, y, w, h = cv2.boundingRect(approx)

    aspect_ratio = w / float(h)

    rectangularity = area / (w * h)

    area_score = area / image_area

    ratio_score = 1 - abs(1.4 - aspect_ratio)

    score = (
        area_score * 2
        + rectangularity
        + ratio_score
    )

    return ContourCandidate(
        contour=contour,
        approx=approx,
        score=score
    )