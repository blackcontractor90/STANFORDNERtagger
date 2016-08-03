#takes an input as input DATE.txt created from sortnertags.py

import re

inputfile = "nerentitieslists/DATE.txt"
outputfile = "nerentitieslists/DATE-YEARONLY.txt"

with open(inputfile) as f:
	yearlines = [line.strip() for line in f.readlines() if re.search('[0-9][0-9][0-9][0-9]',line,flags=0)]

yeartext = "\n".join(yearlines)

with open(outputfile, 'w') as f:
	f.write(yeartext)
