def count_fingers(landmarks):
    """
    Takes a list of 21 (x, y) landmark points and returns
    the number of extended fingers (0 to 5).
    """
    fingers_up = 0

    # Landmark indices for each fingertip and the joint below it (PIP joint)
    # Thumb is handled differently because it moves sideways, not up/down
    finger_tips_pips = [
        (8, 6),    # Index finger: tip=8, pip=6
        (12, 10),  # Middle finger: tip=12, pip=10
        (16, 14),  # Ring finger: tip=16, pip=14
        (20, 18),  # Pinky: tip=20, pip=18
    ]

    # For these 4 fingers: if tip's Y is above (smaller than) pip's Y, finger is extended
    # (Remember: in image coordinates, Y increases downward)
    for tip_idx, pip_idx in finger_tips_pips:
        if landmarks[tip_idx][1] < landmarks[pip_idx][1]:
            fingers_up += 1

    # Thumb: compare tip(4) x-position to the joint before it(3)
    # This is a simplified check — works reasonably for a hand facing the camera
    if landmarks[4][0] > landmarks[3][0]:
        fingers_up += 1

    return fingers_up