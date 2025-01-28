import sys
import re  # For regex support
import os
import string
import tkinter as tk
from tkinter import ttk, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re  # Added for regex support

def get_database_path():
    if getattr(sys, 'frozen', False):
        # Running as a compiled executable
        base_dir = sys._MEIPASS
    else:
        # Running as a script
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    database_path = os.path.join(base_dir, "database.txt")
    return database_path
    
# ====================
# DICTIONARY SECTION
# ====================
REFERENCE_DICTIONARY = {}  # Initialize as empty; will be loaded from database.txt
REVERSE_DICTIONARY = {}    # Reverse dictionary for decryption

# Define the allowed character set (uppercase letters and numbers)
ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
CHAR_SET_LENGTH = len(ALLOWED_CHARS)

# Function to load the dictionary from database.txt
def load_dictionary():
    global REFERENCE_DICTIONARY, REVERSE_DICTIONARY
    try:
        # Get the directory of the executable
        base_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(base_dir, "database.txt")

        if not os.path.exists(database_path):
            raise FileNotFoundError("The database.txt file was not found.")

        with open(database_path, "r") as file:
            REFERENCE_DICTIONARY = {}
            for line in file:
                line = line.strip()
                if line and ":" in line:
                    key, value = line.split(":", 1)
                    REFERENCE_DICTIONARY[key.strip().lower()] = value.strip().upper()
                else:
                    raise ValueError(f"Invalid line format in database.txt: {line}")

        # Update the reverse dictionary
        REVERSE_DICTIONARY = {v: k for k, v in REFERENCE_DICTIONARY.items()}

    except FileNotFoundError as e:
        messagebox.showwarning("File Not Found", str(e))
        REFERENCE_DICTIONARY = {}  # Use an empty dictionary
        REVERSE_DICTIONARY = {}
    except Exception as e:
        messagebox.showwarning("Error Loading Dictionary", f"An error occurred: {str(e)}")
        REFERENCE_DICTIONARY = {}  # Use an empty dictionary
        REVERSE_DICTIONARY = {}

# Watchdog handler to reload the dictionary when database.txt changes
class DictionaryFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("database.txt"):
            load_dictionary()
            messagebox.showinfo("Dictionary Updated", "The dictionary has been reloaded.")

# Initialize the file watcher
def start_file_watcher():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    observer = Observer()
    event_handler = DictionaryFileHandler()
    observer.schedule(event_handler, path=base_dir, recursive=False)
    observer.start()

# Load the dictionary at startup
load_dictionary()

# Start the file watcher
start_file_watcher()

# =============================================
# ENCRYPTION/DECRYPTION FUNCTIONS
# =============================================
def vigenere_like_encrypt(text, key):
    """Encrypts text using a Vigenère-like cipher, ensuring output is within the allowed character set."""
    key = (key * (len(text) // len(key) + 1))[:len(text)]
    encrypted = []
    for t, k in zip(text, key):
        if t in ALLOWED_CHARS and k.upper() in ALLOWED_CHARS:
            # Calculate the new character position within the allowed set
            t_index = ALLOWED_CHARS.index(t)
            k_index = ALLOWED_CHARS.index(k.upper())
            new_index = (t_index + k_index) % CHAR_SET_LENGTH
            encrypted.append(ALLOWED_CHARS[new_index])
        else:
            # If the character is not in the allowed set, leave it as-is
            encrypted.append(t)
    return ''.join(encrypted)

def vigenere_like_decrypt(text, key):
    """Decrypts text using a Vigenère-like cipher, ensuring output is within the allowed character set."""
    key = (key * (len(text) // len(key) + 1))[:len(text)]
    decrypted = []
    for t, k in zip(text, key):
        if t in ALLOWED_CHARS and k.upper() in ALLOWED_CHARS:
            # Calculate the original character position within the allowed set
            t_index = ALLOWED_CHARS.index(t)
            k_index = ALLOWED_CHARS.index(k.upper())
            new_index = (t_index - k_index) % CHAR_SET_LENGTH
            decrypted.append(ALLOWED_CHARS[new_index])
        else:
            # If the character is not in the allowed set, leave it as-is
            decrypted.append(t)
    return ''.join(decrypted)

# =============================================
# GUI APPLICATION
# =============================================
class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JackRabbit")
        self.root.geometry("380x460")  # Adjusted height to accommodate the new layout

        # Input Text
        self.input_label = ttk.Label(root, text="Input Text:")
        self.input_label.pack(pady=5)
        self.input_text = tk.Text(root, height=5, width=40)  # Reduced width
        self.input_text.pack(pady=5)

        # Configure font after creating input_text
        text_font = ("Arial", 12)
        self.input_text.configure(font=text_font)

        # Password
        self.password_label = ttk.Label(root, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        # Buttons (First Row)
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)

        self.encrypt_button = ttk.Button(self.button_frame, text="Encrypt", command=self.encrypt)
        self.encrypt_button.pack(side=tk.LEFT, padx=5)

        self.decrypt_button = ttk.Button(self.button_frame, text="Decrypt", command=self.decrypt)
        self.decrypt_button.pack(side=tk.LEFT, padx=5)

        # Buttons (Second Row)
        self.button_frame2 = ttk.Frame(root)
        self.button_frame2.pack(pady=10)

        self.copy_button = ttk.Button(self.button_frame2, text="Copy Output", command=self.copy_output)
        self.copy_button.pack(side=tk.LEFT, padx=5)

        self.paste_button = ttk.Button(self.button_frame2, text="Paste Input", command=self.paste_input)
        self.paste_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.button_frame2, text="Clear", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Output Text
        self.output_label = ttk.Label(root, text="Output:")
        self.output_label.pack(pady=5)
        self.output_text = tk.Text(root, height=5, width=40, state="disabled")  # Same height as input
        self.output_text.pack(pady=5)

        # Configure font after creating output_text
        self.output_text.configure(font=text_font)

        # Warning Label
        self.warning_label = tk.Label(root, text="", fg="black", bg="white", anchor="w")
        self.warning_label.pack(pady=10, fill=tk.X)

    def show_warning(self, message, color):
        """Update the warning label with a message and background color."""
        self.warning_label.config(text=message, bg=color)

    def encrypt(self):
        try:
            # Convert input text to lowercase
            text = self.input_text.get("1.0", tk.END).strip().lower()
            password = self.password_entry.get().strip().lower()
            if not text or not password:
                self.show_warning("Input and password are required!", "red")
                return

            # Process the text based on the dictionary
            words = text.split()
            processed_words = []
            missing_words = []

            for word in words:
                # Remove punctuation from the word
                cleaned_word = word.translate(str.maketrans('', '', string.punctuation))
                
                if cleaned_word in REFERENCE_DICTIONARY:
                    # Use the reference code from the dictionary
                    processed_words.append(REFERENCE_DICTIONARY[cleaned_word])
                else:
                    # Highlight missing words and use them as-is
                    processed_words.append(word)
                    if len(cleaned_word) >= 4:  # Only consider words with 4 or more letters
                        missing_words.append(word)

            # Highlight missing words in red (case insensitive)
            self.input_text.tag_configure("missing", foreground="red")
            self.input_text.tag_remove("missing", "1.0", tk.END)

            for word in missing_words:
                # Use regex to find whole words only
                start = "1.0"
                while True:
                    pos = self.input_text.search(r'\m' + re.escape(word) + r'\M', start, stopindex=tk.END, regexp=True, nocase=True)
                    if not pos:
                        break
                    end = f"{pos}+{len(word)}c"
                    self.input_text.tag_add("missing", pos, end)
                    start = end

            # Encrypt the processed text (reference codes + original words)
            processed_text = ' '.join(processed_words).upper()
            encrypted = vigenere_like_encrypt(processed_text, password.upper())

            # Display the result
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", encrypted)
            self.output_text.config(state="disabled")

            # Show warning if there are missing words
            if missing_words:
                self.show_warning("Some words are not in the dictionary. Encryption still completed.", "yellow")
            else:
                self.show_warning("Encryption successful!", "green")

        except Exception as e:
            self.show_warning(f"Error: {str(e)}", "red")

    def decrypt(self):
        try:
            # Convert input text to uppercase
            encrypted_text = self.input_text.get("1.0", tk.END).strip().upper()
            password = self.password_entry.get().strip().upper()
            if not encrypted_text or not password:
                self.show_warning("Input and password are required!", "red")
                return

            # Decrypt the text
            decrypted = vigenere_like_decrypt(encrypted_text, password)

            # Convert reference codes back to original words
            words = decrypted.split()
            processed_words = []

            for word in words:
                if word in REVERSE_DICTIONARY:
                    # Replace reference codes with their original words
                    processed_words.append(REVERSE_DICTIONARY[word].lower())
                else:
                    # Keep words as-is if not in the reverse dictionary
                    processed_words.append(word.lower())

            # Combine processed words into a single string
            result = ' '.join(processed_words)

            # Display the result
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            self.output_text.config(state="disabled")
            self.show_warning("Decryption successful!", "green")
        except Exception as e:
            self.show_warning(f"Error: {str(e)}", "red")

    def copy_output(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get("1.0", tk.END).strip())
        self.show_warning("Output copied to clipboard!", "green")

    def paste_input(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", clipboard_text)
        except tk.TclError:
            self.show_warning("No text in clipboard!", "red")

    def clear_fields(self):
        self.input_text.delete("1.0", tk.END)
        self.password_entry.delete(0, tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")
        self.show_warning("", "white")

# Main Application Loop
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()