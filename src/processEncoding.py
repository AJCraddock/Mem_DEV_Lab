#!/usr/bin/python
import argparse, sys, os

# Process command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("infile",  type=argparse.FileType('r'), 
                    default=sys.stdin)
args = parser.parse_args()

#skips first 2 lines of infile could have sliced it but I anticipate
# we may have larger input files that may not need to be loaded into memory
for _ in xrange(2):
    next(args.infile)
total=0
for line in args.infile:
    storage = []
    storage = line.strip().split(",") 
    if storage[14] == 'True':
        total += 1
task = storage[5]
task = task.replace('2',str(storage[2]))


# make the output directory if it doesn't already exist
if not os.path.exists('../Summaries/' + storage[0]+'/'):
   os.makedirs('../Summaries/' + storage[0]+'/')

#Creates output files for each encoding type
with open('../Summaries/' + storage[0]+'/encodingblockSummary'+'.txt','a') as outfile:
    outfile.write(task+'\tScore  '+ str(total)+'\n')
