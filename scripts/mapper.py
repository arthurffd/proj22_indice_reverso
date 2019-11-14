#!/usr/bin/env python3

# Mapper script for words reversed index

from sys import stdin
import re
import os
#import random

for line in stdin:
# Get the file path
    # get full file name from OS
    doc_id = os.environ["map_input_file"]
    
    #doc_id = "path" + "/" + str(random.randrange(5)) # for local test purposes

    # Extract the file name from the path
    doc_id = re.findall(r'\w+', doc_id)[-1]
    
    # Extract an array of all the words inside the document, breaking by spaces
    words = re.findall(r'\w+', line.strip())
    
    # Map the words. Stdout containing: <word> <tab> <doc_id>: 1 
    # Example: "someword  doc001: 1"
    for word in words:
        print("%s\t%s:1" % (word.lower(), doc_id))
