#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Warning:
#  This is my first dive into Python. There is much room for improvement. :)
#  $HeadURL: https://svn.lipflip.org/svn/dictcc-dictionary/input2xml.py $
#  $Id: input2xml.py 14 2008-03-15 17:03:06Z philipp $
#  Philipp Brauner  - lipflip.org
#  Wolfgang Reszel - www.tekl.de 

import sys, re, string, codecs,datetime, os, locale

#
# initialize dictionary
dictionary = {}


#
# calculates an index-key and adds the entry to the dictionary
# multiple translations and annotated terms are stored in one entry
# INDEX: term
#	term: [trans1, trans2, tras3]
#   term (umgs.) : [trans4]

def addEntry(word, definition):
	global dictionary;
	
	# prepare index string // remove all kinds of additional descriptions
	index = word
	index = re.sub('(\([^)]+\))', r'',index)
	index = re.sub('(\{[^}]+\})', r'',index)
	index = re.sub('(\[[^]]+\])', r'',index)
	index = re.sub('  ', r' ', index) # remove 
	index = index.strip()   # .lower()

	if len(index)<1:
		raise NameError

	# get entry from dictionary	
	if dictionary.has_key(index):
		entry = dictionary[index]
	else:
		entry = {}

	# add translation to entry 
	if entry.has_key(word):
		entry[word].append(definition)
	else:
		entry[word]=[definition]

	# store entry in dictionary
	dictionary[index] = entry;


def style(text):
	text = re.sub('(\{[^}]+\})', r' <i>\1</i>',text)
	text = re.sub('(\([^)]+\))', r' <span class="s1">\1</span>',text)
	text = re.sub('(\[[^]]+\])', r' <span class="s2">\1</span>',text)
	return text

#
#  renders an entry to XML
def renderEntry(ID, index):
	global dictionary;
	entry = dictionary[index]
	
	# unique entry id
	ID = "id_"+str(ID)
	
	title = index; # duh. that's a bit to simple
		
	# create html entry
	s = '<d:entry id="' + ID + '" d:title="' + title +'" >\n'
	s+= '<d:index d:value="' + index +'"/>\n'

	# add additional index keys: "to go, go"
	# brute force - nicer if we do this earlier
	if index.startswith("to "):
		s+= '<d:index d:value="' + index[3:] +'"/>\n'
	
	# loop through several spellings
	for term in entry.keys():
		sub ='<h1>'+style(term)+'</h1>\n'
		
		sub+="<ul>"
		for element in entry[term]:
			sub+="<li>"+style(element)+"</li>"
		sub+="</ul>"

		s+=sub
	
	s+='</d:entry>\n\n'

	# add english translations
#	for word in translation_en:
#		s = s + word+"<br />\n"
#	s = s+'</d:entry>\n'

	return s

#
# reads a data file and add terms to dictionary
def readFile(fileName):
	global dictionary
	lines=0
	comments=0
	errors=0

	try:
		input = codecs.open(fileName, "r", "cp1252")
	except IOError:
		print '*** File "' + fileName + '" not found or other error.'
		return False
	else:
		print 'Processing "'+fileName+'"'
		for line in input:
			lines=lines+1

			# trow away comments or empty lines
			if (line[0]=="#") or (len(line)<=2):
				comments=comments+1
				continue

			# throw away my email address
			if (re.search('lipflip', line)):
				comments=comments+1
				continue

			# remove incompatible characters
			line = line.replace("<","&lt;")
			line = line.replace(">","&gt;")

			# split entry into english and german part 
			data = line.split("::", 1);
			if len(data)!=2:
				errors = errors+1
				continue

			left = data[0].strip();
			right = data[1].strip();


			# fix quotes
#			left  = re.sub('"([^"]+)"',r'„\1“'.decode("utf-8"), left)  # dt. anführungsstriche
#			right = re.sub('"([^"]+)"',r'“\1”'.decode("utf-8"), right)  # engl. anführungsstriche
			left = left.replace('"', "")
			right = right.replace('"', "")
#			if (left1!=left) or (right1!=right):
#				print "PANIC! " + line
#				raise NameError

			# ok... add to dictionary
			try:
				addEntry(left, right);
			except:
				print "addEntry('%s', '%s') failed!" % (left, right)
				errors =  errors+1
			try:
				addEntry(right, left);
			except:
				print "addEntry('%s', '%s') failed!" % (right, left)
				errors =  errors+1

		input.close
		print("\nRead %s lines with %s comments. Errors: %s" % ( lines, comments, errors) )
		print("%s entries in dictionary. \n" % len(dictionary))
		
		return True


# Generate XML output
def writeFile(fileName):
	global dictionary

	# prepare output
	print 'Generating XML output. This may take some time...'
	output = codecs.open(fileName,"w","utf-8")

	# XML Header
	output.write(u'''<?xml version="1.0" encoding="UTF-8"?>
<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n''')
	
	# front matter
	output.write(u'''
<d:entry id="front_back_matter" d:title="Vorwort">
    <h1>dict.cc Wörterbuch</h1>
    <p>Dieses Wörterbuch stammt aus dem Online-Wörterbuch <a href="http://www.dict.cc">www.dict.cc</a>, das seinerseits auf der Wortliste von <a href="http://dict.tu-chemnitz.de/">dict.tu-chemnitz.de</a>, sowie der Mitarbeit zahlreicher Benutzerinnen und Benutzer von dict.cc basiert.</p>
    	
    <p>Die Werkzeuge zur Erstellung eines Plugins für Dictionary.App/Lexikon wurden von <a href="http://lipflip.org/">Philipp Brauner</a> („Lipflip“) entwickelt und durch die Integration eines ähnlichen Tools von <a href="http://www.tekl.de/">Wolfgang Reszel</a> verbessert.</p>
    <p><h1>Lizenz:</h1>
Nutzungsbedingungen der Übersetzungsdaten von dict.cc<br />
Stand vom 11. Februar 2005<br />
Die Bezeichnung "die Daten" steht für die Inhalte der Datenbank, die auf den Seiten und in den Dateien auf www.dict.cc zur Verfügung gestellt wird, sowie für Auszüge daraus.<br />
<br />
PERSÖNLICHER GEBRAUCH<br />
Die Nutzung der Daten für den persönlichen Gebrauch ist gestattet, solange die Daten nicht weitergegeben oder veröffentlicht werden.<br />
<br />
VERWENDUNG IN COMPUTERPROGRAMMEN<br />
Die Verwendung der Daten in Computerprogrammen ist erlaubt, wenn folgende Bedingungen eingehalten werden:<br />
Programme, die Daten von dict.cc verwenden, müssen der GPL unterliegen.<br />
Das heißt unter anderem, dass der Quellcode des Programms der Allgemeinheit zur Weiterverwendung zur Verfügung gestellt werden muss.<br />
Die Übersetzungsdaten selbst dürfen nicht mit dem Programm mitgeliefert werden, sondern der Benutzer muss aufgefordert werden, die benötigte Datei für den eigenen Gebrauch direkt von dict.cc herunterzuladen. Dadurch wird gewährleistet, dass jeder Nutzer der Daten diese Lizenzbestimmungen gesehen und akzeptiert hat.<br />
Das Programm darf nicht dazu bestimmt oder geeignet sein, die Daten im Internet zu veröffentlichen, auch nicht auszugsweise.<br />
<br />
SONSTIGE VERWENDUNG<br />
Weitere Arten der Verwendung der Daten, insbesondere die Verwendung auf Webseiten, auch auszugsweise, bedürfen einer ausdrücklichen schriftlichen Genehmigung des Betreibers von dict.cc, Ing. Paul Hemetsberger.<br />
Die Verwendung der Daten im Zusammenhang mit Suchmaschinen-Optimierungstaktiken oder Spamming in jeglicher Form ist strengstens untersagt.<br />
<br />
WEITERE BESTIMMUNGEN<br />
Sämtliche Aspekte bezüglich der Übersetzungsdaten von dict.cc, die in diesen Bestimmungen nicht eindeutig behandelt sind, bedürfen einer schriftlichen Klärung vor einer eventuellen Verwendung. Bei Verstößen gegen diese Bedingungen behält sich der Betreiber von dict.cc rechtliche Schritte vor. Der Gerichtsstand ist Wien. Es gilt materielles österreichisches Recht.<br /></p>
<p><small>Stand: %s / $Rev: 14 $</small></p>
</d:entry>
''' % (str(datetime.date.today()) )  )

	
	# process each dictionary term
	count = 0
	for term in dictionary.keys():
		count = count + 1
		output.write(renderEntry(count, term))
#		if count>2000:
#			break

	
	# Finish up
	output.write(u'''</d:dictionary>\n''');
	output.close
	print ("Wrote %s entries to '%s'" % (count, fileName) )

# main()
print("dict.cc to Dictionary.app XML Converter - $Id: input2xml.py 14 2008-03-15 17:03:06Z philipp $")
print("    Paul Hemetsberger  -  dict.cc")
print("    Philipp M. Brauner -  lipflip.org")
print("    Wolfgang Reszel    -  www.tekl.de");
print("    licensed under the GLP")
print("    http://lipflip.org/articles/dictcc-dictionary-plugin")

# enable printing of unicode strings without using .encode() millions of times
print("Switching sys.stdout to utf-8...")
sys.stdout = codecs.getwriter("utf-8")(sys.stdout);

if readFile("input.txt"):
	writeFile("temporary.xml");
else:
	print 'Error!'
	print 'No data to process. You need to get a translation database'
	print 'from "http://www1.dict.cc/translation_file_request.php".'
	print 'Rename the file to "input.txt" and start over.'
	sys.exit(1);
