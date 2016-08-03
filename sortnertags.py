#further processing the NER output

import os
from collections import defaultdict

workdir = ""
inputfile = "nertags.csv"
outputdir = "nerentitieslists/"
if not os.path.exists(outputdir):
	os.makedirs(outputdir)

print "Reading and processing file..."
with open(workdir+inputfile) as f:
	nertagslist = [line.strip().split('.') for line in f.readlines()]

print "Creating tagset..."

tagset = {line[1].strip() for line in nertagslist}

tagsdict = defaultdict(list)

for tag in tagset:
	print "Working on tag %s" %tag
	for entity, thistag,_ in nertagslist:
		if thistag.strip() == tag:
			tagsdict[tag].append(entity)

for tag in tagsdict:
	fname = tag + ".txt"
	entities = "\n".join(tagsdict[tag])
	with open(workdir+outputdir+fname, 'w') as f:
		f.write(entities)

print "Done."


