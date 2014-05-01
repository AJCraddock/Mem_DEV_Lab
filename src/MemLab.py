#!/usr/bin/python
import argparse, sys, os

# Process command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--indir", "-i", type=str)
args = parser.parse_args()

# Check the provided path to see if it exists
if not os.path.exists(args.indir):
    parser.error("The path " + args.indir + " does not exist")
 
for dataFile in os.listdir(args.indir):
    if os.path.isdir(os.path.join(args.indir, dataFile)): 
        path = args.indir + dataFile
        for fileName in os.listdir(path):
            if  'encoding' in dataFile:
                os.system("python processEncoding.py "+ os.path.join(path.replace(" ","\ "), fileName))
            if 'retrieval' in dataFile:
                 os.system("python processRetrieval.py "+ os.path.join(path.replace(" ","\ "), fileName))
                   #call processEncoding.py passing in the infile,dataFile and subject name       
