# JackRabbit
light encryption for ham radio, in particular JS8call. primary goal is smallest possible payload.

🛠️ Feature Overview
This application provides a GUI-based encryption and decryption tool using a Vigenère-like cipher and a customizable reference dictionary!

✅ Dictionary Management

Loads a custom dictionary (database.txt) for encryption mappings.
Watches database.txt for changes and reloads automatically using Watchdog.

✅ Encryption & Decryption

Encryption:
Replaces words with mapped codes from the dictionary.
Encrypts using a Vigenère-like cipher over allowed characters (A-Z and 0-9).
Highlights words missing from the dictionary in the input text.
Decryption:
Converts ciphered text back to dictionary-defined words.


/

/

/
this simple program is tailor made for the shortest possible payload (for JS8call) but still offer a little bit of privacy.
not AES256 military grade like my other release, but just enought to prevent normal people from decoding it.

source code in the format of a .py is provided with a pre-made .exe for quick running.
the dictionary is already inside, but it is incomplete. more work is needed.
