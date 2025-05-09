import cv2
import random


BG_PATH     = "resources/BG.png"
AI_ROCK     = "resources/1.png"
AI_PAPER    = "resources/2.png"
AI_SCISSORS = "resources/3.png"
AI_POS = (149, 310)

def load_icon(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    return img[:,:,:3], img[:,:,3]

def overlay_alpha(bg, fg, mask, x, y):
    h,w = fg.shape[:2]
    roi = bg[y:y+h, x:x+w]
    inv = cv2.bitwise_not(mask)
    bg_part = cv2.bitwise_and(roi, roi, mask=inv)
    fg_part = cv2.bitwise_and(fg, fg, mask=mask)
    bg[y:y+h, x:x+w] = cv2.add(bg_part, fg_part)

class Icons:
    def __init__(self):
        self.ai_rock, self.mr = load_icon(AI_ROCK)
        self.ai_paper, self.mp = load_icon(AI_PAPER)
        self.ai_scis, self.ms = load_icon(AI_SCISSORS)

    def get_random_move(self):
        return random.choice(["Rock", "Paper", "Scissors"])

    def draw_ai(self, bg, move):
        fg, mask = {
            "Rock": (self.ai_rock, self.mr),
            "Paper": (self.ai_paper, self.mp),
            "Scissors": (self.ai_scis, self.ms)
        }[move]
        overlay_alpha(bg, fg, mask, *AI_POS)

    @staticmethod
    def decide(user, ai):
        if user == "Unknown":
            return "Invalid"
        if user == ai:
            return "Tie"
        wins = (user == "Rock" and ai == "Scissors") or \
               (user == "Scissors" and ai == "Paper") or \
               (user == "Paper" and ai == "Rock")
        return "You Win!" if wins else "You Lose!"

def load_assets():
    bg_img = cv2.imread(BG_PATH)
    icons = Icons()
    return bg_img, icons
