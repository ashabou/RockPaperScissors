# Rock-Paper-Scissors Detection with YOLOv8

This project is a real-time **Rock-Paper-Scissors** game played by two people in front of a webcam. It uses a YOLOv8 model to detect hand gestures (`Rock`, `Paper`, or `Scissors`) and automatically determines the winner of each round.

---

## Project Structure

```
project/
│
├── main.py                     # Main script to run the app
├── src/
│   ├── capture.py              # Webcam frame capture logic
│   ├── config.py               # Config constants and model paths
│   ├── detect.py               # Hand gesture detection using YOLOv8
│   ├── game_logic.py           # Game rules and score updating
│   ├── utils.py                # Drawing and display helpers
│
├── runs/detect/train/weights/best.pt   # Trained YOLOv8 model
├── data/data.yaml              # Dataset config used during training
└── README.md                   # This file
```

---

## Requirements

Install the required packages:

```bash
pip install opencv-python ultralytics
```

Make sure you have a working webcam connected.

---

## YOLOv8 Model

The model detects these classes:

- Rock
- Paper
- Scissors

Model weights path (update in `src/config.py` if different):

```
runs/detect/train/weights/best.pt
```

---

## How to Run

From the project root folder, run:

```bash
python main.py
```

**Controls:**

- Press **`x`** to capture the current frame and detect gestures.
- Press **`c`** to clear the winner display.
- Press **`q`** to quit the application.

---

## Player Assignment

- **Player 1**: Gesture detected on the **right side** of the screen.
- **Player 2**: Gesture detected on the **left side** of the screen.

---

## Game Display

- Bounding boxes are displayed live around detected hands.
- Each box is labeled with the player number and detected gesture.
- Player scores are shown at the top and update after each capture.
- The winner of the current round is displayed below the scores.

---

## Notes

- Ensure good lighting and clear hand visibility.
- Only two hands (players) are evaluated per round.
- You can retrain the YOLOv8 model with your own data if needed.

---

## Retraining Your Own Model (Optional)

To retrain the model:

```bash
yolo task=detect mode=train data=data/data.yaml model=yolov8n.pt epochs=30 imgsz=640
```

---

## Author

Developed by **Safouane** and **Aziz**.

Feel free to reach out for questions!

---
