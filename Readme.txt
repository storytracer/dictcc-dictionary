Download packaged plugin here:
https://sourceforge.net/projects/dictccplugin/files/dict.cc%20Deutsch-Englisch%20Dictionary.zip/download
(Database snapshot made on 2010-02-23)

---------------------------------------------------------------------------

input2xml.py dict.cc to Apple Dictionary Plugin Script ($Rev: 15 $)
$Date: 2008-03-15 18:36:46 +0100 (Sa, 15 MÃƒÂ¤r 2008) $
by Philipp Brauner/Lipflip 2008, licensed under the GLP
   lipflip@lipflip.org
   http://lipflip.org/articles/dictcc-dictionary-plugin
Partially by Wolfgang Reszel
   http://web.mac.com/tekl/deutsch/WšrterbŸcher.html
Changes in README by Sebastian Mastorovic, February 2010

Warning:
  This is my first dive into Python. There is much room for improvement. :)

Installation:
1. Unzip dictcc-dictionary-distrib.zip. You already did this. Hooray!

2. Download and install the OS X Developer Tools from Apple.com.
   You'll need to join the Apple Developer Connection to do this (there's a
   free membership).

3. Download dict.cc's database. You can find the database here,
   please read the licensing conditions carefully:
   http://www1.dict.cc/translation_file_request.php

   Choose version "DE -> EN (Elcombri / old format, cp1252)"
   and download it. Rename dict.cc's database files to "input.txt" 
   and place it into the dictcc-dictionary-distrib directory.

4. Open a Terminal and "cd" to the dictcc-dictionary-distrib directory.

5. Launch the Makefile:
   user$ make

6. After some minutes the dictionary can be installed:
   user$ make install

   It will be placed into /Users/$username/Library/Dictionaries/ and fills
   about 300MB of disk space.

8. Start/restart Dictionary.App.

   Have fun!  Lipflip