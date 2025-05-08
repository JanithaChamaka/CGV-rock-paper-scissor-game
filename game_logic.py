import cv2
import numpy as np
import random
from gesture import run_avg, segment, count_fingers, map_gesture

TOP, RIGHT, BOTTOM, LEFT = 10, 350, 225, 590

def calibrate_background(cam):
    for _ in range(30):
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        roi = frame[TOP:BOTTOM, RIGHT:LEFT]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        run_avg(gray, 0.5)

def get_user_move(cam):
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    roi = frame[TOP:BOTTOM, RIGHT:LEFT]
    roi_color = roi.copy()
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (7, 7), 0)

    seg = segment(gray_blur)
    if seg:
        diff, thr, hand = seg
        fingers, circular = count_fingers(thr, hand)
        user = map_gesture(fingers)
        cv2.drawContours(roi, [hand], -1, (0, 255, 0), 2)
    else:
        user = "Unknown"
        diff = thr = circular = np.zeros_like(gray_blur)

    return user, gray_blur, diff, thr, circular, roi_color, frame,seg


def show_result(user, ai, result, scores, bg_img):
    print(f"[RESULT] You: {user} | AI: {ai} => {result}")
    if result == "You Win!":
        scores[0] += 1
    elif result == "You Lose!":
        scores[1] += 1
