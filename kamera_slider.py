import cv2

# Callback function for the trackbar (not used here)
def nothing(x):
    pass

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create a window
cv2.namedWindow('Camera Feed')

# Create a trackbar (slider) from 0 to 100
cv2.createTrackbar('Slider', 'Camera Feed', 0, 100, nothing)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Get the current position of the slider
    slider_value = cv2.getTrackbarPos('Slider', 'Camera Feed')

    # Calculate the percentage
    percentage = slider_value  # Since the slider range is 0-100

    # Display the percentage on the frame
    cv2.putText(frame, f'Percentage: {percentage}%', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Show the frame
    cv2.imshow('Camera Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
