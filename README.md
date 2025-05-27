# Rock-Paper-Scissors Detection with YOLOv8

This project is a real-time **Rock-Paper-Scissors** game played by two people in front of a webcam. It uses a YOLOv8 model to detect hand gestures (`Rock`, `Paper`, or `Scissors`) and automatically detects the winner when both hands are stable, and includes a cooldown timer to prevent repeated detections too quickly.

---

## Requirements

Install the required packages:

```bash
pip install -r requirements.txt
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

- Press **`x`** to restart the game.
- Press **`q`** to quit the application.

---

## Player Assignment

- **Player 1**: Gesture detected on the **right side** of the screen.
- **Player 2**: Gesture detected on the **left side** of the screen.

---

## Game Display

- When both players show a gesture and hold their hands stable for a short period, the system automatically detects the winner.
- A cooldown timer (5 seconds by default) is shown at the bottom of the screen after each detection to ensure gestures aren't detected repeatedly too quickly.
- Scores are tracked, and the game ends when one player reaches 3 points.
- You can press **`x`** to reset and play again.

---

## Notes

- Only two hands (players) are evaluated per round.
- You can retrain the YOLOv8 model with your own data if needed.

---

## Retraining Your Own Model (Optional)

To retrain the model:

```bash
yolo task=detect mode=train data=data/data.yaml model=yolov8n.pt epochs=30 imgsz=640
```

---

## Dataset

The dataset used for training the model was sourced from [Roboflow](https://roboflow.com).  
You can access the exact dataset used here: [dataset](https://universe.roboflow.com/roboflow-58fyf/rock-paper-scissors-sxsw/dataset/14)

---

Feel free to reach out for questions!

---
