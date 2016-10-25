"""
Usage:
    python3 thisFile.py fileA.spop [fileB.dat ... fileN.spop]

Takes all avida style files and throws them into a json file for easier processing.
This is largely based off project 1 in CSE 480 FS2016

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
import logging


#set up parser
commandParser = argparse.ArgumentParser(description="A list of avida files to convert to json")
commandParser.add_argument('files', metavar="FILE", type=str, nargs="+",
                        help="files to convert")
args = commandParser.parse_args()

#set up logging
FORMAT='%(asctime)-15s %(message)s'

#this will be set later by a command line arg
LEVEL="DEBUG"

logging.basicConfig(format=FORMAT,level=LEVEL)


class Converter():

    def __init__(self,fileName):
        self.fileName=fileName
        self.headers=list()
        self.intermediate=list()

        self._checkValidFile()
        self._setJsonName()

        self._generateHeader()
        self._generateIntermediate()

    def _setJsonName(self):
        self.jsonName=self.fileName+".json"

    def _checkValidFile(self):

        #Check that file even exists
        #technically race conditions exist but those are, hopefully, rare.
        if not os.path.isfile(fileName):
            message="File {} could not be found".format(fileName)
            logging.warn(message)
            self.valid=False

            #check that the file isn't already a json file
        elif re.search("\.json",fileName):
            message="File {} is already a json file. Not converting.".format(fileName)
            logging.warn(message)
            self.valid=False

        else:
            message="File {} is found and valid.".format(fileName)
            logging.info(message)
            self.valid=True

    def _generateHeader(self):
        if not self.valid:
            return -1

        #open file and generate Header (colNames)
        #This assumes that all spop files have the same header
        #If 2 .spop files have slightly different column names
        #(even if they have the same data) they will not be the same json file

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

        firstLines=[]
        with open(self.fileName, "r") as f:
            #read until out of header lines
            while True:
                nextLine=f.readline().strip()
                if len(nextLine)==0 or "#" not in nextLine:
                    break
                else:
                    firstLines.append(nextLine)

        #generate the fields from either the first line of the file
        #or a camel case concatentation of the numbered fields.
        self.header=[]
        for line in firstLines:

            #match starts from beginning of line (unlike search)
            #There've been some files that start this way.
            #We will use the #format lines for the headers
            #over getting things from the numbered lines.
            if re.match("#format",line):
                fields=line.split(" ")
                self.header=fields[1:]
                break

            #if line matches the '# N: field' format:
            elif re.match("# +[0-9]+:",line):
                #Note that changing anything here
                #may cause the header names to change
                #if things have already been generated with this script
                #then the same types of files might not have the same headers.

                #pull out the field.
                line=line.replace(re.match("# +[0-9]+:",line).group(),"").strip()

                #capitolize things.
                line=string.capwords(line)

                #lowercase first letter
                line=line[0].lower()+line[1:]

                #add things back if they're letters (ie, get rid of spaces)
                fieldHeader="".join([ x for x in line if x.isalpha()])

                #add header to list of headers
                self.header.append(fieldHeader)

        message="Headers are {}".format(self.header)
        logging.debug(message)

    def _generateIntermediate(self):
        if not self.valid:
            return -1

        #read in file and zip with headers
        if self.header==list(): self._generateHeader()

        self.intermediate=[]

        with open(fileName, "r") as f:
            for line in f:
                line=line.strip()

                #ignoreHeaders
                if len(line)==0 or "#" in line:
                    continue

                #split lines bases on the space value they've been
                #written with
                fields=line.split(" ")

                #turn fields into ints, or Nones if they should be
                parsedFields=list()
                for field in fields:
                    if field=="(none)":
                        parsedFields.append(None)
                    else:
                        #try to convert to float
                        try:
                            field=float(field)
                        except ValueError:
                            pass
                        parsedFields.append(field)

                self.intermediate.append(dict(zip(self.header,parsedFields)))

    def writeJson(self):
        if not self.valid:
            logging.error("cannot write file {} as it's invalid".format(self.fileName))
            return -1

        if self.intermediate==list(): self._generateIntermediate()

        message="Writing file {}".format(self.jsonName)
        logging.debug(message)

        with open(self.jsonName,'w') as outFile:
            json.dump(self.intermediate, outFile)



for fileName in args.files:
    converter=Converter(fileName)
    converter.writeJson()

