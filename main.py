import cv2
from ultralytics import YOLO
from src.game_logic import determine_winner, update_score
from src.config import MODEL_PATH, CLASS_NAMES, CONFIDENCE_THRESHOLD, CAMERA_INDEX

model = YOLO(MODEL_PATH)
def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    if not cap.isOpened():
        print("Error: Cannot access camera")
        return

    print("Live detection running...")
    print("Press 'x' to capture and detect winner")
    print("Press 'c' to clear winner display")
    print("Press 'q' to quit")

    score = [0, 0]  # Player 1, Player 2
    last_winner = ""
    game_over = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Run detection
        results = model(frame, verbose=False)[0]
        detections = []
        for result in results.boxes:
            conf = result.conf.item()
            if conf >= CONFIDENCE_THRESHOLD:
                cls_id = int(result.cls.item())
                label = CLASS_NAMES[cls_id] if cls_id < len(CLASS_NAMES) else "Unknown"
                x1, y1, x2, y2 = map(int, result.xyxy[0].tolist())
                center_x = (x1 + x2) // 2
                detections.append({
                    "label": label,
                    "box": (x1, y1, x2, y2),
                    "center_x": center_x
                })

        # Sort detections left to right
        detections = sorted(detections, key=lambda d: d["center_x"])

        # Assign players based on position (left = Player 2, right = Player 1)
        player1_gesture = None
        player2_gesture = None

        if len(detections) >= 2:
            player2_gesture = detections[0]["label"]  # Leftmost
            player1_gesture = detections[1]["label"]  # Rightmost

        # Draw detections
        display_frame = frame.copy()
        for i, detection in enumerate(detections):
            x1, y1, x2, y2 = detection["box"]
            color = (0, 255, 0)
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)

            # Label based on horizontal position
            player = "Player 2" if i == 0 else "Player 1"
            gesture = detection["label"]
            text = f"{player}"
            cv2.putText(display_frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Display score at the top
        score_text = f"Player 1: {score[0]}     Player 2: {score[1]}"
        cv2.putText(display_frame, score_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Display last winner if available
        if last_winner:
            cv2.putText(display_frame, f"Winner: {last_winner}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Rock Paper Scissors - Live", display_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('x') and not game_over:
            if player1_gesture and player2_gesture:
                last_winner = determine_winner(player1_gesture, player2_gesture)
                score = update_score(score, last_winner)
                if score[0]== 3 or score[1] == 3:
                    last_winner = f"{last_winner} - Congratulations! \n Press x to play again"
                    game_over = True
                if score[0]< 3 and score[1] < 3:
                    last_winner = f"Player 1: {player1_gesture}, Player 2: {player2_gesture} --- Winner: {last_winner}"
            else:
                last_winner = "Not enough gestures"
                print("Error: Less than 2 gestures detected")
        elif key == ord('x') and game_over:
            score = [0, 0]
            last_winner = ""
            game_over = False
        elif key == ord('c'):
            last_winner = ""

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
