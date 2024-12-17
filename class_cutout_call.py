from class_cutout import ImageCutoutSaver as ics

# Example usage

img_path = 'image_files/captured_test_clean.jpg'  # Replace with your actual image path

# Example coordinates
coordinates = [((279, 110), (279, 110)), ((128, 90), (359, 246)),
               ((209, 193), (401, 385)), ((134, 219), (353, 391)),
               ((120, 115), (384, 286)), ((339, 81), (570, 260))]

# Create an instance of ImageCutoutSaver
cutout_saver = ics(img_path)

# Save the cutouts
cutout_saver.save_cutouts(coordinates)