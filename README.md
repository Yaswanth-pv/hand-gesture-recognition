# Hand Gesture Recognition System

A real-time hand gesture recognition system built with Python, OpenCV, and MediaPipe.

## Features
- Real-time hand tracking using webcam
- Detects and draws 21 hand landmarks with skeleton visualization
- Recognizes 8 gestures: Fist, Open Palm, Peace, Thumbs Up, Pointing, Rock, Call Me, OK
- Voice announcement of detected gestures using pyttsx3
- Two-hand simultaneous detection
- Screenshot action triggered by Open Palm gesture

## Tech Stack
- Python 3.10
- OpenCV - webcam capture and image processing
- MediaPipe - hand landmark detection
- pyttsx3 - text-to-speech voice feedback
- PyAutoGUI - screenshot automation

## Project Structure

    hand-gesture-recognition/
    ├── src/
    │   ├── hand_tracking.py      # Main script
    │   ├── gesture_logic.py      # Gesture recognition logic
    │   └── voice_test.py         # Voice engine test
    ├── models/                   # MediaPipe model (download separately)
    ├── data/                     # Screenshots saved here
    ├── requirements.txt
    └── README.md

## Setup Instructions

### 1. Clone the repository

    git clone https://github.com/Yaswanth-pv/hand-gesture-recognition.git
    cd hand-gesture-recognition

### 2. Create and activate virtual environment

    python -m venv venv
    source venv/Scripts/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Download the MediaPipe model

    curl -L -o models/hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

### 5. Run

    python src/hand_tracking.py

## Supported Gestures

| Gesture    | Description                  | Action           |
|------------|------------------------------|------------------|
| Fist       | All fingers closed           | None             |
| Open Palm  | All fingers extended         | Takes screenshot |
| Peace      | Index and middle up          | None             |
| Thumbs Up  | Only thumb extended          | None             |
| Pointing   | Only index finger up         | None             |
| Rock       | Index and pinky up           | None             |
| Call Me    | Thumb and pinky up           | None             |
| OK         | Thumb and index touching     | None             |

## Git Workflow
- All development happens on the dev branch
- Stable, tested code is merged into main

## Author
Yaswanth-pv