# Configuration constants
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'user123',
    'database': 'traffic_db'
}

# Camera sources
CAMERA_SOURCES = {
    "North": '../resources/videos/tra2.mp4',
    "South": '../resources/videos/tra2.mp4',
    "East": '../resources/videos/tra2.mp4',
    "West": '../resources/videos/tra2.mp4'
}

# Timing parameters
DAY_MIN_GREEN = 15
DAY_MAX_GREEN = 120

# Vehicle classes to detect
VEHICLE_CLASSES = {'car', 'motorcycle', 'bus', 'truck', 'ambulance'}

# Traffic order
TRAFFIC_ORDER = ["North", "East", "South", "West"]

# Mask folder path
MASK_FOLDER = "../resources"

# Speed calibration
SPEED_CALIBRATION = {
    "North": {
        "points": [(300, 200), (900, 200), (1100, 700), (100, 700)],
        "real_width": 3.7,
        "section_length": 50
    },
    "South": {
        "points": [(400, 300), (800, 300), (1000, 800), (200, 800)],
        "real_width": 3.7,
        "section_length": 50
    },
    "East": {
        "points": [(500, 150), (800, 150), (1100, 500), (400, 500)],
        "real_width": 3.7,
        "section_length": 50
    },
    "West": {
        "points": [(400, 180), (750, 180), (950, 550), (300, 550)],
        "real_width": 3.7,
        "section_length": 50
    }
}