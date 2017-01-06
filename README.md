## GCTranslator
Graphics Chipers Translator is a program for translating graphics chipers in plain text. It finds images on the incoming image and tries to interpret them as characters by comparing with the base of characters.
# DEMO 
https://nbviewer.jupyter.org/github/DentonJC/gctranslator/blob/master/Project.ipynb
# DATABASE
Of the box:
1 HVD
2 BRAILLE
3 DAEDRIC 
4 SPACE INVADERS 
5 HYMMNOS 
6 PUZZLE CODE 
7 FLAGGEN-CODE
8 DAGGER-CODE 
9 GARGISH-CODE 
10 FUTURAMA-CODE 
11 Dancing Man Code
12 UTOPIAN 
13 KRYPTON
14 Winkeralphabet
15 MORSECODE 
16 Quadoo Alphabet 
17 KLINGONISCH 
18 GNOMMISH
19 MATORAN 
20 TENCTONESE 
21 SUNUZ 
22 MAZE
23 VISITOR
24 TOMTOM 
25 MUTE
26 FINGERALPHABET
27 INTERGALA 
28 FAKOO
29 HOBRUNES
30 RUNES

Users can add their databases by placing them in a folder /examples. 
Database template: folder called "base name" which contains the images with one character each and named like symbol name.
# REQUIREMENTS
Packages:
python2 or python3
Python libraries:
numpy
pillow
Install on Ubuntu:
/# apt-get install python
/# apt-get install python-pip
/# pip install numpy pillow
# INSTALLATION
Program is not required to build or install.
# USER MANUAL
The program first displays the series of dialog boxes.
1) Enter the image addressEnter address of the code that you want to translate.
2) Enter the path to folder with samplesEnter address of the folder with samples or leave empty to use standart database.
3) Enter the distance between lettersPick the value at which the result you want. If the value is too small the program will cut the not solid characters apart. If the value is too high, the program will interpret several symbols as one in line.
4) Enter the distance between linesPick the value at which the result you want. If the value is too small the program will cut the not solid characters apart. If the value is too high, the program will interpret several symbols as one in row.
5) Clear examples after the previous preprocessing?Answer yes if you are using your own database, and not if the standard.
# TESTS
With distance between letters ([distance] variable in generator) = 20 and empty_threshold = 20 incorrectly recognized:
27 r,w
16 h
22 z
13 y,o
With distance between letters ([distance] variable in generator) = 65 and empty_threshold = 65 - 100% correct
empty_lines_threshold = 70 needed for several lines with only braille chiper (2/)
# LINKS
https://en.wikipedia.org/wiki/Cross-correlation#Normalized_cross-correlation - comparison algorithm
http://www.mygeotools.de/ - database (offline 01/01/2017)
