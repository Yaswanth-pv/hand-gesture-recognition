import cv2

# Open the default webcam (0 = first connected camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam opened. Press 'q' to quit.")

while True:
    ret, frame = cap.read()  # read one frame from the webcam

    if not ret:
        print("Error: Failed to grab frame.")
        break

    cv2.imshow("Webcam Test", frame)  # show the frame in a window

    # Wait 1ms for a key press; if 'q' is pressed, break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()          # release the camera
cv2.destroyAllWindows() # close the window