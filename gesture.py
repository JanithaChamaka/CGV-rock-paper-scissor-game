import cv2
import numpy as np

bg = None

def run_avg(image, aW=0.5):
    global bg
    if bg is None:
        bg = image.copy().astype("float")
    else:
        cv2.accumulateWeighted(image, bg, aW)

def segment(image, threshold=15):
    global bg
    diff = cv2.absdiff(bg.astype("uint8"), image)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return None
    # Filter by area size
    hand_candidates = [c for c in cnts if 5000 < cv2.contourArea(c) < 30000]
    if not hand_candidates:
        return None
    hand = max(cnts, key=cv2.contourArea)
    return diff, thresh, hand