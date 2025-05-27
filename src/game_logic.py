# src/game_logic.py
# Implements logic for playing Rock-Paper-Scissors and scoring

def determine_winner(gesture1, gesture2):
    if gesture1 == gesture2:
        return "Draw"
    if (gesture1 == "Rock" and gesture2 == "Scissors") or \
       (gesture1 == "Scissors" and gesture2 == "Paper") or \
       (gesture1 == "Paper" and gesture2 == "Rock"):
        return "Player 1"
    return "Player 2"


def update_score(score, winner):
    if winner == "Player 1":
        score[0] += 1
    elif winner == "Player 2":
        score[1] += 1
    return score
