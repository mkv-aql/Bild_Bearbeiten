from class_highlight import RectangleSelector  as rs
import cv2

# Load an image or create a blank one
image = cv2.imread('image_files/captured_clean.jpg')  # Replace with your image path
selector = rs(image)
highlighted_areas = selector.run()
print("Highlighted areas:", highlighted_areas)


