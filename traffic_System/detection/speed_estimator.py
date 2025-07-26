import cv2
import numpy as np
from collections import defaultdict, deque
import math

class SpeedEstimator:
    def __init__(self, perspective_points, real_width, section_length):
        self.real_width = real_width
        self.section_length = section_length
        self.matrix = self.get_perspective_matrix(perspective_points)
        self.track_history = defaultdict(lambda: deque(maxlen=10))
        self.pixels_per_meter = None
        self.calibrate_scaling()

    def get_perspective_matrix(self, points):
        src = np.float32(points)
        dst = np.float32([[0, 0], [1000, 0], [1000, 1000], [0, 1000]])
        return cv2.getPerspectiveTransform(src, dst)

    def pixel_to_meters(self, point):
        src = np.array([[[point[0], point[1]]]], dtype=np.float32)
        dst = cv2.perspectiveTransform(src, self.matrix)
        return dst[0][0]

    def calibrate_scaling(self):
        start = np.array([[[0, 0]]], dtype=np.float32)
        end = np.array([[[0, self.section_length]]], dtype=np.float32)

        src_start = cv2.perspectiveTransform(start, self.matrix)
        src_end = cv2.perspectiveTransform(end, self.matrix)

        pixel_length = np.linalg.norm(src_end - src_start)
        self.pixels_per_meter = pixel_length / self.section_length
        print(f"Calibrated scale: {self.pixels_per_meter:.2f} pixels/meter")

    def validate_calibration(self, frame):
        test_points = [(100, 100), (200, 100), (200, 200), (100, 200)]
        for pt in test_points:
            cv2.circle(frame, pt, 5, (0, 255, 0), -1)
            real_pt = self.pixel_to_meters(pt)
            cv2.putText(frame, f"{real_pt[0]:.1f}m,{real_pt[1]:.1f}m",
                        (pt[0] + 10, pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        return frame