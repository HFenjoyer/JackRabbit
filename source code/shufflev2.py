import random
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to shuffle the values in the dictionary
def shuffle_dictionary(file_path):
    try:
        # Read the original dictionary
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Extract keys and values
        keys = []
        values = []
        for line in lines:
            # Split only on the first ": " to handle special characters in values
            key, value = line.strip().split(': ', 1)
            keys.append(key)
            values.append(value)

        # Shuffle the keys (reference codes) independently
        random.shuffle(keys)

        # Shuffle the values (words) independently
        random.shuffle(values)

        # Create the shuffled dictionary by pairing shuffled keys and values
        shuffled_dict = {keys[i]: values[i] for i in range(len(keys))}

        return shuffled_dict
    except Exception as e:
        messagebox.showerror("Error", f"Failed to shuffle dictionary: {e}")
        return None

# Function to save the shuffled dictionary to a new file
def save_shuffled_dict(shuffled_dict, output_path):
    try:
        with open(output_path, 'w') as file:
            for key, value in shuffled_dict.items():
                file.write(f"{key}: {value}\n")
        messagebox.showinfo("Success", f"Shuffled dictionary saved to {output_path}!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save shuffled dictionary: {e}")

# Function to handle the shuffle button click
def shuffle_button_click():
    input_file = filedialog.askopenfilename(title="Select Dictionary File", filetypes=[("Text Files", "*.txt")])
    if not input_file:
        return

    shuffled_dict = shuffle_dictionary(input_file)
    if shuffled_dict:
        output_file = filedialog.asksaveasfilename(title="Save Shuffled Dictionary", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if output_file:
            save_shuffled_dict(shuffled_dict, output_file)

# Create the main application window
root = tk.Tk()
root.title("Dictionary Shuffler v2")
root.geometry("400x200")
root.resizable(False, False)

# Add a label
label = tk.Label(root, text="Welcome to Dictionary Shuffler!", font=("Arial", 14))
label.pack(pady=20)

# Add the shuffle button
shuffle_button = tk.Button(root, text="Shuffle", font=("Arial", 12), bg="blue", fg="white", command=shuffle_button_click)
shuffle_button.pack(pady=20, ipadx=10, ipady=5)

# Run the application
root.mainloop()