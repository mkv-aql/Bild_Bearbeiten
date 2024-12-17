__author__ = 'mkv-aql'

import cv2
import tkinter as tk
from tkinter import simpledialog
from threading import Thread


# Function to open a Tkinter input dialog to enter text
def ask_input(prompt):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_input = simpledialog.askstring("Input", prompt)
    return user_input


# Function to handle capturing video from the webcam
def open_camera():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Display the frame
        cv2.imshow("Camera", frame)

        # Press 'q' to exit the camera window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Tkinter GUI
def tkinter_gui():
    root = tk.Tk()
    root.title("OpenCV GUI with Tkinter")

    def on_submit():
        user_text = text_input.get()  # Get the input text
        user_number = number_input.get()  # Get the input number

        # Print the values entered in Tkinter GUI
        print(f"Text: {user_text}, Number: {user_number}")

        # After printing, clear the fields
        text_input.delete(0, tk.END)
        number_input.delete(0, tk.END)

    # Text input
    text_label = tk.Label(root, text="Enter Text:")
    text_label.pack()
    text_input = tk.Entry(root)
    text_input.pack()

    # Number input
    number_label = tk.Label(root, text="Enter Number:")
    number_label.pack()
    number_input = tk.Entry(root)
    number_input.pack()

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack()

    # Run Tkinter main loop
    root.mainloop()


# Threading the GUI and OpenCV so they can run concurrently
if __name__ == "__main__":
    # Create a thread for the OpenCV camera function
    camera_thread = Thread(target=open_camera)
    camera_thread.daemon = True  # Daemonize the thread so it closes when main program exits
    camera_thread.start()

    # Run Tkinter GUI in the main thread
    tkinter_gui()
