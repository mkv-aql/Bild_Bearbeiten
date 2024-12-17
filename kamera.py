import cv2
import torch
from pytesseract import Output, pytesseract
import easyocr
import PIL
import numpy as np
import re
import pandas as pd
import threading
pd.set_option('display.max_columns', None) # Display all columns
np.set_printoptions(linewidth=200, precision = 4)

print(f'Cuda is available: {torch.cuda.is_available()}')
print(f'Cuda device count: {torch.cuda.device_count()}')
print(f'Cuda current device: {torch.cuda.current_device()}')
print(f'Cuda device name: {torch.cuda.get_device_name()}')

# Set up
# empty dataframe to store bbox and Namen
df_capture = pd.DataFrame(columns=['bbox', 'Namen', 'Confidence Level', 'Bildname'])

# Filter text
def filter_text(text):
    if re.match(r'^\d+[a-zA-Z0-9\-\/]*$', text):
        return False
    if text.lower() in ['klingel', 'licht','sss siedle','sss', 'siedle','werbung','klingeln','kräftig',
                        'bitte','einen','eingang','weiter','zu','video','überwachung','videoüberwachung','werbung!',
                        'keine','oder','zeitungen','einwerfen','danke','oder zeitungen einwerfen!danke', 'hier wohnt','hier',
                        'wohnt','familie','fam', 'fam.', 'fa', 'fa.','elcom']:
        return False
    return True

def ocr(image_path, reader):
    ocr_results = reader.readtext(image_path, contrast_ths=0.05, adjust_contrast=0.7, text_threshold=0.8, low_text=0.4)
    dfOCRResults = pd.DataFrame(ocr_results, columns=['bbox', 'Namen', 'Confidence Level'])

    return dfOCRResults



# Callback function for mouse
def mouse_callback(event, x, y, flags, param):
    global button_top_left, button_bottom_right, df_capture
    if event == cv2.EVENT_LBUTTONDOWN:
        if button_top_left[0] < x < button_bottom_right[0] and button_top_left[1] < y < button_bottom_right[1]:

            # For normal camera method
            reader = easyocr.Reader(['de'], gpu=False, recog_network='latin_g2')  # recog fuer bessere Genauigkeit
            text_frame = ocr(frame, reader)  # Returned as DataFrame: bbox, Namen, Confidence Level, Bildname
            for index, row in text_frame.iterrows():
                (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], row['bbox'][3]
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(frame, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

            print('Captured')
            cv2.imwrite('image_files/captured.jpg', frame) # Save captured image
            cv2.imwrite('image_files/captured_clean.jpg', frame_clean) # Save captured image
            df_capture = pd.concat([df_capture, pd.DataFrame(text_frame)], ignore_index=True)
            # save to csv
            df_capture.to_csv('capture.csv', index=False)


# Draw button and setup mouse callback function
# Capture button boundaries
button_top_left = (0, 0)
button_bottom_right = (50, 50)
# Save button boundaries
# button_top_left = (frame.shape[1] - 100, frame.shape[0] - 50)
# button_bottom_right = (frame.shape[1], frame.shape[0])


def draw_button(frame):
    # Draw button and setup mouse callback
    cv2.rectangle(frame, button_top_left, button_bottom_right, (255, 0, 0), 2)
    cv2.putText(frame, 'Click to capture',
                (button_top_left[0] + 10, button_top_left[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 1, cv2.LINE_AA)
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', mouse_callback)

def create_slider(frame):
    # Create a trackbar (slider) from 0 to 200
    cv2.createTrackbar('Helligkeitswert', 'frame', 0, 200, edit_camera_settings)


def prepare_camera():
    # Open camera
    # cap = cv2.VideoCapture(0) # Webcam
    cap = cv2.VideoCapture(1) # USB camera
    # reduce size of resolution
    cap.set(3, 720)
    # Cap the frame rate to 15
    cap.set(5, 15)
    # set brightness
    cap.set(10, 150)
    # set constrast
    cap.set(11, 50)

    return cap

def edit_camera_settings(x):
    # Get the current position of the slider
    slider_value = cv2.getTrackbarPos('Helligkeitswert', 'frame')
    # Change brightness
    cap.set(propId=10, value= slider_value)

#Open camera
cap = prepare_camera()
slider_status = 0
while True:
    ret, frame = cap.read()
    # Copy of frame
    frame_clean = frame.copy()

    if not ret: print('Error: Could not read frame'); break

    # Draw button
    draw_button(frame)

    # create slider
    if slider_status == 0: create_slider(frame); slider_status = 1

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# EDIT PHASE
# Draw all button of bounding box
def create_button_bbox(img, df_capture):
    for index, row in df_capture.iterrows():
        (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], row['bbox'][3]

    return 0

#Button functions
def mouse_callback_2(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'x: {x}, y: {y}')

        for index, row in df_capture.iterrows():
            (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], row['bbox'][3]
            button_top_left_name = (top_left[0] - 10, top_left[1] - 10)
            button_bottom_right_name = (bottom_right[0] + 10, bottom_right[1] + 10)
            print(f'\nbutton_top_left_name: {button_top_left_name}')
            print(f'\nbutton_bottom_right_name: {button_bottom_right_name}')
            if button_top_left_name[0] < x < button_bottom_right_name[0] and button_top_left_name[1] < y < button_bottom_right_name[1]:
                print(f'Index: {index} clicked')

# open image with openCV
while True:
    img = cv2.imread('image_files/captured.jpg')

    for index, row in df_capture.iterrows():
        (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], row['bbox'][3]

        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(img, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)


    # create_button_bbox(img, df_capture)

    cv2.imshow('edit', img)

    #Set mouse function
    cv2.setMouseCallback('edit', mouse_callback_2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



