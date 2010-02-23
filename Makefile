#
# Makefile
#
# $Id: Makefile 13 2008-03-15 14:52:33Z philipp $
#

###########################

# You need to edit these values.

DICT_NAME		=	"dict.cc Deutsch-Englisch Dictionary"
DICT_SRC_PATH	=	temporary.xml
CSS_PATH		=	dictcc.css
PMDOC_NAME      =   dictcc.pmdoc
PLIST_PATH		=	dictcc.plist
DATE            =   `date +"%Y-%m-%d"`

DICT_BUILD_OPTS		=
# Suppress adding supplementary key.
# DICT_BUILD_OPTS		=	-s 0	# Suppress adding supplementary key.

###########################

# The DICT_BUILD_TOOL_DIR value is used also in "build_dict.sh" script.
# You need to set it when you invoke the script directly.

DICT_BUILD_TOOL_DIR	=	"/Developer/Extras/Dictionary Development Kit"
DICT_BUILD_TOOL_BIN	=	"$(DICT_BUILD_TOOL_DIR)/bin"

###########################

DICT_DEV_KIT_OBJ_DIR	=	./objects
export	DICT_DEV_KIT_OBJ_DIR

DESTINATION_FOLDER	=	~/Library/Dictionaries
RM			=	/bin/rm

###########################

all:
	@/usr/bin/python input2xml.py
	@"$(DICT_BUILD_TOOL_BIN)/build_dict.sh" $(DICT_BUILD_OPTS) $(DICT_NAME) $(DICT_SRC_PATH) $(CSS_PATH) $(PLIST_PATH)
	echo "Done."
	echo "removing xml"
	$(RM) -f $(DICT_SRC_PATH)
	@echo "Use 'make install' to install the dictionary or 'make package' to create the Install Package."
	
package:
	@echo "- Creating Install Package."
	@/Developer/Applications/Utilities/PackageMaker.app/Contents/MacOS/PackageMaker -d $(PMDOC_NAME) -o $(DICT_NAME)_$(DATE).pkg
	@echo "- Zipping Install Package."
	@zip $(DICT_NAME)_$(DATE).zip -9 -o $(DICT_NAME)_$(DATE).pkg 
	@echo "Done."
	@echo "Execute '$(DICT_NAME) $(DATE).pkg' to install the dictionary."


install:
	echo "Installing into $(DESTINATION_FOLDER)".
	mkdir -p $(DESTINATION_FOLDER)
	ditto --noextattr --norsrc $(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary  $(DESTINATION_FOLDER)/$(DICT_NAME).dictionary
	touch $(DESTINATION_FOLDER)
	echo "Done."
	echo "To test the new dictionary, try Dictionary.app."

clean:
	$(RM) -rf $(DICT_DEV_KIT_OBJ_DIR)
	$(RM) -f $(DICT_SRC_PATH)
