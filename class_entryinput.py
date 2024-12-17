__author__ = 'mkv-aql'
import cv2
import tkinter as tk
from tkinter import simpledialog
from threading import Thread

class OpenCVTkinterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window (for asking input)
        self.text_input = None
        self.number_input = None
        self.camera_thread = None

    # Function to open a Tkinter input dialog to enter text
    def ask_input(self, prompt):
        user_input = simpledialog.askstring("Input", prompt)
        return user_input

    # Function to handle capturing video from the webcam
    def open_camera(self):
        cap = cv2.VideoCapture(0)  # Open the default camera (webcam)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Live Webcam Feed", frame)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    # Tkinter GUI
    def tkinter_gui(self):
        self.root.deiconify()  # Show the hidden root window
        self.root.title("OpenCV GUI with Tkinter")

        def on_submit():
            user_text = self.text_input.get()  # Get the input text
            user_number = self.number_input.get()  # Get the input number

            # Print the values entered in Tkinter GUI
            print(f"Text: {user_text}, Number: {user_number}")

            # After printing, clear the fields
            self.text_input.delete(0, tk.END)
            self.number_input.delete(0, tk.END)

        # Text input
        text_label = tk.Label(self.root, text="Enter Text:")
        text_label.pack()
        self.text_input = tk.Entry(self.root)
        self.text_input.pack()

        # Number input
        number_label = tk.Label(self.root, text="Enter Number:")
        number_label.pack()
        self.number_input = tk.Entry(self.root)
        self.number_input.pack()

        # Submit button
        submit_button = tk.Button(self.root, text="Submit", command=on_submit)
        submit_button.pack()

        # Run Tkinter main loop
        self.root.mainloop()

    # Function to run both the camera and the GUI concurrently
    def run(self):
        # Create a thread for the OpenCV camera function
        self.camera_thread = Thread(target=self.open_camera)
        self.camera_thread.daemon = True  # Daemonize the thread so it closes when main program exits
        self.camera_thread.start()

        # Run Tkinter GUI in the main thread
        self.tkinter_gui()

# Instantiate and run the application
if __name__ == "__main__":
    app = OpenCVTkinterApp()
    app.run()
