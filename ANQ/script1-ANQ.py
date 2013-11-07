
import sys
sys.path.append("/Users/oriana/Dropbox/Grad/Evaluation2") # add the directory where textgrid.py is to PYTHONPATH

import os
import csv
from textgrid import *

def sortBreak(b):
	if "1" in b:
		return "1"
	elif "2" in b:
		return "2"
	elif "3" in b:
		return "3"
	elif b == "":
		return "NA"
	else: 
		return "Other" 


poaDict = {
	'N':'uvl',
	'b':'lab',
	'p':'lab',
	'm':'lab',
	'F':'lab',
	'f':'lab',
	'c':'alv',
	'cy':'alv.pal',
	'd':'alv',
	'n':'alv',
	't':'alv',
	's':'alv',
	'z':'alv',
	'k':'vel',
	'kj':'vel.pal',
	'g':'vel',
	'gy':'vel.pal',
	'gj':'vel.pal',
	'y':'alv',
	'sj':'alv.pal',
	'sy':'alv.pal',
	'zj':'alv.pal',
	'zy':'alv.pal',
	'nj':'alv.pal',
	'r':'palv',
	'h':'glot',
	'hj':'glot.pal',
	'hy':'glot.pal',
	'cj':'alv.pal',
	'a':'low',
	'e':'mid',
	'o':'mid',
	'i':'high',
	'I':'high',
	'u':'high',
	'U':'high',
	'aH':'low',
	'eH':'mid',
	'oH':'mid',
	'iH':'high',
	'uH':'high',
	'w':'lab'

}

voiceless = "s S f p t k h H"

def addData(grid, fname,writer):
	phoneTier = grid[0]
	wordTier = grid[1]
	# breakTier = grid[2]
	# toneTier = grid[3]
	for i,token in enumerate(phoneTier):
		# if ("i","u","U","I")in phoneTier[i].mark == True :
		if re.search("(?<![a-z])[iyu]", token.mark):

# Create blank list for info to be written
			info = []

#Filename
			info.append(str(fname))

# Token time 
			info.append(token.minTime)

# Name of tier: could be "v", "V", "c,V" or "cc,V". Exclude "vH".
			info.append(token.mark) 

# Morpheme: problem with phone tokens that span multiple
			wd = ["FAILURE"]
			#for k,word in enumerate(wordTier):
			wd = [wordTier.intervalContaining(token.maxTime-0.001).mark]
				#if word.minTime <= token.minTime and word.maxTime >= token.maxTime:
					# wd = [word.mark]
				# if wd == []:
				# 	if word.minTime <= token.minTime <= word.maxTime:
				# 		wd.append(word.mark)
				# 	elif word.minTime <= token.maxTime <= word.maxTime:
				# 		wd.append(word.mark)
				# 	else:
				# 		wd.append("FAILURE")
			info.append("".join(wd))

#PrevSeg:

			seg = ["FAIL"]
			try: 
				if len(phoneTier[i-1].mark) == 1:
					seg = phoneTier[i-1].mark
				else:
					seg = phoneTier[i-2].mark
			except:
				seg = ["#"]
			info.append("".join(seg))
			prevSeg = "".join(seg)


			# ## Burst?
			# if re.search("<cl>,",token.mark) or re.search("<cl>,",phoneTier[i-1].mark):
			# 	info.append("N")
			# else:
			# 	info.append("Y")

# FollSeg
			seg = ["FAIL"]
			try: 
				if len(phoneTier[i+1].mark) == 1:
					seg = phoneTier[i+1].mark
				else:
					seg = phoneTier[i+2].mark

			except:
				seg = ["#"]
			info.append("".join(seg))
			follSeg = "".join(seg)

# HVD.envt change this to use prevSeg
			if prevSeg in voiceless and follSeg in voiceless:
				info.append('Y')
			elif prevSeg in voiceless and (phoneTier[i+1].mark == "#" or phoneTier[i+1].mark == "sp"):
				info.append('Y')
			else: 
				info.append('N')

			# # info.append("Y") if (re.search("[ptksch]", token.mark) or re.search("[ptksch#]", phoneTier[i-1].mark)) and re.search("[ptksch#]", phoneTier[i+1].mark) else info.append("N") #This is not quite right. Should be using the more complicated code from the FollSeg bit. 

# Devoiced? 
			# devoiced = "Y" if re.search("[IU]", token.mark) else "N"
			# info.append(devoiced)

# Vowel duration
			info.append(token.duration())

			# # Onset 0/1
			# info.append("Y") if re.search("[kgsztdnhbpmyrwc]", token.mark) or re.search("[kgsztdnhbpmyrwc]", phoneTier[i-1].mark) else info.append("N")

			# # Coda 0/1
			# info.append("Y") if re.search("[NQ]", token.mark) or re.search("[NQ]", phoneTier[i+1].mark) else info.append("N")

			# # Accent - get from point tier
			# tones = []	
			# for k,point in enumerate(toneTier):
			# 	if  point.time >= token.minTime - 0.01 and point.time <= token.maxTime + 0.01 and point.mark=="A":
			# 		tones.append("A1")
			# 	elif point.time >= phoneTier[i-1].minTime - 0.01 and point.time <= phoneTier[i-1].maxTime + 0.01 and point.mark=="A":
			# 		tones.append("A2")
			# info.append("None") if tones == [] else info.append("".join(tones))

			# # Tone - also from point tier
			# tones = []	
			# for k,point in enumerate(toneTier):
			# 	if  point.time >= token.minTime - 0.01 and point.time <= token.maxTime + 0.01 and point.mark!="A":
			# 		tones.append(point.mark)
			# info.append("None") if tones == [] else info.append("".join(tones))

					
			# # PrevBreak - break tier
			# br = []
			# for k,point in enumerate(breakTier):
			# 	if  token.minTime - 0.01 <= point.time <= token.minTime + 0.01:
			# 		br.append(point.mark)	
			# info.append("None") if br == [] else info.append("".join(br))

			# # break type
			# info.append(sortBreak("".join(br)))

# PrevPz
			if phoneTier[i-1].mark == "sp":
				info.append(phoneTier[i-1].duration())
			else:
				info.append("NA")


			# wd = wordTier.intervalContaining(token.minTime-0.001)
			# try:
			# 	if wd.mark == "#":
			# 		info.append(wd.duration())
			# 	else:
			# 		info.append("NA")
			# except:
			# 	info.append("ERR")
			# # FollBreak
			# br = []
			# for k,point in enumerate(breakTier):
			# 	if  token.maxTime - 0.01 <= point.time <= token.maxTime + 0.01:
			# 		br.append(point.mark) 
			# info.append("None") if br == [] else info.append("".join(br))

			# ## Break type
			# info.append(sortBreak("".join(br)))

			# ## Boundary pitch movement?
			# if sortBreak("".join(br)) == '2':
			# 	info.append("Y") if "b" in "".join(br) else info.append('N')
			# elif sortBreak("".join(br)) == '3':
			# 	info.append("P")
			# else:
			# 	info.append("NA")

# FollPz
			if phoneTier[i+1].mark == "sp":
				info.append(phoneTier[i-1].duration())
			else:
				info.append("NA")
			# wd = wordTier.intervalContaining(token.maxTime+0.01)
			# if wd.mark == "#":
			# 	info.append(wd.duration())
			# elif phoneTier[i+1].mark == "<pz>":
			# 	info.append(phoneTier[i+1].duration())
			# else:
			# 	info.append("NA")


			# # # Syll duration
			# if re.search("(?<!.)[iuIU](?!.)",token.mark) == None:
			# 	if re.search("<cl>,?[a-z]?",phoneTier[i-1].mark):
			# 		info.append(token.duration() + phoneTier[i-1].duration()) # What about cases where U is alone? 
			# 	else: 
			# 		info.append(token.duration())
			# elif re.search("[aeiouAEIOU#]{1}",phoneTier[i-1].mark):
			# 	info.append(token.duration())
			# else:
			# 	if re.search("<cl>,?[A-Za-z]?",phoneTier[i-1].mark):
			# 		info.append(token.duration() + phoneTier[i-1].duration())
			# 	elif re.search("[a-zA-Z]{1}",phoneTier[i-1].mark) and re.search("(?<!.)<[A-Za-z]{2}>(?!.)",phoneTier[i-2].mark):
			# 		info.append(token.duration() + phoneTier[i-1].duration() + phoneTier[i-2].duration())
			# 	elif re.search("[A-Za-z]{1}",phoneTier[i-1].mark):
			# 		info.append(token.duration() + phoneTier[i-1].duration())
			# 	else:
			# 		info.append("ERR")

			# # Previous manner

			# # Following manner

			# # Previous POA 
			# try:
			# 	info.append(poaDict[prevSeg])
			# except:
			# 	info.append("NA")

			# ## Following POA
			# try:
			# 	info.append(poaDict[follSeg])
			# except:
			# 	info.append("NA")			# Could make this into a function like "get POA"
			# poa= []
			# if info[5] in poaDict.keys():
			# 	poa.append(poaDict[info[5]])
			# elif re.search(",([a-zIU]+)",info[5]):
			# 	cons = re.search(",([a-zIU]+)",info[5])
			# 	poa.append(poaDict[cons.groups()[0]])
			# info.append("".join(poa))

			# # Following POA
			# poa= []
			# if info[6] in poaDict.keys():
			# 	poa.append(poaDict[info[6]])
			# elif re.search("(?<cl>,)([a-zIU]+)",info[6]):
			# 	cons = re.search("([a-zIU]+),",info[6])
			# 	poa.append(poaDict[cons.groups()[0]])
			# info.append("".join(poa))



			# Adjacent devoiced v? Search 3 left and 3 right. 
			## CONCEPTUALLY: keep looking left until you find [aeiouAEIOU]. If [IU] then yes, if not then no. Also rightwards search. 

			# try:
			# 	prevsegs = [phoneTier[i-1],phoneTier[i-2]]
			# adj = []

			# for j in range(1,3):
			# 	try:
			# 		if re.search("([IU])",phoneTier[i-j]):
			# 			adj = ["L"]
			# 		if re.search("([IU])",phoneTier[i+j]):
			# 			adj.append("R")
			# 		else: 
			# 			adj = ["None"]
			# 	except:
			# 		pass
			# info.append("".join(adj))
			# LAST COLUMN MARKER
			info.append("#")
			#Stuff:
			# if i == 0:
			# 	info.append("NA")
			# else:
			# 	info.append(phoneTier[i-1].mark)
			# if i == len(phoneTier)-1:
			# 	info.append("NA")
			# else:
			# 	info.append(phoneTier[i+1].mark)
			# for k,word in enumerate(wordTier):
			# 	if word.minTime <= token.minTime and word.maxTime >= token.maxTime:
			# 		info.append(word.mark)
			# 		if word.minTime == token.minTime: 
			# 			info.append("initial")
			# 		elif word.maxTime == token.maxTime:
			# 			info.append("final")
			# 		else:
			# 			info.append("medial")

			writer.writerow(info)

columnNames = [
"file",
"minTime",
"mark",
"morpheme",
"prevSeg",
"follSeg",
"HVD.envt",
"vowelDur",
"prevPz",
"follPz",
"end"
	]
def extract(fileName,dataName): 
	with open(dataName, 'w') as data:
		writer = csv.writer(data,delimiter="	",quotechar='"')
		writer.writerow(columnNames)
		for root, dirs, files in os.walk('TextGrid'):
			for fname in files:
				if re.search(fileName, fname):
					print fname

					try:
						tg = TextGridFromFile(os.path.join('TextGrid/',fname))
					except ValueError as e:
						print "problem opening %s" % fname
						print e
					
					addData(tg, fname,writer)

extract(".*TextGrid","anq-pilot.txt")



# def fileExtract(fileName,dataName):
# 	with open(dataName, 'w') as data: 
# 		writer = csv.writer(data,delimiter="	",quotechar='"')
# 		writer.writerow(["file", "minTime", "mark", "vowel", "morpheme","prevSeg","burst","follSeg","HVD.envt", "devoiced", "onset", "coda","accent","tone","prevBreak","prevBreak.type","prevPz", "follBreak","follBreak.type","follBreak.bpm", "follPz", "vDur","syllDur","precPOA","follPOA", "end"])
# 		print fileName
# 		try:
# 			tg = TextGridFromFile(fileName)
# 			addData(tg)
# 		except ValueError as e:
# 			print "problem opening %s" % fname
# 			print e


### THIS IS THE ONE THAT WORKS! #######
# with open('basicdata.txt', 'w') as data: # put this stuff in the main body. 
# 	writer = csv.writer(data,delimiter="	",quotechar='"')
# 	writer.writerow(["file", "minTime", "mark", "vowel", "morpheme","prevSeg","burst","follSeg","HVD.envt", "devoiced", "onset", "coda","accent","tone","prevBreak","prevBreak.type","prevPz", "follBreak","follBreak.type","follBreak.bpm", "follPz", "vDur","syllDur","precPOA","follPOA", "end"])
# 	for root, dirs, files in os.walk('TextGrid'):
# 		for fname in files:
# 			if re.search('.*TextGrid', fname):
# 				print fname
# 				try:
# 					tg = TextGridFromFile(os.path.join('TextGrid/' , fname))
# 				except ValueError as e:
# 					print "problem opening %s" % fname
# 					print e
# 				addData(tg)	





############ TO DO #############
# how to ADD data to a file instead of replacing existing data. 
# how to iterate through all files in a directory
# how to find which word it is? stat time of segment has to be bewteeen beginning and end of word! make a list of tuples of min/maxTimes

# PrevSeg: if previous mark is <cl>, then take the char 











