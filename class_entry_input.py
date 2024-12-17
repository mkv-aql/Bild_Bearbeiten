import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class CsvEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Editor")

        self.csv_data = None

        # Create UI components
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.load_button = tk.Button(self.frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.frame, text="Save CSV", command=self.save_csv)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.frame, text="Add Name", command=self.add_name)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.name_label = tk.Label(self.frame, text="Enter Name:")
        self.name_label.pack(side=tk.LEFT, padx=5)

        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        self.listbox = tk.Listbox(self.root, width=50, height=15)
        self.listbox.pack(pady=10)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.csv_data = pd.read_csv(file_path)
                self.listbox.delete(0, tk.END)  # Clear previous entries
                for index, row in self.csv_data.iterrows():
                    # Show index and current names
                    self.listbox.insert(tk.END, f"{index}: {row['Namen']}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV file: {e}")

    def save_csv(self):
        if self.csv_data is not None:
            # Save the updated DataFrame back to CSV
            self.csv_data.to_csv('updated_file.csv', index=False)
            messagebox.showinfo("Success", "CSV file updated successfully.")

    def add_name(self):
        if self.csv_data is not None:
            new_name = self.name_entry.get()
            if not new_name:
                messagebox.showwarning("Warning", "Please enter a name before adding.")
                return

            # Add the new name to the DataFrame
            new_index = len(self.csv_data)  # Get the next index
            self.csv_data.loc[new_index] = [None, None, new_name]  # Add a new row

            # Clear the entry and refresh the listbox
            self.name_entry.delete(0, tk.END)
            self.listbox.delete(0, tk.END)
            for index, row in self.csv_data.iterrows():
                self.listbox.insert(tk.END, f"{index}: {row['Namen']}")

            messagebox.showinfo("Success", f"Added new name: {new_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CsvEditor(root)
    root.mainloop()
