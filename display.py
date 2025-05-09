import cv2

TOP, RIGHT, BOTTOM, LEFT = 10, 350, 225, 590
PLAY_Y1, PLAY_X1 = 234, 795

def show_live_background(cam, bg_img, scores,text):
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        resized = cv2.resize(frame, (398, 420))  # Fit full frame to BG area
        disp = bg_img.copy()
        scale_x = 398 / frame.shape[1]
        scale_y = 420 / frame.shape[0]
        scaled_top = int(TOP * scale_y)
        scaled_bottom = int(BOTTOM * scale_y)
        scaled_right = int(RIGHT * scale_x)
        scaled_left = int(LEFT * scale_x)
        cv2.rectangle(resized, (scaled_right, scaled_top), (scaled_left, scaled_bottom), (0, 255, 0), 2)
        disp[234:654, 795:1193] = resized
        cv2.putText(disp, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 6)
        cv2.putText(disp, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(disp, text, (410, 695), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow("BG", disp)
        key = cv2.waitKey(1)
        if key == ord('s') or key == ord('S'):
            break
        elif key == ord('q') or key == ord('Q'):
            cam.release()
            cv2.destroyAllWindows()
            exit()

def show_countdown(cam, scores, bg_img):
    for i in (3, 2, 1):
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        resized = cv2.resize(frame, (398, 420))  # Fit full frame to BG area
        disp = bg_img.copy()
        scale_x = 398 / frame.shape[1]
        scale_y = 420 / frame.shape[0]
        scaled_top = int(TOP * scale_y)
        scaled_bottom = int(BOTTOM * scale_y)
        scaled_right = int(RIGHT * scale_x)
        scaled_left = int(LEFT * scale_x)
        cv2.rectangle(resized, (scaled_right, scaled_top), (scaled_left, scaled_bottom), (0, 255, 0), 2)
        disp[234:654, 795:1193] = resized
        cv2.putText(disp, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 6)
        cv2.putText(disp, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(disp, str(i), (600, 445), cv2.FONT_HERSHEY_COMPLEX, 4, (0, 0, 0), 5)
        cv2.imshow("BG", disp)
        cv2.waitKey(1000)

    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    resized = cv2.resize(frame, (398, 420))  # Fit full frame to BG area
    disp = bg_img.copy()
    scale_x = 398 / frame.shape[1]
    scale_y = 420 / frame.shape[0]
    scaled_top = int(TOP * scale_y)
    scaled_bottom = int(BOTTOM * scale_y)
    scaled_right = int(RIGHT * scale_x)
    scaled_left = int(LEFT * scale_x)
    cv2.rectangle(resized, (scaled_right, scaled_top), (scaled_left, scaled_bottom), (0, 255, 0), 2)
    disp[234:654, 795:1193] = resized
    cv2.putText(disp, "Shoot!", (540, 425), cv2.FONT_HERSHEY_COMPLEX, 1.8, (0, 0, 0), 3)
    cv2.imshow("BG", disp)
    cv2.waitKey(1000)