import cv2
import numpy as np

# Create a blank image
img = np.zeros((400, 600, 3), dtype=np.uint8)

# System State
state = 1

# Define button dimensions
button_height = 50
button_width = 100

# Define button positions
button_positions_1 = {
    'Change Case to 2': (50, 50),
    'Button2': (200, 50),
    'Button3': (350, 50)
}

# Define button positions
button_positions_2 = {
    'Change Case to 1': (100, 100),
    'Button5': (250, 100),
    'Button6': (400, 100)
}

# Function to draw buttons
def draw_buttons_1():
    for btn, pos in button_positions_1.items():
        cv2.rectangle(img, pos, (pos[0] + button_width, pos[1] + button_height), (200, 200, 200), -1)
        cv2.putText(img, btn, (pos[0] + 10, pos[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

def draw_buttons_2():
    for btn, pos in button_positions_2.items():
        cv2.rectangle(img, pos, (pos[0] + button_width, pos[1] + button_height), (200, 200, 200), -1)
        cv2.putText(img, btn, (pos[0] + 10, pos[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

# Define callback functions for each button
def button1_callback_1():
    global state
    state = 2
    print("Button 1 clicked!")

def button2_callback_1():
    print("Button 2 clicked!")

def button3_callback_1():
    print("Button 3 clicked!")

# Create a dictionary to map button clicks to functions
button_callbacks_1 = {
    'Change Case to 2': button1_callback_1,
    'Button2': button2_callback_1,
    'Button3': button3_callback_1
}

# Define callback functions for each button
def button4_callback_2():
    global state
    state = 1
    print("Button 4 clicked!")

def button5_callback_2():
    print("Button 5 clicked!")

def button6_callback_2():
    print("Button 6 clicked!")

button_callbacks_2 = {
    'Change Case to 1': button4_callback_2,
    'Button5': button5_callback_2,
    'Button6': button6_callback_2
}

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:

        match state:
            case 1:
                for btn, pos in button_positions_1.items():
                    if pos[0] < x < pos[0] + button_width and pos[1] < y < pos[1] + button_height:
                        button_callbacks_1[btn]()
                        print(f'Button {btn} clicked!')

            case 2:
                for btn, pos in button_positions_2.items():
                    if pos[0] < x < pos[0] + button_width and pos[1] < y < pos[1] + button_height:
                        button_callbacks_2[btn]()
                        print(f'Button {btn} clicked!')

        # for btn, pos in button_positions_1.items():
        #     if pos[0] < x < pos[0] + button_width and pos[1] < y < pos[1] + button_height:
        #         button_callbacks_1[btn]()  # Call the corresponding function
        #         print(f'Button {btn} clicked!')

# Setup the window and mouse callback
cv2.namedWindow("Buttons Example")
cv2.setMouseCallback("Buttons Example", mouse_callback)

# Main loop
while True:
    img[:] = (0, 0, 0)  # Clear the image
    if state == 1:
        draw_buttons_1()      # Draw buttons
    elif state == 2:
        draw_buttons_2()      # Draw buttons
    else:
        print("Invalid state!")

    cv2.imshow("Buttons Example", img)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
