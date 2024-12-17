__author__ = 'mkv-aql'

from class_easyOCR_V1 import OCRProcessor  # Import the class from the file where it's defined

# Example usage
if __name__ == "__main__":
    # Path to your image
    image_path = 'image_files/Briefkaesten.jpg'  # Replace with your image file

    # Initialize the OCRProcessor class
    ocr_processor = OCRProcessor(language='de', gpu=True, recog_network='latin_g2')

    # Perform OCR on the image
    df_results = ocr_processor.ocr(image_path)

    # Print the results
    print(df_results)

    # Save the results to a CSV (file name without extension)
    ocr_processor.save_to_csv(df_results, image_path.split('.')[0])
