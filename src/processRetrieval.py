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
block = 0
typeOfRetrieval = ""
hit_check = 0
miss_check = 0
fa_check = 0
cr_check = 0
previous_hit = False
spatial_correct = 0
spatial_incorrect = 0
debuggCount =0 
for line in args.infile:
    storage = []
    storage = line.strip().split(",")

#gets the block number for other things later on
    if block == 0:
        block = storage[2] 
#
#    if  "spatial" not in typeOfRetrieval  or "temporal" not in typeOfRetrieval:
    if typeOfRetrieval == "": 
        if int(block) < 3:
            if "recog" != storage[7]:
                typeOfRetrieval = storage[7]
        elif int(block) == 3:
            typeOfRetrieval = "temporal"
        elif int(block) == 4:
            typeOfRetrieval = "spatial"
#=IF(AND(H3="recog", IF(OR(I3="congruent", I3="incongruent"), M3="NUMPAD0")), "hit", "")
    if  "congruent" in storage[8].lower() and "NUMPAD0" in storage[12] and  "recog" in storage[7]:
        hit_check += 1
        previous_hit = True
#=IF(AND(H3="recog", IF(OR(I3="congruent", I3="incongruent"), M3="NUMDECIMAL")), "miss", "")
    if  "congruent" in storage[8].lower() and "NUMDECIMAL" in storage[12] and  "recog" in storage[7]:
        miss_check += 1
        previous_hit = False
#=IF(AND(H3="recog", I3="novel", M3="NUMPAD0"), "FA", "")    
    if  "novel" in storage[8].lower() and "NUMPAD0" in storage[12] and  "recog" in storage[7]:
        fa_check += 1
        previous_hit = False
#=IF(AND(H4="recog", I4="novel", M4="NUMDECIMAL"), "CR", "")
    if  "novel" in storage[8].lower() and "NUMDECIMAL" in storage[12] and  "recog" in storage[7]:
        cr_check += 1
        previous_hit = False
#=IF(AND(H8="spatialQ", Q7="hit", P8=1), "correct", "")
    if  "spatial" in storage[7].lower() or "temporal" in storage[7].lower():
        if previous_hit == True  and storage[15] == 'True':
            spatial_correct += 1
            previous_hit = False
#=IF(AND(H9="spatialQ", Q8="hit", P9=0), "incorrect", "")
    if  "spatial" in storage[7].lower() or "temporal" in storage[7].lower():
        if previous_hit == True  and storage[15] == 'False':
            spatial_incorrect += 1
            previous_hit = False

#print "Summary for " + str(storage[0])
#print str(block)
#print typeOfRetrieval
#print str(hit_check)
#print str(miss_check)
#print str(fa_check)
#print str(cr_check)
#print str(spatial_correct)
#print str(spatial_incorrect)
spatial_probability = (float(spatial_correct) /(spatial_correct + spatial_incorrect))*100
#print str(spatial_probability)

if not os.path.exists('../Summaries/' + storage[0]+'/'):
   os.makedirs('../Summaries/' + storage[0]+'/')

#Creates output files for each encoding type
with open('../Summaries/' + storage[0]+'/retrievalSummary'+'.txt','a') as      outfile:
        outfile.write('Retrival Run {0} ( {1} ) \n\tHits Count: {2} \n\tMiss Count: {3} \n\tFA Check: {4} \n\tCR Check: {5} \n\tSpatial Correct: {6} \n\tSpatial Incorrect: {7} \n\tSpatial Probability: {8:.2f}%\n\n\n'.format( block,
                             typeOfRetrieval, hit_check, miss_check, fa_check,
                             cr_check, spatial_correct, spatial_incorrect,
                             spatial_probability ) )

