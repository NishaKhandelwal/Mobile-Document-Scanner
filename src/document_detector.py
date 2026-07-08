"""
document_detector.py

Scores every contour and returns the most likely document.

Instead of taking the first contour with four points,
we evaluate multiple geometric properties.
"""

import cv2
import numpy as np


class DocumentCandidate:

    def __init__(self, contour):

        self.contour = contour

        self.area = cv2.contourArea(contour)

        self.score = 0

        self.approx = None


def score_contour(contour, image_area):

    candidate = DocumentCandidate(contour)

    candidate.area = cv2.contourArea(contour)

    if candidate.area < image_area * 0.02:
        return None

    perimeter = cv2.arcLength(contour, True)

    approx = cv2.approxPolyDP(
        contour,
        0.02 * perimeter,
        True
    )

    candidate.approx = approx

    score = 0

    # -------------------------
    # Area
    # -------------------------

    area_ratio = candidate.area / image_area

    score += min(area_ratio * 30, 30)

    # -------------------------
    # Number of corners
    # -------------------------

    if len(approx) == 4:
        score += 20

    elif len(approx) == 5:
        score += 12

    elif len(approx) == 6:
        score += 6

    # -------------------------
    # Convex
    # -------------------------

    if cv2.isContourConvex(approx):
        score += 10

    # -------------------------
    # Bounding rectangle
    # -------------------------

    x, y, w, h = cv2.boundingRect(approx)

    ratio = w / float(h)

    if 0.5 <= ratio <= 2.2:
        score += 10

    # -------------------------
    # Solidity
    # -------------------------

    hull = cv2.convexHull(contour)

    hull_area = cv2.contourArea(hull)

    if hull_area > 0:

        solidity = candidate.area / hull_area

        score += solidity * 10

    # -------------------------
    # Extent
    # -------------------------

    rect_area = w * h

    if rect_area > 0:

        extent = candidate.area / rect_area

        score += extent * 10

    # -------------------------
    # Rectangle fill
    # -------------------------

    rectangle = np.array([
        [[x, y]],
        [[x + w, y]],
        [[x + w, y + h]],
        [[x, y + h]]
    ])

    overlap = cv2.matchShapes(
        approx,
        rectangle,
        cv2.CONTOURS_MATCH_I1,
        0
    )

    score += max(0, 10 - overlap * 20)

    candidate.score = round(score, 2)

    return candidate