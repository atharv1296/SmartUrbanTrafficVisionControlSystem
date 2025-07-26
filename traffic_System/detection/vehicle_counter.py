import cv2
import numpy as np
from collections import defaultdict, deque
from deep_sort_realtime.deepsort_tracker import DeepSort
from config import VEHICLE_CLASSES, TRAFFIC_ORDER

class VehicleCounter:
    def __init__(self, model):
        self.model = model
        self.trackers = {
            side: DeepSort(max_age=30, n_init=3, nms_max_overlap=1.0)
            for side in TRAFFIC_ORDER
        }
    
    def apply_mask(self, frame, mask):
        """Apply region mask to frame with validation"""
        if mask is not None:
            if mask.shape[:2] != frame.shape[:2]:
                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
            if len(mask.shape) == 2:
                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            return cv2.bitwise_and(frame, mask)
        return frame

    def count_vehicles(self, frame, mask, direction, tracker):
        masked_frame = self.apply_mask(frame, mask)
        conf = 0.5
        results = self.model.predict(masked_frame, imgsz=640, conf=conf, device='cuda', verbose=False)

        detections = []
        vehicle_details = {
            'total': 0,
            'ambulance': 0,
            'types': defaultdict(int),
            'speeds': [],
            'positions': []
        }

        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()

            for box, cls, conf in zip(boxes, classes, confs):
                class_name = self.model.names[int(cls)]
                if class_name in VEHICLE_CLASSES:
                    x1, y1, x2, y2 = map(int, box)
                    detections.append(([x1, y1, x2 - x1, y2 - y1], conf, class_name))
                    vehicle_details['positions'].append((x1, y1, x2, y2))
                    
                    color = (0, 0, 255) if class_name == 'ambulance' else (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{class_name} {conf:.2f}",
                               (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                               0.6, color, 2)

                    vehicle_details['total'] += 1
                    vehicle_details['types'][class_name] += 1
                    if class_name == 'ambulance':
                        vehicle_details['ambulance'] += 1

        tracks = tracker.update_tracks(detections, frame=frame)
        return vehicle_details, frame