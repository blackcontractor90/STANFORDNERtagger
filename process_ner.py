#extract NER tags from output of Stanford NLP

import re, os

workdir = ""
readdir = "" #where the NER-tagged files are
outputdir = workdir
outputfile = "nertags.csv"

nertaglist = []
nametagtexts = []

for nerfile in os.listdir(workdir+readdir):
	print "Processing file %s" % nerfile
	with open(workdir+readdir+nerfile) as f:
		nerprocessed = f.readlines()

		nerprocessednum = enumerate(nerprocessed)

		namesandtags = []

		for index, line in nerprocessednum:
			skipindex = 0
			if 'NamedEntityTag' in line:
				thisline = line.split()
				if thisline[5] != 'NamedEntityTag=0]' and index < len(nerprocessed):
					newtag = thisline[5]
					newname = [thisline[0]]
					myindex = index +1
					try:
						nextline = nerprocessed[myindex]
					except IndexError:
						break
						#as long as the same tag continues, assume same entity
						while nextline.strip().endswith(thisline[5]):
							nextlinelist = nextline.split()
							nextlinename = nextlinelist[0]
							newname.append(nextlinename)
							myindex += 1
							try:
								nextline = nerprocessed[myindex]
							except IndexError:
								myindex -= 1
								break
						skipindex = myindex - index
						for i in range(0, skipindex):
							next(nerprocessednum)
						#clean up so only name and tags remain
						newname[:] = [re.sub('\[Text=','',namepart,count=0, flags=0) for namepart in newname]
						thistag = re.sub('NamedEntityTag=([A-Z]+)\]*','\g<1>',newtag,count=0, flags=0)
                newnamestring = " ".join(newname)
                		#remove commas in named entity so they don't mess up the csv
                		newnamestring = re.sub(',', '', newnamestring, count=0, flags=0)
                		#add tag and filename to line
                		newline = [newnamestring]
                		newline.append(thistag)
                		newline.append(nerfile)
                		nameplustagplusfile = ",".join(newline)
                		namesandtags.append(nameplustagplusfile)

                		nametagtext = "\n".join(namesandtags) #from a single file
                		nametagtexts.append(nametagtext) #add tags from single file to list

                		fulltext = "\n".join(nametagtexts) #tags from all files into text
                		with open(outputdir+outputfile, 'w') as f:
                			f.write(fulltext)





