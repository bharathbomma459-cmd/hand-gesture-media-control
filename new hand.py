import cv2
import mediapipe as mp
import pyautogui
import pygetwindow as gw
import time
import numpy as np
from collections import deque

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

# cooldown
last_action_time = 0
cooldown = 2   # seconds

def can_trigger_action():
    global last_action_time
    now = time.time()
    if now - last_action_time > cooldown:
        last_action_time = now
        return True
    return False

# smoothing
smooth_queue = deque(maxlen=5)
def smooth_landmarks(landmarks):
    """landmarks: (21,3) np.array"""
    smooth_queue.append(landmarks)
    return np.mean(smooth_queue, axis=0)

def focus_youtube():
    windows = gw.getWindowsWithTitle("YouTube")
    if windows:
        win = windows[0]
        win.activate()
        time.sleep(0.3)

# stable detection
stable_count = 0
last_gesture = None
def is_stable(gesture, required=6):
    global stable_count, last_gesture
    if gesture == last_gesture:
        stable_count += 1
    else:
        stable_count = 0
        last_gesture = gesture
    return stable_count >= required

# helper: finger up test (for index/middle/ring/pinky)
def finger_is_up(landmarks, tip_idx, pip_idx):
    # landmarks are normalized (y smaller = higher/up)
    return landmarks[tip_idx][1] < landmarks[pip_idx][1]

# helper: thumb is extended check (simple heuristic using x)
def thumb_is_up(landmarks):
    return landmarks[4][0] < landmarks[3][0]  

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    gesture_label = "No hand"

    if res.multi_hand_landmarks:
        # only use first detected hand
        hand_landmarks = res.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # convert to numpy array [21 x 3]
        lm = np.array([[p.x, p.y, p.z] for p in hand_landmarks.landmark])
        lm = smooth_landmarks(lm)

        # compute finger states
        thumb_up = thumb_is_up(lm)
        index_up = finger_is_up(lm, 8, 6)
        middle_up = finger_is_up(lm, 12, 10)
        ring_up = finger_is_up(lm, 16, 14)
        pinky_up = finger_is_up(lm, 20, 18)

        # Fist: all fingers down (tips below pips)
        if (not index_up) and (not middle_up) and (not ring_up) and (not pinky_up):
            gesture_label = "Fist (Pause/Play)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.press("space")

        # Open palm: all fingers up
        elif index_up and middle_up and ring_up and pinky_up:
            gesture_label = "Open Palm (High Speed)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.hotkey("shift",".")

        # Two fingers (index + middle) up -> Volume Up
        elif index_up and middle_up and (not ring_up) and (not pinky_up):
            gesture_label = "Peace sign (Vol Up)"
            if is_stable(gesture_label) and can_trigger_action():
                for i in range(5):
                  pyautogui.press("volumeup")

        # Ring + pinky -> Volume Down (index & middle down)
        elif (not index_up) and (not middle_up) and ring_up and pinky_up:
            gesture_label = "Inverted peace/Ring+ Pink (Vol Down)"
            if is_stable(gesture_label) and can_trigger_action():
                for i in range(5):
                   i=i-5
                   pyautogui.press("volumedown")

        # Pinky only -> Next Video (pinky up, others down)
        elif (not index_up) and (not middle_up) and (not ring_up) and pinky_up:
            gesture_label = "Pinky Only (Next)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.hotkey("shift", "n")

        # All except pinky -> Previous Video (index+middle+ring up, pinky down)
        elif index_up and middle_up and ring_up and (not pinky_up):
            gesture_label = "All except pinky (Previous)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.hotkey("shift", "p")
                
        # 👍 MIDDLE + ring →  Theater Mode
        elif (not index_up) and middle_up and ring_up and (not pinky_up):
            gesture_label = " Middle + Ring (Theater Mode)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.press("t")

        #index -> slower
        elif index_up and (not middle_up) and (not ring_up) and (not pinky_up):
            gesture_label = "Index Only (Slower)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.hotkey("shift", ",")

        # Three Fingers (Index + Ring + Pinky) → Forward
        elif index_up and (not middle_up) and  ring_up and pinky_up:
            gesture_label = " All Except Middle Up (Forward)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.hotkey("shift", "right")

        # Three Fingers (Index + Middle + Pinky) → Rewind
        elif index_up and middle_up and (not ring_up) and pinky_up:
            gesture_label = "All Except Ring Up (Rewind)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.hotkey("shift", "left")

        # Super Gesture (Index + Middle + Pinky Up) → Fullscreen
        elif (not index_up) and middle_up and ring_up and pinky_up :
            gesture_label = "Super Gesture (Fullscreen)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.press("f")

        # 🤘 Rock Sign (Index + Pinky Up) → Mute/Unmute
        elif index_up and (not middle_up) and (not ring_up) and pinky_up:
            gesture_label = "🤘 Rock Sign (Mute/Unmute)"
            if is_stable(gesture_label) and can_trigger_action():
                pyautogui.press("m")

        else:
            # intermediate states — show immediate label but don't trigger actions
            # build a descriptive label for debugging
            parts = []
            if index_up: parts.append("Index")
            if middle_up: parts.append("Middle")
            if ring_up: parts.append("Ring")
            if pinky_up: parts.append("Pinky")
            if not parts:
                parts = ["Closed"]
            gesture_label = " + ".join(parts)

    # show current detected gesture instantly for user feedback
    cv2.putText(frame, f"Gesture: {gesture_label}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2, cv2.LINE_AA)

    cv2.imshow("YouTube Gesture Control - AirPointer", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
