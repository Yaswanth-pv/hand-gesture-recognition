def get_finger_states(landmarks):
    states = []
    states.append(landmarks[4][0] > landmarks[3][0])
    finger_tips_pips = [(8, 6), (12, 10), (16, 14), (20, 18)]
    for tip_idx, pip_idx in finger_tips_pips:
        states.append(landmarks[tip_idx][1] < landmarks[pip_idx][1])
    return states

def count_fingers(landmarks):
    return sum(get_finger_states(landmarks))

def recognize_gesture(landmarks):
    thumb, index, middle, ring, pinky = get_finger_states(landmarks)
    if not any([thumb, index, middle, ring, pinky]):
        return "Fist"
    if all([thumb, index, middle, ring, pinky]):
        return "Open Palm"
    if index and middle and not ring and not pinky and not thumb:
        return "Peace"
    if thumb and not index and not middle and not ring and not pinky:
        return "Thumbs Up"
    if index and not middle and not ring and not pinky and not thumb:
        return "Pointing"
    if index and pinky and not middle and not ring and not thumb:
        return "Rock"
    if thumb and pinky and not index and not middle and not ring:
        return "Call Me"
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    distance = ((thumb_tip[0] - index_tip[0])**2 + (thumb_tip[1] - index_tip[1])**2) ** 0.5
    if distance < 60 and middle and ring and pinky:
        return "OK"
    return "Unknown"
