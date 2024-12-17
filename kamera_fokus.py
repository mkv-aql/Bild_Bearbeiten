__author__ = 'mkv-aql'

import cv2

# Initialize the webcam
cap = cv2.VideoCapture(1)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set focus (This might not work on all cameras)
# Set focus to a value between 0 and 255, depending on your camera's supported range
focus_value = 30  # Adjust this value as needed
if cap.set(cv2.CAP_PROP_FOCUS, focus_value):
    print(f"Focus set to {focus_value}")
else:
    print("Focus control not supported on this camera.")

# Read frames from the camera and display them
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow('frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
