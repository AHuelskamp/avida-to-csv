"""
Usage:
    python3 thisFile.py fileA.spop [fileB.dat ... fileN.spop]

Takes all avida style files and throws them into a json file for easier processing. 
This is largely based off project 1 in CSE 480 

The avida files are odd in that they have a multiline header describing the columns, 
a blank line, and then the data. 

The names for the json fields are made from concatenating the columIDs together. 

If a line is missing columns, (in some .spop files where things are "dead") it
is assumed that the missing fields are from the end.
"""

import re 
import csv 
import json 
import sys 
import argparse 
import os
import string 



#set up parser
commandParser = argparse.ArgumentParser(description="A list of avida files to convert to json") 
commandParser.add_argument('files', metavar="FILE", type=str, nargs="+", 
                        help="files to convert")
args = commandParser.parse_args()


#set up eprint function 
#should be replaced by logger soon 
def eprint(message,newline=True):
    sys.stderr.write(message)
    if newline: sys.stderr.write("\n")

"""
for file in args.files
    convert it. 
    write it. 
"""


for fileName in args.files: 
    #Check that file even exists 
    if not os.path.isfile(fileName):
        #in the future, I want to throw this into a logger 
        eprint("{} could not be found".format(fileName))
        continue 

    #open file and generate Header (colNames) 
    #This assumes that all spop files have the same header
    #If 2 .spop files have slightly different column names
    #(even if they have the same data) they will not be the same json file
    
    headers=[]
    with open(fileName, "r") as f: 
        while True:
            #read until out of header lines 
            nextLine=f.readline().strip()
            if len(nextLine)==0 or "#" not in nextLine: 
                break 
            else: 
                headers.append(nextLine)

    # names are just camelCase Concatenations
    # of numbered lines like below 
    # '# 1: field description 1' 
    # '# 2: field description 2' 
    # ... 
    # '# N: field description N' 
    #
    # unless a format line is there 
    # in spop files format lines look like this: 
    # '#format field1 fileld2 ... fieldN'

    jsonHeaders=[]
    for line in headers: 
        #match starts from beginning of line (unlike search) 
        if re.match("#format",line):
            fields=line.split(" ")
            jsonHeaders=fields[1:]
            break

        elif re.match("# +[0-9]+:",line): 
            line=line.replace(re.match("# +[0-9]+:",line).group(),"").strip()
            line=string.capwords(line)
            line=line[0].lower()+line[1:]
            fieldHeader="".join([ x for x in line if x.isalpha()])
            jsonHeaders.append(fieldHeader)
    
    #then, read in the rest of the file and 
    #dump it into a jsonFile

    jsonIntermediate=[]
    
    with open(fileName, "r") as f:
        for line in f: 
            line=line.strip()

            #ignoreHeaders
            if len(line)==0 or "#" in line:
                continue 
            
            fields=line.split(" ")
            jsonIntermediate.append(dict(zip(jsonHeaders,fields)))

    
    with open(fileName+".json",'w') as outFile:
        json.dump(jsonIntermediate,outFile)



