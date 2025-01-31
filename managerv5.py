import random
import string
import os
import tkinter as tk
import re
import time
from threading import Thread

# Reserved reference codes (common 2-letter English words)
RESERVED_CODES = {
    "WE", "SO", "BE", "IT", "DO", "AT", "IN", "OK", "TV", "PC", "FM", "AI", "AP",
    "IQ", "DJ", "CD", "ID", "HI", "IF", "IS", "IR", "ON", "BY", "TO", "OF", "OR",
    "AN", "AS", "MY", "UP", "HE", "GO", "NO", "US", "AM", "ME"
}

# Special characters rules
SPECIAL_CHARACTERS = {
    "$": "front",
    "%": "front",
    "@": "end",
    "#": "end",
    "&": "end",
}

# Allowed characters for reference codes
ALLOWED_CHARS = string.ascii_uppercase + string.digits
CHAR_SET_LENGTH = len(ALLOWED_CHARS)

# Function to calculate maximum unique codes
def calculate_max_codes():
    base_codes = CHAR_SET_LENGTH ** 2  # Two-character base codes
    special_codes = len(SPECIAL_CHARACTERS) * base_codes
    return special_codes - len(RESERVED_CODES)

# Function to load the dictionary
def load_dictionary():
    if not os.path.exists("database.txt"):
        with open("database.txt", "w") as file:
            file.write("")
        return {}
    dictionary = {}
    with open("database.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:
                word, code = line.split(": ")
                dictionary[word] = code
    return dictionary

# Function to save the dictionary
def save_dictionary(dictionary):
    with open("database.txt", "w") as file:
        for word, code in dictionary.items():
            file.write(f"{word}: {code}\n")

# Function to generate a unique reference code
def generate_reference_code(dictionary, used_special_chars):
    code_length = 2
    base_codes = ALLOWED_CHARS

    while True:
        if len(dictionary) >= calculate_max_codes():
            raise Exception("Maximum dictionary capacity reached. Cannot generate new reference codes.")

        # Cycle through special characters to balance usage
        for special_character, position in SPECIAL_CHARACTERS.items():
            # Generate base code
            base_code = ''.join(random.choice(base_codes) for _ in range(code_length))

            # Apply special character
            if position == "front":
                reference_code = special_character + base_code
            else:
                reference_code = base_code + special_character

            # Ensure uniqueness
            if reference_code not in dictionary.values() and reference_code not in RESERVED_CODES:
                return reference_code

# Function to add a word
def add_word(word):
    try:
        # Validate the word
        if not word.isalpha() or len(word) < 4:
            raise ValueError(f"Word '{word}' is invalid. Must be alphabetic and at least 4 characters long.")

        # Check for duplicates
        if word in dictionary:
            raise ValueError(f"Word '{word}' already exists in the dictionary.")

        # Check dictionary capacity
        if len(dictionary) >= calculate_max_codes():
            raise Exception("Dictionary is at maximum capacity. Cannot add new words.")

        # Generate a unique reference code
        reference_code = generate_reference_code(dictionary, SPECIAL_CHARACTERS)
        dictionary[word] = reference_code
        save_dictionary(dictionary)
        update_display()

        # Success message
        status_area.config(text=f"Success: '{word}' added with code '{reference_code}'.", fg="green")

    except Exception as e:
        # Gracefully display error messages in the status area
        status_area.config(text=f"Error: {str(e)}", fg="red")

# Function to process a paragraph of text
def process_paragraph():
    paragraph = paragraph_entry.get("1.0", tk.END).strip()
    words = re.findall(r'\b[a-zA-Z]{4,}\b', paragraph)  # Extract words with 4 or more letters

    if not words:
        status_area.config(text="Error: No valid words found in the text.", fg="red")
        return

    status_area.config(text=f"Processing {len(words)} words...", fg="black")
    root.update_idletasks()  # Update the GUI

    for word in words:
        add_word(word.lower())
        time.sleep(0.1)  # Add a slight delay to prevent lag/crash
        root.update_idletasks()  # Update the GUI after each word

    status_area.config(text="Processing complete.", fg="green")

# Function to update the display of the dictionary
def update_display():
    dictionary_display.delete(1.0, tk.END)
    for word, code in dictionary.items():
        dictionary_display.insert(tk.END, f"{word}: {code}\n")

# Function to clear the input text window
def clear_input():
    paragraph_entry.delete("1.0", tk.END)
    status_area.config(text="Input cleared.", fg="blue")

# GUI Setup
root = tk.Tk()
root.title("Dictionary Manager v5")

# Create and place the widgets
tk.Label(root, text="Paste a paragraph of text:").grid(row=0, column=0, padx=10, pady=10)
paragraph_entry = tk.Text(root, width=50, height=10)
paragraph_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

process_button = tk.Button(root, text="Process Paragraph", command=lambda: Thread(target=process_paragraph).start())
process_button.grid(row=1, column=1, padx=10, pady=10)

# Add the Clear button
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.grid(row=1, column=2, padx=10, pady=10)

# Status area for messages
status_area = tk.Label(root, text="", fg="black", wraplength=300)
status_area.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

tk.Label(root, text="Dictionary:").grid(row=3, column=0, padx=10, pady=10)
dictionary_display = tk.Text(root, width=50, height=15)
dictionary_display.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

# Initialize the dictionary display
dictionary = load_dictionary()
update_display()

# Start the main loop
root.mainloop()