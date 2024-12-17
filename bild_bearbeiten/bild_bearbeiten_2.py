import pandas as pd
import cv2
import ast
import numpy as np

# Load the CSV file and process bounding boxes
def load_bboxes(csv_file):
    df = pd.read_csv(csv_file)
    df['bbox'] = df['bbox'].apply(lambda x: ast.literal_eval(x.replace('np.int32(', '').replace(')', '')))
    return df

# Draw bounding boxes on the image
def draw_bboxes(image, bboxes):
    for bbox in bboxes:
        # Convert bbox to proper format for drawing
        pts = np.array(bbox, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

# Mouse callback function
def get_bbox(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for index, bbox in enumerate(param):
            # Check if point is inside the polygon
            if cv2.pointPolygonTest(bbox, (x, y), False) >= 0:
                print(f"Clicked inside bbox {index}: {bbox.tolist()}")

# Main function
def main(image_path, csv_file):
    # Load bounding boxes from CSV
    df = load_bboxes(csv_file)

    # Open the image
    image = cv2.imread(image_path)
    if image is None:
        print("Could not open or find the image.")
        return

    # Draw bounding boxes on the image
    bboxes = df['bbox'].tolist()
    draw_bboxes(image, bboxes)

    # Set mouse callback
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", get_bbox, param=bboxes)

    # Display the image
    while True:
        cv2.imshow("Image", image)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Esc key to exit
            break

    cv2.destroyAllWindows()


# Example usage
if __name__ == "__main__":

    image_path = '../image_files/captured_clean.jpg'  # Replace with your image path
    csv_file = '../csv_files/capture.csv'  # Replace with your CSV file path
    main(image_path, csv_file)
