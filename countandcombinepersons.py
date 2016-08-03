#takes in a csv file created by process_ner.py

import re
from collections import defaultdict
from collections import Counter

workdir = ""
inputfile_ner = "nertags.csv"
outputdir = workdir
outputfilepersons = "frequentpersons.txt"
outputfiledocs = "frequentpersonsindocs.txt"

with open(workdir+inputfile_ner) as f:
	nerlist = [line.strip().split(',') for line in f.readlines()]

fileset = {line[2].strip() for line in nerlist}

personsdict = defaultdict(list)
orgsdict = defaultdict(list)

for f in fileset:
    print "Entering filename %s in dictionary" %f
    for entity,tag,filename in nerlist:
        if filename.strip() == f:
            if tag.strip() == 'PERSON':
                personsdict[f].append(entity.lower().strip())

personsonly = []
accept = 0
newpersonsdict = defaultdict(list)
for fn in personsdict:
	print "Processing names in filename %s" %fn
	entdict = defaultdict(list)
	for person in personsdict[fn]:
		plist = person.split()
		if plist[-1] in entdict:
			entdict[plist[-1]].append(plist)
		else:
			entdict[plist[-1]] = [plist]

	for entity in entdict:
		thisentnames = entdict[entity]
		for name in thisentnames:
			if len(name) > 1:
				selectname = max(thisentnames, key=len)
				namestring = "".join(selectname)
				namestring= re.sub(',', '', namestring)
				#add this filename to list of files containing the namestring
				if namestring in newpersonsdict and fn not in newpersonsdict[namestring]:
                    newpersonsdict[namestring].append(fn)                
                else:
                	newpersonsdict[namestring] = [fn]
                personsonly.append(namestring)

 #count how many documents each person appears in
 frequentindocslist = []
 for key in newpersonsdict:
 	if len(newpersonsdict[key]) > 1:
 		frequentindocstring = key + ":" + str(len(newpersonsdict[key]))
 		frequentindocslist.append(frequentindocstring)

 #counts the number of a name has appeared no matter how many docs r there
 countpersons = Counter(personsonly)

 frequentpersonslist = []
 for key in countpersons:
 	if countpersons[key] > 1:
 		frequencystring = key + ":" + str(countpersons[key])
 		frequentpersonslist.append(frequencystring)

 frequentpersonstext = "\n".join(frequentpersonslist)
 with open(outputfilepersons, 'w') as f:
 	f.write(frequentpersonstext)

 frequentindocstext = "\n".join(frequentindocslist)
 with open(outputfiledocs, 'w') as f:
 	f.write(frequentindocstext)


