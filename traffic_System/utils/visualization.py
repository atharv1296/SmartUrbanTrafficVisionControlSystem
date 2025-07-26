import cv2
import math
import time

def draw_vehicle_info(frame, vehicle_data, is_current_green, signal_remaining, current_mode, next_side, emergency_start_time=None):
    """
    Draw traffic light and vehicle info overlays on a video frame.
    """
    status = "GREEN" if is_current_green else "RED"
    color = (0, 255, 0) if is_current_green else (0, 0, 255)

    if is_current_green and current_mode == "NORMAL":
        countdown = math.ceil(signal_remaining)
        status_text = f"GREEN: {countdown}s | Next: {next_side}"
    else:
        status_text = f"{status} | Next: {next_side}"

    cv2.putText(frame, status_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, f"Vehicles: {vehicle_data.get('total', 0)} (Ambulances: {vehicle_data.get('ambulance', 0)})",
                (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    text_y_pos = 150
    if signal_remaining <= 5 and current_mode == "NORMAL":
        countdown = math.ceil(signal_remaining)
        cv2.putText(frame, f"Changing in: {countdown}s",
                    (50, text_y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 255), 2)
        text_y_pos += 30

    if current_mode == "NORMAL":
        if is_current_green and signal_remaining <= 5:
            countdown = math.ceil(signal_remaining)
            cv2.putText(frame, f"Next: {next_side} in {countdown}s",
                        (50, text_y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
            text_y_pos += 30
        elif not is_current_green:
            approx_wait = signal_remaining
            cv2.putText(frame, f"Approx wait: {approx_wait:.0f}s",
                        (50, text_y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
            text_y_pos += 30

    if current_mode == "EMERGENCY_PENDING" and emergency_start_time is not None:
        remaining = 5 - (time.time() - emergency_start_time)
        if remaining > 0:
            cv2.putText(frame, f"EMERGENCY OVERRIDE IN {math.ceil(remaining)}s",
                        (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    return frame
