import cv2
import numpy as np


# Global variables
drawing = False  # True if the mouse is pressed
ix, iy = -1, -1  # Initial coordinates
rectangles = []  # To store rectangles
undo_stack = []  # To keep track of the drawn rectangles

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, rectangles

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Create a temporary frame to display the rectangle
            temp_frame = frame.copy()
            cv2.rectangle(temp_frame, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('Image', temp_frame)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(frame, (ix, iy), (x, y), (0, 255, 0), 2)
        rectangles.append(((ix, iy), (x, y)))  # Save the coordinates
        undo_stack.append(((ix, iy), (x, y)))  # Save to undo stack
        cv2.imshow('Image', frame)
        print(f"Highlighted area: {((ix, iy), (x, y))}")  # Print coordinates

def undo_last_rectangle():
    if undo_stack:
        undo_stack.pop()  # Remove the last rectangle from the undo stack
        redraw_frame()

def redraw_frame():
    global frame
    frame = np.zeros((500, 500, 3), dtype=np.uint8)  # Reset the frame
    for rect in undo_stack:
        cv2.rectangle(frame, rect[0], rect[1], (0, 255, 0), 2)
    cv2.imshow('Image', frame)

# Create a blank black image
frame = np.zeros((500, 500, 3), dtype=np.uint8)  # 500x500 pixels
cv2.imshow('Image', frame)

# Bind the mouse callback function to the window
cv2.setMouseCallback('Image', draw_rectangle)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('u'):  # Press 'u' to undo the last rectangle
        undo_last_rectangle()
    elif key == 27:  # Press 'Esc' to exit
        break

cv2.destroyAllWindows()

# Print all highlighted rectangles
print("All highlighted areas:", rectangles)
