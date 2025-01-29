import sys
import re  # For regex support
import os
import string
import tkinter as tk
from tkinter import ttk, messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ====================
# DICTIONARY SECTION
# ====================
REFERENCE_DICTIONARY = {}  # Initialize as empty; will be loaded from database.txt
REVERSE_DICTIONARY = {}    # Reverse dictionary for decryption

# Define the allowed character set (uppercase letters, numbers, and special characters)
ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
SPECIAL_CHARS = ['@', '$', '#', '%', '&']  # Added special characters
CHAR_SET_LENGTH = len(ALLOWED_CHARS)

# Function to load the dictionary from database.txt
def load_dictionary():
    global REFERENCE_DICTIONARY, REVERSE_DICTIONARY
    try:
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
                    REFERENCE_DICTIONARY[key.strip()] = value.strip()
                else:
                    raise ValueError(f"Invalid line format in database.txt: {line}")

        REVERSE_DICTIONARY = {v: k for k, v in REFERENCE_DICTIONARY.items()}

    except FileNotFoundError as e:
        messagebox.showwarning("File Not Found", str(e))
        REFERENCE_DICTIONARY = {}
        REVERSE_DICTIONARY = {}
    except Exception as e:
        messagebox.showwarning("Error Loading Dictionary", f"An error occurred: {str(e)}")
        REFERENCE_DICTIONARY = {}
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
# HIGHLIGHTING FUNCTION
# =============================================
def highlight_missing_words(text_widget, missing_words):
    """Highlights words not in the dictionary within the given text widget."""
    text_widget.tag_configure("missing", foreground="red")
    text_widget.tag_remove("missing", "1.0", tk.END)

    for word in missing_words:
        start = "1.0"
        while True:
            pos = text_widget.search(re.escape(word), start, stopindex=tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(word)}c"
            text_widget.tag_add("missing", pos, end)
            start = end

# =============================================
# ENCRYPTION/DECRYPTION FUNCTIONS
# =============================================
def vigenere_like_encrypt(text, key):
    """Encrypts text using a Vigenère-like cipher, ensuring output is within the allowed character set."""
    key = (key * (len(text) // len(key) + 1))[:len(text)]
    encrypted = []
    for t, k in zip(text, key):
        if t in ALLOWED_CHARS and k.upper() in ALLOWED_CHARS:
            t_index = ALLOWED_CHARS.index(t)
            k_index = ALLOWED_CHARS.index(k.upper())
            new_index = (t_index + k_index) % CHAR_SET_LENGTH
            encrypted.append(ALLOWED_CHARS[new_index])
        else:
            encrypted.append(t)
    return ''.join(encrypted)

def vigenere_like_decrypt(text, key):
    """Decrypts text using a Vigenère-like cipher, ensuring output is within the allowed character set."""
    key = (key * (len(text) // len(key) + 1))[:len(text)]
    decrypted = []
    for t, k in zip(text, key):
        if t in ALLOWED_CHARS and k.upper() in ALLOWED_CHARS:
            t_index = ALLOWED_CHARS.index(t)
            k_index = ALLOWED_CHARS.index(k.upper())
            new_index = (t_index - k_index) % CHAR_SET_LENGTH
            decrypted.append(ALLOWED_CHARS[new_index])
        else:
            decrypted.append(t)
    return ''.join(decrypted)

# =============================================
# GUI APPLICATION
# =============================================
class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JackRabbit v3")
        self.root.geometry("380x460")

        # Input Text
        self.input_label = ttk.Label(root, text="Input Text:")
        self.input_label.pack(pady=5)
        self.input_text = tk.Text(root, height=5, width=40)
        self.input_text.pack(pady=5)
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
        self.output_text = tk.Text(root, height=5, width=40, state="disabled")
        self.output_text.pack(pady=5)
        self.output_text.configure(font=text_font)

        # Warning Label
        self.warning_label = tk.Label(root, text="", fg="black", bg="white", anchor="w")
        self.warning_label.pack(pady=10, fill=tk.X)

    def show_warning(self, message, color):
        """Update the warning label with a message and background color."""
        self.warning_label.config(text=message, bg=color)

    def encrypt(self):
        try:
            text = self.input_text.get("1.0", tk.END).strip().lower()
            password = self.password_entry.get().strip().lower()
            if not text or not password:
                self.show_warning("Input and password are required!", "red")
                return

            words = text.split()
            processed_words = []
            missing_words = []

            for word in words:
                cleaned_word = word.translate(str.maketrans('', '', string.punctuation))
                if cleaned_word in REFERENCE_DICTIONARY:
                    processed_words.append(REFERENCE_DICTIONARY[cleaned_word])
                else:
                    processed_words.append(word)
                    if len(cleaned_word) >= 4:
                        missing_words.append(word)

            highlight_missing_words(self.input_text, missing_words)

            processed_text = ' '.join(processed_words).upper()
            encrypted = vigenere_like_encrypt(processed_text, password.upper())

            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", encrypted)
            self.output_text.config(state="disabled")

            if missing_words:
                self.show_warning("Some words are not in the dictionary. Encryption still completed.", "yellow")
            else:
                self.show_warning("Encryption successful!", "green")

        except Exception as e:
            self.show_warning(f"Error: {str(e)}", "red")

    def decrypt(self):
        try:
            encrypted_text = self.input_text.get("1.0", tk.END).strip().upper()
            password = self.password_entry.get().strip().upper()
            if not encrypted_text or not password:
                self.show_warning("Input and password are required!", "red")
                return

            decrypted = vigenere_like_decrypt(encrypted_text, password)

            words = decrypted.split()
            processed_words = []

            for word in words:
                if word in REVERSE_DICTIONARY:
                    processed_words.append(REVERSE_DICTIONARY[word].lower())
                else:
                    processed_words.append(word.lower())

            result = ' '.join(processed_words)

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
