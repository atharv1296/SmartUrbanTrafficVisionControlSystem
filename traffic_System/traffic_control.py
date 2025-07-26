import time
from collections import defaultdict
from config import TRAFFIC_ORDER, DAY_MIN_GREEN, DAY_MAX_GREEN

class TrafficController:
    def __init__(self):
        self.current_mode = "NORMAL"
        self.current_green_index = 0
        self.previous_green_index = -1
        self.signal_remaining = 0
        self.emergency_side = None
        self.emergency_start_time = 0
        self.vehicle_counts = {side: {'total': 0, 'ambulance': 0} for side in TRAFFIC_ORDER}
        self.last_update_time = time.time()
        self.last_log_time = time.time()

    def calculate_green_time(self, vehicle_count):
        """Dynamic green time calculation with safety limits"""
        base = vehicle_count * 2
        limits = (DAY_MIN_GREEN, DAY_MAX_GREEN)
        return max(limits[0], min(limits[1], base))

    def update_traffic_state(self, elapsed, vehicle_data):
        current_time = time.time()
        
        # Emergency handling
        if self.current_mode == "NORMAL" and any(data['ambulance'] > 0 for data in vehicle_data.values()):
            self.current_mode = "EMERGENCY_PENDING"
            self.emergency_side = next(side for side, data in vehicle_data.items() if data['ambulance'] > 0)
            self.emergency_start_time = current_time
            print(f"\nEMERGENCY: Ambulance detected in {self.emergency_side}")
            
        elif self.current_mode == "EMERGENCY_PENDING":
            if current_time - self.emergency_start_time >= 5:
                self.current_mode = "EMERGENCY_ACTIVE"
                self.current_green_index = TRAFFIC_ORDER.index(self.emergency_side)
                self.signal_remaining = self.calculate_green_time(
                    self.vehicle_counts[self.emergency_side]['total']
                )
                print(f"Switching to {self.emergency_side} for {self.signal_remaining} seconds")

        elif self.current_mode == "EMERGENCY_ACTIVE":
            self.signal_remaining -= elapsed
            if self.signal_remaining <= 0:
                self.current_mode = "NORMAL"
                self.current_green_index = (TRAFFIC_ORDER.index(self.emergency_side) + 1) % 4
                next_side = TRAFFIC_ORDER[self.current_green_index]
                self.signal_remaining = self.calculate_green_time(
                    self.vehicle_counts[next_side]['total']
                )
                print("\nResuming normal operation")
                self.emergency_side = None

        # Normal operation
        if self.current_mode == "NORMAL":
            self.signal_remaining -= elapsed
            if self.signal_remaining <= 0:
                self.current_green_index = (self.current_green_index + 1) % 4
                next_side = TRAFFIC_ORDER[self.current_green_index]
                self.signal_remaining = self.calculate_green_time(
                    self.vehicle_counts[next_side]['total']
                )
                print(f"\nNormal rotation to {next_side} for {self.signal_remaining} seconds")

        return self.current_green_index, self.signal_remaining, self.current_mode