__author__ = 'mkv-aql'

# another_script.py
import tkinter as tk
from class_entry_input_2 import CsvEditor  # Import the CsvEditor class

# Create the root window for Tkinter
root = tk.Tk()

# Path to the CSV file you want to load
csv_file_path = "csv_files/20241004_170906.csv"

# Instantiate the CsvEditor class with the CSV file path
app = CsvEditor(root, csv_file_path)

# Run the Tkinter main loop
root.mainloop()
