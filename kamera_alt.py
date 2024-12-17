import cv2
from pytesseract import Output, pytesseract
import easyocr
import PIL
import numpy as np
import re
import pandas as pd
import torch

pd.set_option('display.max_columns', None)  # Display all columns
np.set_printoptions(linewidth=200, precision=4)

# Check GPU with torch
print(f'Cuda is available: {torch.cuda.is_available()}')
print(f'Cuda device count: {torch.cuda.device_count()}')
print(f'Cuda current device: {torch.cuda.current_device()}')
print(f'Cuda device name: {torch.cuda.get_device_name()}')


# Set up
# empty dataframe to store bbox and Namen
df_capture = pd.DataFrame(columns=['bbox', 'Namen', 'Confidence Level', 'Bildname'])


# Set pytesseract path, UNCOMMENT if using pytesseract
# pytesseract.tesseract_cmd = r'C:\\Users\\AgamSafaruddinDeutsc\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
# Initialize EasyOCR with german
# reader = easyocr.Reader(['de'])

# Process frame for Pytesseract
def process_frame_ocr(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh


# Filter text
def filter_text(text):
    if re.match(r'^\d+[a-zA-Z0-9\-\/]*$', text):
        return False
    if text.lower() in ['klingel', 'licht', 'sss siedle', 'sss', 'siedle', 'werbung', 'klingeln', 'kräftig',
                        'bitte', 'einen', 'eingang', 'weiter', 'zu', 'video', 'überwachung', 'videoüberwachung',
                        'werbung!',
                        'keine', 'oder', 'zeitungen', 'einwerfen', 'danke', 'oder zeitungen einwerfen!danke',
                        'hier wohnt', 'hier',
                        'wohnt', 'familie', 'fam', 'fam.', 'fa', 'fa.', 'elcom']:
        return False
    return True


def ocr(image_path, reader):
    # Initialize EasyOCR with german, but outside of function for better performance
    # reader = easyocr.Reader(['de'], gpu=False, recog_network='latin_g2') # recog fuer bessere Genauigkeit
    ocr_results = reader.readtext(image_path, contrast_ths=0.05, adjust_contrast=0.7, text_threshold=0.8, low_text=0.4)
    dfOCRResults = pd.DataFrame(ocr_results, columns=['bbox', 'Namen', 'Confidence Level'])

    return dfOCRResults


# Callback function for mouse
def mouse_callback(event, x, y, flags, param):
    global button_top_left, button_bottom_right, df_capture
    if event == cv2.EVENT_LBUTTONDOWN:
        if button_top_left[0] < x < button_bottom_right[0] and button_top_left[1] < y < button_bottom_right[1]:

            # For normal camera method
            reader = easyocr.Reader(['de'], gpu=True, recog_network='latin_g2')  # recog fuer bessere Genauigkeit
            text_frame = ocr(frame, reader)  # Returned as DataFrame: bbox, Namen, Confidence Level, Bildname
            for index, row in text_frame.iterrows():
                (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], \
                row['bbox'][3]
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(frame, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

            print('Captured')
            cv2.imwrite('image_files/captured.jpg', frame)  # Save captured image
            cv2.imwrite('image_files/captured_clean.jpg', frame_clean)  # Save captured image
            df_capture = pd.concat([df_capture, pd.DataFrame(text_frame)], ignore_index=True)
            # save to csv
            df_capture.to_csv('capture.csv', index=False)


# Draw button and setup mouse callback function
# Button boundaries
button_top_left = (0, 0)
button_bottom_right = (50, 50)


def draw_button(frame):
    # Draw button and setup mouse callback
    cv2.rectangle(frame, button_top_left, button_bottom_right, (255, 0, 0), 2)
    cv2.putText(frame, 'Click to capture',
                (button_top_left[0] + 10, button_top_left[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 1, cv2.LINE_AA)
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', mouse_callback)


def prepare_camera():
    # Open camera
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(1) # Open second camera
    # reduce size of resolution
    cap.set(3, 480)
    # Cap the frame rate to 15
    cap.set(5, 15)
    # set brightness
    cap.set(10, 150)
    # set constrast
    cap.set(11, 50)

    return cap


# Open camera
cap = prepare_camera()

# Pytessract Method
'''
#Interval frame count
frame_interval = 3
frame_count = 0

while True:
    ret, frame = cap.read()

    # Draw button and setup mouse callback
    cv2.rectangle(frame, button_top_left, button_bottom_right, (255, 0, 0), 2)
    cv2.putText(frame, 'Click test', (button_top_left[0] + 10, button_top_left[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', mouse_callback) 

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #results = reader.readtext(gray)

    #Apply frame count
    frame_count += 1

    if frame_count % frame_interval == 0:


        #Bounding box with Pytesseract

        details = pytesseract.image_to_data(gray, output_type=Output.DICT)
        #print(f'Details: {details}')
        n_boxes = len(details['text'])
        for i in range(n_boxes):
            if int(details['conf'][i]) > 40: #confidence level 60%
                (x, y, w, h) = (details['left'][i], details['top'][i], details['width'][i], details['height'][i])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
                cv2.putText(frame, details['text'][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA) 



        # Using Pytesseract
        process_frame = process_frame_ocr(frame)
        text = pytesseract.image_to_string(process_frame)
        # text = pytesseract.image_to_string(frame)

        print(f'Detected Text: {text.strip()}')


        cv2.imshow('frame', frame)
        #cv2.imshow('processed', process_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
'''

# OCR Method

# Initialize EasyOCR with german, but outside of function for better performance
reader = easyocr.Reader(['de'], gpu=True, recog_network='latin_g2') # recog fuer bessere Genauigkeit
while True:
    ret, frame = cap.read()

    # Copy of frame
    frame_clean = frame.copy()

    # Using OCR
    text_frame = ocr(frame, reader) # Returned as DataFrame: bbox, Namen, Confidence Level, Bildname
    print(f'\nDetected Text: \n{text_frame}')
    # print(f'\nFiltered Text: \n{process_frame[process_frame['Namen'].apply(filter_text)]}')

    # # print first row of the DataFrame
    # if not text_frame.empty:
    #     print(f'\nFirst Row: \n{text_frame.iloc[0,0]}') #iloc[row, column]


    # Bounding Box with EasyOCR Old
    # for index, row in text_frame.iterrows():
    #     (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], row['bbox'][3]
    #     # print(f'\nType: {type(row)}') #pandas.core.series.Series
    #     # print(f'\nType:{type(top_left)}') #list
    #     # print(f'\nType:{type(top_left[0])}') #numpy.int32
    #     cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
    #     cv2.putText(frame, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # Boundin Box with EasyOCR New
    for index, row in text_frame.iterrows():
        top_left = tuple(map(int, row['bbox'][0]))
        bottom_right = tuple(map(int, row['bbox'][2]))
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(frame, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # Draw button
    draw_button(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''

# Normal camera method
while True:
    ret, frame = cap.read()
    # Copy of frame
    frame_clean = frame.copy()

    if not ret:
        print('Error: Could not read frame')
        break

    # Draw button
    draw_button(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''

# EDIT PHASE
# Draw all button of bounding box
def create_button_bbox(img, df_capture):
    for index, row in df_capture.iterrows():
        (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], row['bbox'][
            3]

    return 0


# Button functions
def mouse_callback_2(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'x: {x}, y: {y}')

        for index, row in df_capture.iterrows():
            (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], \
            row['bbox'][3]
            button_top_left_name = (top_left[0] - 10, top_left[1] - 10)
            button_bottom_right_name = (bottom_right[0] + 10, bottom_right[1] + 10)
            print(f'\nbutton_top_left_name: {button_top_left_name}')
            print(f'\nbutton_bottom_right_name: {button_bottom_right_name}')
            if button_top_left_name[0] < x < button_bottom_right_name[0] and button_top_left_name[1] < y < \
                    button_bottom_right_name[1]:
                print(f'Index: {index} clicked')


# open image with openCV
while True:
    img = cv2.imread('image_files/captured.jpg')

    for index, row in df_capture.iterrows():
        (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], row['bbox'][
            3]

        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(img, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # create_button_bbox(img, df_capture)

    cv2.imshow('edit', img)

    # Set mouse function
    cv2.setMouseCallback('edit', mouse_callback_2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



