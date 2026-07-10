import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)

screen_w, screen_h = pyautogui.size()

TARGET_FPS = 60
FRAME_TIME = 1.0 / TARGET_FPS

# landmark ids from the mediapipe hand model
THUMB_TIP = 4
INDEX_TIP = 8
INDEX_PIP = 6
INDEX_MCP = 5
MIDDLE_TIP = 12
MIDDLE_PIP = 10
RING_TIP = 16
RING_PIP = 14
PINKY_TIP = 20
PINKY_PIP = 18

FRAME_MARGIN = 0.15  # how much of the edge of the cam frame to ignore

# smoothing - higher alpha = snappier, lower = smoother but laggier
ALPHA_MIN = 0.18
ALPHA_MAX = 0.75
SPEED_LOW = 4
SPEED_HIGH = 60
DEAD_ZONE = 1.5

CLICK_COOLDOWN = 0.6

smooth_x, smooth_y = None, None
filt_x, filt_y = None, None
fist_down = False
last_click = 0
last_time = 0
gesture = "None"

RAW_ALPHA = 0.6  # smooths the raw landmark a bit before we even map it to screen coords

fps_hist = []
FPS_WINDOW = 30


def dist(a, b):
    return math.hypot(b.x - a.x, b.y - a.y)


def finger_up(lm, tip, pip):
    return lm[tip].y < lm[pip].y


def thumb_folded(lm):
    return dist(lm[THUMB_TIP], lm[INDEX_MCP]) < 0.08


def is_fist(lm):
    return (
        not finger_up(lm, INDEX_TIP, INDEX_PIP)
        and not finger_up(lm, MIDDLE_TIP, MIDDLE_PIP)
        and not finger_up(lm, RING_TIP, RING_PIP)
        and not finger_up(lm, PINKY_TIP, PINKY_PIP)
        and thumb_folded(lm)
    )


def get_gesture(lm):
    if is_fist(lm):
        return "Fist"

    idx_up = finger_up(lm, INDEX_TIP, INDEX_PIP)
    mid_up = finger_up(lm, MIDDLE_TIP, MIDDLE_PIP)
    ring_up = finger_up(lm, RING_TIP, RING_PIP)
    pinky_up = finger_up(lm, PINKY_TIP, PINKY_PIP)

    if idx_up and not mid_up and not ring_up and not pinky_up:
        return "Index Only (Move)"

    return "Other"


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def smooth_cursor(tx, ty):
    global smooth_x, smooth_y

    if smooth_x is None:
        smooth_x, smooth_y = tx, ty
        return smooth_x, smooth_y

    dx = tx - smooth_x
    dy = ty - smooth_y
    d = math.hypot(dx, dy)

    if d < DEAD_ZONE:
        return smooth_x, smooth_y

    # scale alpha based on how fast the hand is moving - slow = smooth it
    # out more, fast = just track it so it doesn't feel laggy
    t = clamp((d - SPEED_LOW) / (SPEED_HIGH - SPEED_LOW), 0.0, 1.0)
    alpha = ALPHA_MIN + t * (ALPHA_MAX - ALPHA_MIN)

    smooth_x += alpha * dx
    smooth_y += alpha * dy
    return smooth_x, smooth_y


def move_cursor(lm):
    global filt_x, filt_y

    raw_x, raw_y = lm[INDEX_TIP].x, lm[INDEX_TIP].y

    if filt_x is None:
        filt_x, filt_y = raw_x, raw_y
    else:
        filt_x += RAW_ALPHA * (raw_x - filt_x)
        filt_y += RAW_ALPHA * (raw_y - filt_y)

    # remap so the edges of the "active zone" hit the screen edges,
    # not the literal edges of the webcam frame
    span = 1 - 2 * FRAME_MARGIN
    nx = clamp((filt_x - FRAME_MARGIN) / span, 0.0, 1.0)
    ny = clamp((filt_y - FRAME_MARGIN) / span, 0.0, 1.0)

    tx = nx * screen_w
    ty = ny * screen_h

    cx, cy = smooth_cursor(tx, ty)
    pyautogui.moveTo(cx, cy, duration=0)


def left_click():
    pyautogui.mouseDown(button="left")
    pyautogui.mouseUp(button="left")


while True:
    t0 = time.time()

    ok, frame = cap.read()
    if not ok:
        break

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    h, w = frame.shape[:2]

    now = time.time()
    if last_time:
        fps_hist.append(now - last_time)
        if len(fps_hist) > FPS_WINDOW:
            fps_hist.pop(0)
    last_time = now
    fps = (1 / (sum(fps_hist) / len(fps_hist))) if fps_hist else 0

    status = "Idle"

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand, mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style(),
            )

            lm = hand.landmark
            gesture = get_gesture(lm)
            fist_now = is_fist(lm)

            # only click on the moment the fist closes, not every frame
            # while it's held down
            if fist_now and not fist_down:
                if now - last_click > CLICK_COOLDOWN:
                    left_click()
                    last_click = now
                    status = "Left clicked"
                fist_down = True
            elif not fist_now:
                fist_down = False

            if gesture == "Index Only (Move)":
                move_cursor(lm)
                if status == "Idle":
                    status = "Moving"

            ix, iy = int(lm[INDEX_TIP].x * w), int(lm[INDEX_TIP].y * h)
            cv2.circle(frame, (ix, iy), 10, (0, 255, 0), -1)

    cv2.rectangle(frame, (0, 0), (340, 130), (30, 30, 30), -1)
    cv2.putText(frame, f"Gesture: {gesture}", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"Mouse: {status}", (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (60, 220, 60), 2)
    cv2.putText(frame, f"FPS: {int(fps)}", (15, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    cv2.putText(frame, "Press 'q' to quit", (15, 118), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

    cv2.imshow("AI Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # cap the loop at ~60fps so it's not just spinning as fast as possible
    dt = time.time() - t0
    if dt < FRAME_TIME:
        time.sleep(FRAME_TIME - dt)

cap.release()
cv2.destroyAllWindows()