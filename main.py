import cv2
import mediapipe as mp
import pyautogui
import time

from utils import get_active_window_info, BROWSERS

# ----------- TIMER INPUT -----------
minutes = float(input("Enter timer in minutes: "))
END_TIME = time.time() + (minutes * 60)
print(f"Timer started for {minutes} minutes...\n")
# ----------------------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)

cap = cv2.VideoCapture(0)

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
    bases   = [6, 10, 14, 18]

    for tip, base in zip(fingers, bases):
        if h.landmark[tip].y > h.landmark[base].y:
            return False
    return True

last_trigger_time = 0
DELAY = 1.5
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if time.time() >= END_TIME:
        print("\nTime is up! Closing window automatically...")
        pyautogui.hotkey("ctrl", "w")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    current_time = time.time()

    window_title, process_name = get_active_window_info()

    is_instagram = window_title and "instagram" in window_title.lower()
    is_youtube = window_title and "youtube" in window_title.lower()

    if process_name in BROWSERS and (is_instagram or is_youtube):
        if result.multi_hand_landmarks:
            main_hand = min(
                result.multi_hand_landmarks,
                key=get_hand_distance_from_center
            )

            hand_landmarks = main_hand
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_up = is_index_finger_up(hand_landmarks)
            middle_up = is_middle_finger_up(hand_landmarks)
            all_up = are_all_fingers_up(hand_landmarks)

            if current_time - last_trigger_time > DELAY:
                label = ""

                if all_up:
                    print("FIVE FINGERS → CLOSE WINDOW")
                    pyautogui.hotkey("ctrl", "w")
                    label = "CLOSING WINDOW"
                    break

                elif index_up and not middle_up:
                    count += 1
                    print("Index UP → count =", count)
                    pyautogui.press("down")
                    label = "INDEX (scroll down)"

                elif middle_up and not index_up:
                    count -= 1
                    print("Middle UP → count =", count)
                    pyautogui.press("up")
                    label = "MIDDLE (scroll up)"

                if label:
                    cv2.putText(frame, label, (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    last_trigger_time = current_time
    else:
        cv2.putText(frame, "Instagram or YouTube not active", (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
