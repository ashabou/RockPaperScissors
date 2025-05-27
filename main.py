import cv2
import time
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
    print("Hands must remain stable to trigger winner detection")
    print("Press 'c' to clear winner display")
    print("Press 'q' to quit")

    score = [0, 0]
    last_winner = ""
    game_over = False

    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    stable_count = 0
    THRESHOLD = 10000  # motion score threshold
    STABLE_FRAMES = 10  # how many consecutive stable frames trigger detection
    COOLDOWN_SECONDS = 5
    last_detection_time = 0  # timestamp of last winner detection

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        movement_score = cv2.countNonZero(thresh)

        prev_gray = gray.copy()

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

        # Sort by x-position
        detections = sorted(detections, key=lambda d: d["center_x"])

        player1_gesture = None
        player2_gesture = None

        if len(detections) >= 2:
            player2_gesture = detections[0]["label"]
            player1_gesture = detections[1]["label"]

        display_frame = frame.copy()
        for i, detection in enumerate(detections):
            x1, y1, x2, y2 = detection["box"]
            color = (0, 255, 0)
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)

            player = "Player 2" if i == 0 else "Player 1"
            cv2.putText(display_frame, player, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        score_text = f"Player 1: {score[0]}     Player 2: {score[1]}"
        cv2.putText(display_frame, score_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        if last_winner:
            cv2.putText(display_frame, f"Winner: {last_winner}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        current_time = time.time()
        # Show cooldown timer if still in cooldown phase
        time_since_last_detection = current_time - last_detection_time
        if time_since_last_detection < COOLDOWN_SECONDS:
            cooldown_remaining = COOLDOWN_SECONDS - int(time_since_last_detection)
            cooldown_text = f"Please wait... {cooldown_remaining}s"
            text_size = cv2.getTextSize(cooldown_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = (display_frame.shape[1] - text_size[0]) // 2  # center horizontally
            text_y = display_frame.shape[0] - 20  # 20 px from bottom
            cv2.putText(display_frame, cooldown_text, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        cv2.imshow("Rock Paper Scissors - Live", display_frame)

        # Stability check
        if movement_score < THRESHOLD and not game_over and (current_time - last_detection_time) >= COOLDOWN_SECONDS:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= STABLE_FRAMES:
            print("Hands stable - detecting winner")
            if player1_gesture and player2_gesture:
                last_winner = determine_winner(player1_gesture, player2_gesture)
                score = update_score(score, last_winner)
                last_detection_time = time.time()  # start cooldown
                if score[0] == 3 or score[1] == 3:
                    last_winner = f"{last_winner} - Congratulations! \n Press 'x' to play again"
                    game_over = True
                else:
                    last_winner = f"Player 1: {player1_gesture}, Player 2: {player2_gesture} --- Winner: {last_winner}"
            else:
                last_winner = "Not enough gestures"
                print("Error: Less than 2 gestures detected")

            stable_count = 0  # reset after detection

        key = cv2.waitKey(1) & 0xFF

        if key == ord('x') and game_over:
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