import random
import numpy as np
from game_logic import calibrate_background, get_user_move, show_result, TOP, BOTTOM, RIGHT, LEFT
from display import show_live_background, show_countdown
from assets import load_assets, overlay_alpha, Icons, AI_POS
import cv2

from gesture import run_avg

def main():
    bg_img, icons = load_assets()
    cam = cv2.VideoCapture(0)
    scores = [0, 0]

    print("[INFO] Calibrating background on ROI...")
    calibrate_background(cam)
    text = "Press 's' to Start the Game"

    show_live_background(cam, bg_img, scores,text)

    while True:
        show_countdown(cam, scores, bg_img)

        user, gray_blur, diff, thr, circular, roi_color, frame, seg = get_user_move(cam)
        ai_move = icons.get_random_move()
        result = icons.decide(user, ai_move)

        # Update score BEFORE displaying
        if result == "You Win!":
            scores[1] += 1
        elif result == "You Lose!":
            scores[0] += 1

        # Copy the base background
        disp = bg_img.copy()

        # Draw AI icon
        icons.draw_ai(disp, ai_move)

        # Show result on the screen
        show_result(user, ai_move, result, scores, disp)
        fg, mask = (icons.ai_rock, icons.mr) if ai_move == "Rock" else \
            (icons.ai_paper, icons.mp) if ai_move == "Paper" else \
                (icons.ai_scis, icons.ms)

        # Add ROI and overlay into display
        resized = cv2.resize(frame, (398, 420))  # Fit full frame to BG area
        scale_x = 398 / frame.shape[1]
        scale_y = 420 / frame.shape[0]
        scaled_top = int(TOP * scale_y)
        scaled_bottom = int(BOTTOM * scale_y)
        scaled_right = int(RIGHT * scale_x)
        scaled_left = int(LEFT * scale_x)
        cv2.rectangle(resized, (scaled_right, scaled_top), (scaled_left, scaled_bottom), (0, 255, 0), 2)
        disp[234:654, 795:1193] = resized
        overlay_alpha(disp, fg, mask, AI_POS[0], AI_POS[1])
        cv2.putText(disp, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 6)
        cv2.putText(disp, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(disp, user, (850, 300), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        cv2.putText(disp, ai_move, (150, 300), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        (text_width, text_height), _ = cv2.getTextSize(result, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)
        x_center = 640 - text_width // 2
        cv2.putText(disp, result, (x_center, 425), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 2)
        # Display scores
        cv2.putText(disp, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 6)
        cv2.putText(disp, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(disp, "Press 'E' to Exit | Press 'R' to Recalibrate Background",
                    (410, 695), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)

        # Show image processing stages
        gray_bgr = cv2.cvtColor(gray_blur, cv2.COLOR_GRAY2BGR)
        thr_vis = cv2.cvtColor(thr, cv2.COLOR_GRAY2BGR) if seg else gray_bgr.copy()
        circ_bgr = cv2.cvtColor(circular, cv2.COLOR_GRAY2BGR)
        diff_bgr = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
        stack = np.hstack([
            cv2.resize(roi_color, (200, 200)),
            cv2.resize(gray_bgr, (200, 200)),
            cv2.resize(diff_bgr, (200, 200)),
            cv2.resize(thr_vis, (200, 200)),
            cv2.resize(circ_bgr, (200, 200))
        ])
        cv2.imshow("Image Processing Stages", stack)
        cv2.imshow("BG", disp)

        key = cv2.waitKey(0) & 0xFF
        if key == ord('e') or key == ord('E'):
            break
        elif key == ord('r') or key == ord('R'):
            print("[INFO] Recalibrating background...")
            for _ in range(30):
                ret, frame = cam.read()
                frame = cv2.flip(frame, 1)
                roi = frame[TOP:BOTTOM, RIGHT:LEFT]
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (7, 7), 0)
                run_avg(gray, 0.5)

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
