import cv2
import time
import os
from database.db_setup import setup_database, create_user
from models.yolo_model import load_yolo_model
from detection.vehicle_counter import VehicleCounter
from detection.speed_estimator import SpeedEstimator
from traffic_control import TrafficController
from config import CAMERA_SOURCES, TRAFFIC_ORDER, MASK_FOLDER, SPEED_CALIBRATION
from utils.visualization import draw_vehicle_info


def initialize_cameras():
    caps = {}
    for side, src in CAMERA_SOURCES.items():
        cap = cv2.VideoCapture(src)
        if not cap.isOpened():
            print(f"Failed to open {side} camera")
            exit(1)

        caps[side] = {
            'cap': cap,
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        }
        print(f"{side} camera initialized: {caps[side]['width']}x{caps[side]['height']}")
    return caps

def load_masks():
    masks = {}
    for side in TRAFFIC_ORDER:
        mask_file = f"mask_{side.lower()}.png"
        full_path = os.path.join(MASK_FOLDER, mask_file)

        if os.path.exists(full_path):
            mask = cv2.imread(full_path, cv2.IMREAD_COLOR)
            if mask is not None:
                masks[side] = mask
                print(f"Loaded {side} specific mask from {full_path}")
            else:
                print(f"Failed to load {side} mask (file exists but read error)")
                masks[side] = None
        else:
            default_mask_path = os.path.join(MASK_FOLDER, "mask.png")
            if os.path.exists(default_mask_path):
                mask = cv2.imread(default_mask_path, cv2.IMREAD_COLOR)
                masks[side] = mask if mask is not None else None
                print(f"Using default mask for {side}")
            else:
                print(f"No mask found for {side}")
                masks[side] = None

        if masks[side] is not None and len(masks[side].shape) == 2:
            masks[side] = cv2.cvtColor(masks[side], cv2.COLOR_GRAY2BGR)
    return masks

def main():
    # Initialize database
    setup_database()
    create_user("officer1", "securepass", "officer")

    # Load YOLO model
    model = load_yolo_model('../Yolo-Weights/yolov12l.pt')

    # Initialize components
    caps = initialize_cameras()
    masks = load_masks()
    vehicle_counter = VehicleCounter(model)
    traffic_controller = TrafficController()

    # Initialize speed estimators
    speed_estimators = {
        side: SpeedEstimator(
            SPEED_CALIBRATION[side]["points"],
            SPEED_CALIBRATION[side]["real_width"],
            SPEED_CALIBRATION[side]["section_length"]
        )
        for side in TRAFFIC_ORDER
    }

    try:
        last_update_time = time.time()
        last_log_time = time.time()

        while True:
            current_time = time.time()
            elapsed = current_time - last_update_time
            last_update_time = current_time

            # Process all camera feeds
            vehicle_data = {}
            for side in TRAFFIC_ORDER:
                cam_info = caps[side]
                ret, frame = cam_info['cap'].read()
                if not ret:
                    cam_info['cap'].set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                # Detect and track vehicles
                data, processed_frame = vehicle_counter.count_vehicles(
                    frame,
                    masks[side],
                    side,
                    vehicle_counter.trackers[side]
                )
                vehicle_data[side] = data
                caps[side]['last_vehicle_data'] = data

                # Update speed estimation
                frame = speed_estimators[side].validate_calibration(frame)

                # Display
                is_current_green = (side == TRAFFIC_ORDER[traffic_controller.current_green_index])
                next_side = TRAFFIC_ORDER[(traffic_controller.current_green_index + 1) % 4]
                frame = draw_vehicle_info(
                    frame,
                    data,
                    is_current_green,
                    traffic_controller.signal_remaining,
                    traffic_controller.current_mode,
                    next_side
                )

                # Show frame
                cv2.imshow(side, frame)

            # Update traffic control
            traffic_controller.update_traffic_state(elapsed, vehicle_data)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Cleanup
        for side in TRAFFIC_ORDER:
            if caps[side]['cap'].isOpened():
                caps[side]['cap'].release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()