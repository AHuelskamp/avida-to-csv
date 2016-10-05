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

import csv 
import json 
import sys 
import argparse 


commandParser = argparse.ArgumentParser(description="A list of avida files to convert to json") 
commandParser.add_argument('files', metavar="FILE", type=str, nargs="+", 
                        help="files to convert")

args = commandParser.parse_args()

