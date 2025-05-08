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

def count_fingers(thresh, hand):
    hull = cv2.convexHull(hand)
    extT = tuple(hull[hull[:, :, 1].argmin()][0])
    extB = tuple(hull[hull[:, :, 1].argmax()][0])
    extL = tuple(hull[hull[:, :, 0].argmin()][0])
    extR = tuple(hull[hull[:, :, 0].argmax()][0])
    cX = (extL[0] + extR[0]) // 2
    cY = (extT[1] + extB[1]) // 2

    def dist(p1, p2):
        return np.hypot(p1[0] - p2[0], p1[1] - p2[1])

    dists = np.array([dist((cX, cY), pt) for pt in (extT, extB, extL, extR)])
    radius = int(0.8 * dists.max())

    mask = np.zeros(thresh.shape[:2], dtype="uint8")
    cv2.circle(mask, (cX, cY), radius, 255, 1)
    circular_roi = cv2.bitwise_and(thresh, thresh, mask=mask)

    cnts, _ = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print(f"[DEBUG] Found {len(cnts)} contours in circular ROI")

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    if len(cnts) > 0:
        cnts = cnts[1:]  # ignore wrist

    for c in cnts:
        cv2.drawContours(circular_roi, [c], -1, (255, 255, 255), 2)

    return len(cnts), circular_roi

def map_gesture(n):
    if n in (0, 1): return "Rock"
    if n in (1, 2): return "Scissors"
    if n >= 5: return "Paper"
    return "Unknown"