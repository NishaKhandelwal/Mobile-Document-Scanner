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

    area_score = candidate.area / image_area

    perimeter = cv2.arcLength(contour, True)

    approx = cv2.approxPolyDP(
        contour,
        0.03 * perimeter,
        True
    )

    candidate.approx = approx

    # Ignore tiny contours

    if candidate.area < image_area * 0.02:
        return None

    score = 0

    # Area

    score += min(area_score * 60, 60)

    # Four corners

    if len(approx) == 4:
        score += 25

    # Convex

    if cv2.isContourConvex(approx):
        score += 10

    # Rectangle quality

    x, y, w, h = cv2.boundingRect(approx)

    ratio = w / float(h)

    if 0.4 < ratio < 2.5:
        score += 5

    candidate.score = score

    return candidate