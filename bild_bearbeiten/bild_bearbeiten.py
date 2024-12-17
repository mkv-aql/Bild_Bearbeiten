import cv2
import pandas as pd
import ast

from multiple_buttons_opencv import button_positions

df_capture = pd.read_csv('../csv_files/capture_test.csv')

# Button Coordinates:
    #Save button corrdinates
button_top_left = (0, 0)
button_bottom_right = (100, 50)

# Function to convert the bbox string to a list of integers
def parse_bbox(bbox_str):
    # Remove the np.int32() parts and evaluate the string safely
    cleaned_str = bbox_str.replace('np.int32(', '').replace(')', '')
    return ast.literal_eval(cleaned_str)


# Apply the function to the bbox column
df_capture['bbox'] = df_capture['bbox'].apply(parse_bbox)
print(f'size of df_capture: {df_capture.size}')

# Now, df['bbox'] contains lists of integer coordinates
# print(df_capture['bbox'].tolist()) # List of lists of integers
print(df_capture['bbox'])

# Remove Bildname and confidence level columns
df_capture.drop(columns=['Bildname', 'Confidence Level'], inplace=True)
print(df_capture)

#Button functions
def mouse_callback_remove_index(event, x, y, flags, param):
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
                remove_index(index)
            else:
                print(f'Index not found, next index')
                continue
            break

def mouse_callback_save(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'x: {x}, y: {y}')
        if button_top_left[0] < x < button_bottom_right[0] and button_top_left[1] < y < button_bottom_right[1]:
            save_csv(csv=1)

def remove_index(index):
    df_capture.drop(index, inplace=True)
    print(f'Index {index} removed')

def save_csv(csv):
    print(f'Save button clicked')
    pass

def draw_button(frame):
    # Draw button and setup mouse callback
    cv2.rectangle(frame, button_top_left, button_bottom_right, (255, 0, 0), -1) # -1 to fill the rectangle
    cv2.putText(frame, 'Save',
                (button_top_left[0] + 10, button_top_left[1] + 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 1, cv2.LINE_AA)
    cv2.namedWindow('edit')
    cv2.setMouseCallback('edit', mouse_callback_save)

while True:
    img = cv2.imread('../image_files/captured_test.jpg')

    for index, row in df_capture.iterrows():
        (top_left, top_right, bottom_right, bottom_left) = row['bbox'][0], row['bbox'][1], row['bbox'][2], row['bbox'][3]
        cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)
        cv2.putText(img, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    # Draw button
    draw_button(img)

    cv2.imshow('edit', img)

    # Set mouse function
    cv2.setMouseCallback('edit', mouse_callback_remove_index)
    # cv2.setMouseCallback('edit', mouse_callback_save)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

