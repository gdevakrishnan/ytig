import time
import cv2
import mediapipe as mp
import pyautogui
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from utils import get_active_window_info, BROWSERS

app = FastAPI()
templates = Jinja2Templates(directory="templates")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)

CENTER_X = 0.5
CENTER_Y = 0.5

def get_hand_distance_from_center(hand_landmarks):
    wrist = hand_landmarks.landmark[0]
    dx = wrist.x - CENTER_X
    dy = wrist.y - CENTER_Y
    return (dx**2 + dy**2) ** 0.5

def is_index_finger_up(h):
    return h.landmark[8].y < h.landmark[6].y

def is_middle_finger_up(h):
    return h.landmark[12].y < h.landmark[10].y

def are_all_fingers_up(h):
    fingers = [8, 12, 16, 20]
    bases = [6, 10, 14, 18]
    for tip, base in zip(fingers, bases):
        if h.landmark[tip].y > h.landmark[base].y:
            return False
    return True

cap = cv2.VideoCapture(0)

# -------- SMART TIMER STATE --------
TIMER_RUNNING = False
REMAINING_TIME = None
LAST_CHECK = None
DELAY = 1.5
last_trigger_time = 0
# ----------------------------------

def generate_frames():
    global REMAINING_TIME, TIMER_RUNNING, LAST_CHECK, last_trigger_time

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()

        # -------- SMART TIMER LOGIC (RUNS ONLY ON IG/YT) --------
        if TIMER_RUNNING and REMAINING_TIME is not None:
            window_title, process_name = get_active_window_info()
            is_instagram = window_title and "instagram" in window_title.lower()
            is_youtube = window_title and "youtube" in window_title.lower()

            if process_name in BROWSERS and (is_instagram or is_youtube):
                elapsed = now - LAST_CHECK
                REMAINING_TIME -= elapsed

            LAST_CHECK = now

            if REMAINING_TIME <= 0:
                print("Time is up! Closing window...")
                pyautogui.hotkey("ctrl", "w")
                TIMER_RUNNING = False
        # ---------------------------------------------

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        window_title, process_name = get_active_window_info()
        is_instagram = window_title and "instagram" in window_title.lower()
        is_youtube = window_title and "youtube" in window_title.lower()

        label = "Move your hand"

        if process_name in BROWSERS and (is_instagram or is_youtube):
            if result.multi_hand_landmarks:
                main_hand = min(
                    result.multi_hand_landmarks,
                    key=get_hand_distance_from_center
                )

                mp_draw.draw_landmarks(frame, main_hand, mp_hands.HAND_CONNECTIONS)

                index_up = is_index_finger_up(main_hand)
                middle_up = is_middle_finger_up(main_hand)
                all_up = are_all_fingers_up(main_hand)

                if now - last_trigger_time > DELAY:

                    if all_up:
                        label = "CLOSE WINDOW"
                        pyautogui.hotkey("ctrl", "w")

                    elif index_up and not middle_up:
                        label = "SCROLL DOWN"
                        pyautogui.press("down")

                    elif middle_up and not index_up:
                        label = "SCROLL UP"
                        pyautogui.press("up")

                    last_trigger_time = now

        else:
            label = "Open Instagram or YouTube"

        cv2.putText(frame, label, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (138, 43, 226), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/start")
def start_timer(minutes: float = Form(...)):
    global REMAINING_TIME, TIMER_RUNNING, LAST_CHECK

    REMAINING_TIME = minutes * 60
    TIMER_RUNNING = True
    LAST_CHECK = time.time()

    return {"status": "started", "seconds": REMAINING_TIME}


@app.get("/time_left")
def time_left():
    global REMAINING_TIME
    return {"seconds": max(0, REMAINING_TIME or 0)}


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
