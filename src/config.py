# src/config.py
# Configuration file to store paths and constant values used across modules
MODEL_PATH = "runs/detect/train/weights/best.pt"
CLASS_NAMES = ['Paper','Rock', 'Scissors']
CONFIDENCE_THRESHOLD = 0.5
CAMERA_INDEX = 0  # Default camera index, change if using external webcam
