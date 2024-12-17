import cv2
import numpy as np

# Create a blank image
img = np.zeros((400, 600, 3), dtype=np.uint8)

# Define button dimensions
button_height = 50
button_width = 100

# Define button positions
button_positions = {
    'Button1': (50, 50),
    'Button2': (200, 50),
    'Button3': (350, 50)
}

# Function to draw buttons
def draw_buttons():
    for btn, pos in button_positions.items():
        cv2.rectangle(img, pos, (pos[0] + button_width, pos[1] + button_height), (200, 200, 200), -1)
        cv2.putText(img, btn, (pos[0] + 10, pos[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

# Define callback functions for each button
def button1_callback():
    print("Button 1 clicked!")

def button2_callback():
    print("Button 2 clicked!")

def button3_callback():
    print("Button 3 clicked!")

# Create a dictionary to map button clicks to functions
button_callbacks = {
    'Button1': button1_callback,
    'Button2': button2_callback,
    'Button3': button3_callback
}

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for btn, pos in button_positions.items():
            if pos[0] < x < pos[0] + button_width and pos[1] < y < pos[1] + button_height:
                button_callbacks[btn]()  # Call the corresponding function
                print(f'Button {btn} clicked!')

# Setup the window and mouse callback
cv2.namedWindow("Buttons Example")
cv2.setMouseCallback("Buttons Example", mouse_callback)

# Main loop
while True:
    img[:] = (0, 0, 0)  # Clear the image
    draw_buttons()      # Draw buttons
    cv2.imshow("Buttons Example", img)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
