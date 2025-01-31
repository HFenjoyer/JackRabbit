# JackRabbit

🛠️ This application provides a GUI-based encryption and decryption tool using a Vigenère-like cipher and a customizable reference dictionary!

![image alt](https://github.com/HFenjoyer/JackRabbit/blob/main/example.jpg?raw=true)

basically this is using a dictionary reference table to replace words with simple 2-3 characters code. 
this make for a One Time Pad like encryption. it isnt FED proof, but plenty good for joking around.
without the dictionary it is impossible to crack. for example : A3 D2 H5
good luck trying to find what it means without my personnal look-up table.
this is the trick! not only does it provide pretty good protection, but i have formated the output to be suitable for Js8call (only UPPERCASE or numbers) 

my goal was first to make the payload text smallest possible.
no more 50characters to send "hello how are you"

JS8call and propagation can be pretty bad at receiving and its hell sending everything again and again until the other side has it correctly. now using this JACKRABBIT unique formating and reference table the text are not only shorter then normal, but it create pretty good security!


=

Dictionary Manager:
it is to add words into, or create your own dictionary of references. it is checking to make sure and only add unique words and to generate unique reference codes.


![image alt](https://github.com/HFenjoyer/JackRabbit/blob/main/manager%20example.jpg?raw=true)



Shuffler:
simply mix the reference codes. it is to create your own unique set of references. so even if you have the same word list as everybody it is still unique and un-crackable.
it will first ask you for the location of the existing dictionary, then for the location and name of the new-shuffled one. 

![image alt](https://github.com/HFenjoyer/JackRabbit/blob/main/shuffler%20example.jpg?raw=true)

=

source code in the format of a .py is provided with a pre-made .exe for quick running.

i provide a special program to add words into the dictionary, and another to scamble the references codes.

=

some tips and tricks:

-when sending numbers =< 2characters, put some zeroes in front. this prevent mis-decode 
for example 23, write it as 023. for 2 write it as 002

-scramble your own dictionary!

-missing words? ADD THEM YOURSELF

-dont trust the .exe? compile it youself!
install python, and the module required (use notepad++ to open the .py and check them).
use the command: pyinstaller --onefile --noconsole --icon=icon.ico --add-data "database.txt;." JackRabbitv3.py
this is the command for the main file. for the other scripts you must change the command slightly. HAVE FUN

=

=

=

"some people" will be seething, Enjoy while it last!
