def count_fingers(landmarks):
    """
    Takes a list of 21 (x, y) landmark points and returns
    the number of extended fingers (0 to 5).
    """
    fingers_up = 0

    finger_tips_pips = [
        (8, 6),    # Index
        (12, 10),  # Middle
        (16, 14),  # Ring
        (20, 18),  # Pinky
    ]

    for tip_idx, pip_idx in finger_tips_pips:
        if landmarks[tip_idx][1] < landmarks[pip_idx][1]:
            fingers_up += 1

    if landmarks[4][0] > landmarks[3][0]:
        fingers_up += 1

    return fingers_up


def get_finger_states(landmarks):
    """
    Returns [thumb, index, middle, ring, pinky] as booleans.
    True = extended, False = folded
    """
    states = []
    states.append(landmarks[4][0] > landmarks[3][0])

    finger_tips_pips = [(8, 6), (12, 10), (16, 14), (20, 18)]
    for tip_idx, pip_idx in finger_tips_pips:
        states.append(landmarks[tip_idx][1] < landmarks[pip_idx][1])

    return states


def recognize_gesture(landmarks):
    """
    Returns a gesture name string based on which fingers are extended.
    """
    thumb, index, middle, ring, pinky = get_finger_states(landmarks)

    if not thumb and not index and not middle and not ring and not pinky:
        return "Fist"
    elif thumb and index and middle and ring and pinky:
        return "Open Palm"
    elif index and middle and not ring and not pinky and not thumb:
        return "Peace"
    elif thumb and not index and not middle and not ring and not pinky:
        return "Thumbs Up"
    elif index and not middle and not ring and not pinky and not thumb:
        return "Pointing"
    else:
        return "Unknown"