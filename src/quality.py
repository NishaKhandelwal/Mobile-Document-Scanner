"""
quality.py

Image Quality Analysis Utilities
--------------------------------
Evaluates image quality before scanning.

Metrics:
1. Blur
2. Brightness
3. Contrast
"""

import cv2
import numpy as np


class ImageQuality:

    def __init__(self, gray):

        self.gray = gray

        self.blur = self.calculate_blur()

        self.brightness = self.calculate_brightness()

        self.contrast = self.calculate_contrast()

    def calculate_blur(self):
        """
        Variance of Laplacian

        Higher value = Sharper image
        """

        return cv2.Laplacian(
            self.gray,
            cv2.CV_64F
        ).var()

    def calculate_brightness(self):

        return float(np.mean(self.gray))

    def calculate_contrast(self):

        return float(np.std(self.gray))

    def get_report(self):

        return {

            "blur": round(self.blur, 2),

            "brightness": round(self.brightness, 2),

            "contrast": round(self.contrast, 2)

        }
    def enhancement_parameters(report):
        """
        Decide preprocessing parameters
        based on image quality.
        """

        clip_limit = 2.5
        sharpen = 1.5

        if report["brightness"] < 80:
            clip_limit = 4.0

        elif report["brightness"] > 190:
            clip_limit = 2.0

        if report["blur"] < 120:
            sharpen = 2.0

        if report["contrast"] < 30:
            clip_limit += 0.5

        return {

            "clip_limit": clip_limit,

            "sharpen": sharpen

        }