import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
from gesture_logic import count_fingers, recognize_gesture
import pyautogui
import subprocess
import sys
import time

# ── Voice engine setup ──────────────────────────────────────────────
def speak(text):
    """Speak text using a separate Python process — most reliable on Windows."""
    script = f"import pyttsx3; e=pyttsx3.init(); e.setProperty('rate',150); e.say('{text}'); e.runAndWait()"
    subprocess.Popen([sys.executable, "-c", script])

# ── MediaPipe setup ──────────────────────────────────────────────────
MODEL_PATH = "models/hand_landmarker.task"

base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

# ── Webcam setup ─────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Hand tracking started. Press 'q' to quit.")

# ── Hand skeleton connections ─────────────────────────────────────────
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

# ── Gesture action mapping ────────────────────────────────────────────
def action_screenshot():
    screenshot = pyautogui.screenshot()
    filename = f"data/screenshot_{int(time.time())}.png"
    screenshot.save(filename)
    print(f"Screenshot saved: {filename}")

GESTURE_ACTIONS = {
    "Open Palm": action_screenshot,
}

# ── Cooldown tracking ─────────────────────────────────────────────────
last_gesture = ""
last_action_time = 0
COOLDOWN_SECONDS = 2
last_spoken_gesture = ""
last_spoken_time = 0
stable_gesture = ""
stable_gesture_time = 0
STICKY_SECONDS = 1.5

# ── Main loop ─────────────────────────────────────────────────────────
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        h, w, _ = frame.shape

        for i, hand_landmarks in enumerate(result.hand_landmarks):
            points = []
            for landmark in hand_landmarks:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                points.append((x, y))

            gesture_name = recognize_gesture(points)
            current_time = time.time()

            # Sticky gesture: if Unknown, keep showing last stable gesture briefly
            if gesture_name == "Unknown" or not gesture_name:
                if current_time - stable_gesture_time < STICKY_SECONDS:
                    gesture_name = stable_gesture
                else:
                    gesture_name = ""
            else:
                stable_gesture = gesture_name
                stable_gesture_time = current_time

            finger_count = count_fingers(points)

            # Display info on screen
            y_offset = 50 + i * 80
            display_gesture = gesture_name if gesture_name else ""
            cv2.putText(frame, f"Hand {i+1} | Fingers: {finger_count} | Gesture: {display_gesture}",
                        (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # Draw skeleton
            for start_idx, end_idx in HAND_CONNECTIONS:
                cv2.line(frame, points[start_idx], points[end_idx], (255, 0, 0), 2)

            # Draw landmark dots
            for (x, y) in points:
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            # Voice announcement with cooldown (only for first hand)
            if i == 0 and gesture_name and gesture_name != "Unknown":
                if (gesture_name != last_spoken_gesture or
                        current_time - last_spoken_time > COOLDOWN_SECONDS):
                    speak(gesture_name)
                    last_spoken_gesture = gesture_name
                    last_spoken_time = current_time

            # Trigger action with cooldown
            if gesture_name in GESTURE_ACTIONS:
                if (gesture_name != last_gesture or
                        current_time - last_action_time > COOLDOWN_SECONDS):
                    GESTURE_ACTIONS[gesture_name]()
                    last_gesture = gesture_name
                    last_action_time = current_time

    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()