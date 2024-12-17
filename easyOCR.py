__author__ = 'mkv-aql'

import ast
import easyocr
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None) # Display all columns
np.set_printoptions(linewidth=200, precision = 4)

# df_capture = pd.DataFrame(columns=['bbox', 'Namen', 'Confidence Level', 'Bildname']) #Empty df

def ocr(image_path, reader):
    ocr_results = reader.readtext(image_path, contrast_ths=0.05, adjust_contrast=0.7, text_threshold=0.8, low_text=0.4)
    dfOCRResults = pd.DataFrame(ocr_results, columns=['bbox', 'Namen', 'Confidence Level'])

    return dfOCRResults

# save to csv fucntion
def save_csv(dfOCRResults, name):
    dfOCRResults.to_csv(f'{name}.csv', index=False)
    print(f'Saved to {name}.csv')

# Load image
# image_path = '20241004_170906.JPG'
# image_path = 'tests.jpeg'
image_path = 'image_files/Briefkaesten.jpg'
image = cv2.imread(image_path)

# get ocr results
reader = easyocr.Reader(['de'], gpu=True, recog_network='latin_g2')
dfOCRResults = ocr(image, reader)
print(dfOCRResults)

# save to csv with name without extension
save_csv(dfOCRResults, image_path.split('.')[0]) # Save to csv with name without extension


# Function to convert the bbox string to a list of integers
def parse_bbox(bbox_str):
    # Remove the np.int32() parts and evaluate the string safely
    cleaned_str = bbox_str.replace('np.int32(', '').replace(')', '')
    return ast.literal_eval(cleaned_str)

df_capture = pd.read_csv(f"{image_path.split('.')[0]}.csv") # Load csv

# Apply the function to the bbox column
df_capture['bbox'] = df_capture['bbox'].apply(parse_bbox)
print(f'size of df_capture: {df_capture.size}')

# Now, df['bbox'] contains lists of integer coordinates
# print(df_capture['bbox'].tolist()) # List of lists of integers
#print(df_capture['bbox'])

# Remove Bildname and confidence level columns
#df_capture.drop(columns=['Bildname', 'Confidence Level'], inplace=True)
print(df_capture)

for index, row in df_capture.iterrows():
    top_left = tuple(map(int, row['bbox'][0]))
    bottom_right = tuple(map(int, row['bbox'][2]))
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

# open with matplotlib too
plt.imshow(image)
plt.show()

# Resize image to fit screen
image_show = image.copy()
scale_percent = 25
width = int(image_show.shape[1] * scale_percent / 100)
height = int(image_show.shape[0] * scale_percent / 100)
dim = (width, height)
image_show = cv2.resize(image_show, dim, interpolation=cv2.INTER_AREA)


cv2.imshow('result', image_show)


cv2.waitKey(0)
cv2.destroyAllWindows()



# REDETECT NAMES
########################################################################################################################

# Cut image in half and detect names again
image = cv2.imread(image_path)
height, width, _ = image.shape
half = width // 2
image_left = image[:, :half]
image_right = image[:, half:]

# get ocr results
dfOCRResults_left = ocr(image_left, reader)
dfOCRResults_right = ocr(image_right, reader)

# save to csv with name without extension
save_csv(dfOCRResults_left, f"{image_path.split('.')[0]}_left") # Save to csv with name without extension
save_csv(dfOCRResults_right, f"{image_path.split('.')[0]}_right") # Save to csv with name without extension

# Load csv
df_capture_left = pd.read_csv(f"{image_path.split('.')[0]}_left.csv")
df_capture_right = pd.read_csv(f"{image_path.split('.')[0]}_right.csv")

# Apply the function to the bbox column
df_capture_left['bbox'] = df_capture_left['bbox'].apply(parse_bbox)

# Apply the function to the bbox column
df_capture_right['bbox'] = df_capture_right['bbox'].apply(parse_bbox)

for index, row in df_capture_left.iterrows():
    top_left = tuple(map(int, row['bbox'][0]))
    bottom_right = tuple(map(int, row['bbox'][2]))
    cv2.rectangle(image_left, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image_left, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

for index, row in df_capture_right.iterrows():
    top_left = tuple(map(int, row['bbox'][0]))
    bottom_right = tuple(map(int, row['bbox'][2]))
    cv2.rectangle(image_right, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image_right, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

# open with matplotlib both left and right
# plt.imshow(image_left)
# plt.show()
#
# plt.imshow(image_right)
# plt.show()

# Cut image in half horizontally and detect names again
image = cv2.imread(image_path)
height, width, _ = image.shape
half = height // 2
image_top = image[:half, :]
image_bottom = image[half:, :]
# get ocr results
dfOCRResults_top = ocr(image_top, reader)
dfOCRResults_bottom = ocr(image_bottom, reader)

# save to csv with name without extension
save_csv(dfOCRResults_top, f"{image_path.split('.')[0]}_top") # Save to csv with name without extension
save_csv(dfOCRResults_bottom, f"{image_path.split('.')[0]}_bottom") # Save to csv

# Load csv
df_capture_top = pd.read_csv(f"{image_path.split('.')[0]}_top.csv")
df_capture_bottom = pd.read_csv(f"{image_path.split('.')[0]}_bottom.csv")

# Apply the function to the bbox column
df_capture_top['bbox'] = df_capture_top['bbox'].apply(parse_bbox)

# Apply the function to the bbox column
df_capture_bottom['bbox'] = df_capture_bottom['bbox'].apply(parse_bbox)

for index, row in df_capture_top.iterrows():
    top_left = tuple(map(int, row['bbox'][0]))
    bottom_right = tuple(map(int, row['bbox'][2]))
    cv2.rectangle(image_top, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image_top, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

for index, row in df_capture_bottom.iterrows():
    top_left = tuple(map(int, row['bbox'][0]))
    bottom_right = tuple(map(int, row['bbox'][2]))
    cv2.rectangle(image_bottom, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image_bottom, row['Namen'], top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

# open with matplotlib both top and bottom
plt.imshow(image_top)
plt.show()

plt.imshow(image_bottom)
plt.show()


# Add up all the detected names and compare
df_capture_side = pd.concat([df_capture_left, df_capture_right])
df_capture_top_bottom = pd.concat([df_capture_top, df_capture_bottom])

# count total number of names detected
print(f'Total number of names detected: {df_capture.size}')
print(f'Total number of names detected: {df_capture_side.size}')
print(f'Total number of names detected: {df_capture_top_bottom.size}')


# Cleaning names
########################################################################################################################

# if statments of the biggest number of names detected
if df_capture.size > df_capture_side.size and df_capture.size > df_capture_top_bottom.size:
    df_capture = df_capture
elif df_capture_side.size > df_capture.size and df_capture_side.size > df_capture_top_bottom.size:
    df_capture = df_capture_side
else:
    df_capture = df_capture_top_bottom

# Remove the numbers from the names column in the dataframe
df_capture['Namen'] = df_capture['Namen'].str.replace(r'[0-9]', '', regex=True)
# Remove the special characters from the names column in the dataframe
df_capture['Namen'] = df_capture['Namen'].str.replace(r'[^\w\s]', '', regex=True)
# Seperate the names with a space in the names column into seperate rows in the dataframe
df_capture = df_capture.explode('Namen')

# Remove rows that have empty names
df_capture = df_capture[df_capture['Namen'] != '']
# Remove rowse that have names with less than 3 characters
df_capture = df_capture[df_capture['Namen'].str.len() > 2]
# Reset index
df_capture.reset_index(drop=True, inplace=True)

print(df_capture)

