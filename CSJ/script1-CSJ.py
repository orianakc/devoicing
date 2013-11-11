
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

def addData(grid, fname, writer):
	phoneTier = grid[1]
	wordTier = grid[0]
	breakTier = grid[2]
	toneTier = grid[3]
	for i,token in enumerate(phoneTier):
		# if ("i","u","U","I")in phoneTier[i].mark == True :
		if re.search("(?<![aeiou],)[iuIU](?!,[aeiou])", token.mark) and re.search("H",token.mark) == None and re.search("<uv>",token.mark) == None :
			# Create blank list for info to be written
			info = []
			#Filename
			info.append(str(fname))
			# Token time 
			info.append(token.minTime)
			# Name of tier: could be "v", "V", "c,V" or "cc,V". Exclude "vH".
			info.append(token.mark) 
			# Vowel type - i or u
			if re.search("[Ii]", token.mark): 
				info.append("i") 
			elif re.search("[uU]", token.mark):
				info.append("u")
			# Morpheme: problem with phone tokens that span multiple
			wd = ["FAILURE"]
			#for k,word in enumerate(wordTier):
			wd = [wordTier.intervalContaining(token.maxTime-0.01).mark]
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

				# HAVE TO HAVE AN "ELSE" CONDITION HERE

			#PrevSeg: special cases! also word boundaries...?
			seg = []
			if re.search("([a-zA-Z]{1,2}),[iuIU]",token.mark):
				mySeg = re.search("([a-zA-Z]{1,2}),[iuIU]",token.mark)
				seg.append(mySeg.groups()[0])
			elif re.search("([a-zA-Z]{1,2})(?!.)",phoneTier[i-1].mark):
				mySeg = re.search("([a-zA-Z]{1,2})(?!.)",phoneTier[i-1].mark)
				seg.append(mySeg.groups()[0])
			elif re.search("([a-zA-Z]{1,2})(?!.)",phoneTier[i-2].mark):
				mySeg = re.search("([a-zA-Z]{1,2})(?!.)",phoneTier[i-2].mark)
				seg.append(mySeg.groups()[0])			
			else:
				seg.append("EXCEPT")
			info.append("".join(seg))
			prevSeg = "".join(seg)


			## Burst?
			if re.search("<cl>,",token.mark) or re.search("<cl>,",phoneTier[i-1].mark):
				info.append("N")
			else:
				info.append("Y")

			# FollSeg
			seg = []
			if re.search("[iuIU],([a-zA-Z]{1,2})",token.mark):
				mySeg = re.search("[iuIU],([a-zA-Z]{1,2})",token.mark)
				seg.append(mySeg.groups()[0])
			elif re.search("(?<!.)([a-zA-Z]{1,2})",phoneTier[i+1].mark):
				mySeg = re.search("(?<!.)([a-zA-Z]{1,2})",phoneTier[i+1].mark)
				seg.append(mySeg.groups()[0])
			else: 
				try:
					if re.search("(?<!.)([a-zA-Z]{1,2})",phoneTier[i+2].mark):
						mySeg = re.search("(?<!.)([a-zA-Z]{1,2})",phoneTier[i+2].mark)
						seg.append(mySeg.groups()[0])
					else:
						mySeg = re.search("(?<!.)([a-zA-Z]{1,2})",phoneTier[i+3].mark)
						seg.append(mySeg.groups()[0])						
				except:
					seg.append("##")

			info.append("".join(seg))
			follSeg = "".join(seg)

# # Syll duration
			syllable = []
			duration = 0
			onset = ""
			coda = ""

			if re.search("^[a-zA-Z]{1,2},[iuIU]$",token.mark):			## "sj,I" or "c,U"
				if re.search("^<cl>$",phoneTier[i-1].mark):				## "<cl>" + "c,U"
					syllable.append(phoneTier[i-1].mark)
					duration += phoneTier[i-1].duration()
				syllable.append(token.mark)
				duration += token.duration()
			elif re.search("^<cl>,[a-zA-Z]{1,2},[iuIU]$",token.mark):	## "<cl>,c,U"
				syllable.append(token.mark)
				duration = token.duration()
			elif re.search("^[iuIU].*$",token.mark):					## "U" or "i,N"
				if re.search("[aeiou]$",phoneTier[i-1].mark):			## Ignores prev interval containing V
					pass
				elif re.search("^<cl>,[a-zA-Z]{1,2}$",phoneTier[i-1].mark): ## Captures "<cl>,k"
					syllable.append(phoneTier[i-1].mark)
					duration += phoneTier[i-1].duration()
				elif re.search("^[a-zA-Z]{1,2}$",phoneTier[i-1].mark):	## Captures "k"
					duration += phoneTier[i-1].duration()
					if re.search("^<cl>$",phoneTier[i-2].mark):			## Adds "<cl>" of "k"
						duration += phoneTier[i-2].duration()
						syllable.append(phoneTier[i-2].mark)
					syllable.append(phoneTier[i-1].mark)
				if re.search("^[iuIU],?N?$",token.mark):
					syllable.append(token.mark) 
					duration += token.duration()  
				if re.search("^[NQ]",phoneTier[i+1].mark):				## 
					syllable.append(re.search("^([NQ])",phoneTier[i+1].mark).group())
					coda = re.search("^([NQ])",phoneTier[i+1].mark).group()
					if re.search("^[NQ]$",phoneTier[i+1].mark):
						duration += phoneTier[i+1].duration()
					else: 
						duration = "ERR_CODA_OVERLAP"
			else: 
				syllable.append(re.search("(.*[iuIU]),?.*$",token.mark).group())
				duration = "ERR_OVERLAP"

			info.append("".join(syllable))
			info.append(duration)



			# HVD.envt change this to use prevSeg
			if prevSeg in "k ky kj t tj ty c cj cy F h hy hj p py pj s sj sy" and follSeg in "k ky kj t tj ty c cj cy F h hy hj p py pj s sj sy":
				info.append('Y')
			elif prevSeg in "k ky kj t tj ty c cj cy F hj hy p py s sj sy" and phoneTier[i+1].mark == "#":
				info.append('Y')
			else: 
				info.append('N')

			# info.append("Y") if (re.search("[ptksch]", token.mark) or re.search("[ptksch#]", phoneTier[i-1].mark)) and re.search("[ptksch#]", phoneTier[i+1].mark) else info.append("N") #This is not quite right. Should be using the more complicated code from the FollSeg bit. 

			# Devoiced? 
			devoiced = "Y" if re.search("[IU]", token.mark) else "N"
			info.append(devoiced)

#DEBUG ME   # Onset 0/1
			# info.append("Y") if re.search("[kgsztdnhbpmyrwcF]", token.mark) or re.search("[kgsztdnhbpmyrwcF]", phoneTier[i-1].mark) else info.append("N")

# DEBUG ME # Coda 0/1
			# info.append("Y") if re.search("[NQ]", token.mark) or re.search("[NQ]", phoneTier[i+1].mark) else info.append("N")

			# Accent - get from point tier
			tones = []	
			for k,point in enumerate(toneTier):
				if  point.time >= token.minTime - 0.01 and point.time <= token.maxTime + 0.01 and point.mark=="A":
					tones.append("A1")
				elif point.time >= phoneTier[i-1].minTime - 0.01 and point.time <= phoneTier[i-1].maxTime + 0.01 and point.mark=="A":
					tones.append("A2")
			info.append("None") if tones == [] else info.append("".join(tones))

# Tone - make this ignore "A"
			tones = []	
			for k,point in enumerate(toneTier):
				if  point in token and re.search("A",point.mark)==None:
					tones.append(point.mark)
			info.append("None") if tones == [] else info.append("".join(tones))

			# Tone type
			
					
			# PrevBreak - break tier
			br = []
			for k,point in enumerate(breakTier):
				if  token.minTime - 0.01 <= point.time <= token.minTime + 0.01:
					br.append(point.mark)	
			info.append("None") if br == [] else info.append("".join(br))

			# break type
			info.append(sortBreak("".join(br)))

			# PrevPz - hmm but ignores cases where vowel is in an initial CV syll
			wd = wordTier.intervalContaining(token.minTime-0.001)
			try:
				if wd.mark == "#":
					info.append(wd.duration())
				else:
					info.append("NA")
			except:
				info.append("ERR")
			# FollBreak
			br = []
			for k,point in enumerate(breakTier):
				if  token.maxTime - 0.01 <= point.time <= token.maxTime + 0.01:
					br.append(point.mark) 
			info.append("None") if br == [] else info.append("".join(br))

			## Break type
			info.append(sortBreak("".join(br)))

			## Boundary pitch movement?
			if sortBreak("".join(br)) == '2':
				info.append("Y") if "b" in "".join(br) else info.append('N')
			elif sortBreak("".join(br)) == '3':
				info.append("P")
			else:
				info.append("NA")

			# FollPz
			# wd = wordTier.intervalContaining(token.maxTime+0.01)
			if phoneTier[i+1].mark == "#":
				info.append(phoneTier[i+1].duration())
			elif phoneTier[i+1].mark == "<pz>":
				info.append(phoneTier[i+1].duration())
			else:
				info.append("NA")

			# Vowel duration
			if re.search("(?<!.)[iuIU](?!.)",token.mark):
				info.append(token.duration())
			else:
				info.append("NA")



			# Previous manner

			# Following manner

			# Previous POA 
			try:
				info.append(poaDict[prevSeg])
			except:
				info.append("NA")

			## Following POA
			try:
				info.append(poaDict[follSeg])
			except:
				info.append("NA")			# Could make this into a function like "get POA"


# Adjacent devoiced v? Search 3 left and 3 right. 
# ## Devoiced left? 
			adjleft = []
			try: 
				adjleft.append(phoneTier[i-3].mark)
			except: 
				continue
			try:
				adjleft.append(phoneTier[i-2].mark)
			except: 
				continue
			try:
				adjleft.append(phoneTier[i-1].mark)
			except: 
				continue
			if re.search("[IU](?!.*[aeiou])","".join(adjleft)):
				info.append("L")
			else:
				info.append("N")
			info.append(" ".join(adjleft))
			# adj = ["ERR"]
			# try:
			# 	if re.search("[aeiouAEIOU]",phoneTier[i-1].mark):
			# 		if re.search("[IU]",phoneTier[i-1].mark):
			# 			adj=["L"]
			# 		elif re.search("[aeiouAEIOU]",phoneTier[i-2].mark):
			# 			if re.search("[IU](?!,)",phoneTier[i-2].mark):
			# 				adj=["L"]
			# 			else:
			# 				adj=["N"]
			# 		else:
			# 			adj=["N"]
			# 	else:
			# 		adj=["N"]
			# except:
			# 	adj=["N"]
			# info.append("".join(adj))
## Devoiced right?
			adjleft = []
			try: 
				adjleft.append(phoneTier[i+1].mark)
			except: 
				continue
			try:
				adjleft.append(phoneTier[i+2].mark)
			except: 
				continue
			try:
				adjleft.append(phoneTier[i+3].mark)
			except: 
				continue
			if re.search("[IU]","".join(adjleft)) and re.search("[aeiou]","".join(adjleft))==None:
				info.append("R")
			else:
				info.append("N")
			info.append(" ".join(adjleft))
			# adj = ["ERR"]
			# if re.search("[aeiouAEIOU]",phoneTier[i+1].mark):
			# 	if re.search("[IU]",phoneTier[i+1].mark):
			# 		adj=["R"]
			# 	elif re.search("[aeiouAEIOU]",phoneTier[i+2].mark):
			# 		if re.search("[IU](?!,)",phoneTier[i+2].mark):
			# 			adj=["R"]
			# 		else:
			# 			adj=["N"]
			# 	else:
			# 		adj=["N"]
			# else:
			# 	adj=["N"]
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

# tg = TextGridFromFile("A01F0055.TextGrid")
# addData(tg)


# print phoneTier[1:40]

##
## myMatch = re.search("<cl>,([a-z])", myString)
## myMatch.groups()[0]
## string method .find finds thing in a string. 

## OKAY THIS ISN'T WORKING GET "NameError: global name 'tg' is not defined"
def extract(fileName,dataName): 
	with open(dataName, 'w') as data:
		writer = csv.writer(data,delimiter="	",quotechar='"')
		writer.writerow(["file", "minTime", "mark", "vowel", "morpheme","prevSeg","burst","follSeg","HVD.envt", "devoiced", "onset", "coda","accent","tone","prevBreak","prevBreak.type","prevPz", "follBreak","follBreak.type","follBreak.bpm", "follPz", "vDur","syllDur","precPOA","follPOA","dvL","dvR", "end"])
		for root, dirs, files in os.walk('TextGrid'):
			for fname in files:
				if re.search(fileName, fname):
					print fname
					try:
						tg = TextGridFromFile(os.path.join('TextGrid/',fname))
					except ValueError as e:
						print "problem opening %s" % fname
						print e
					addData(tg, fname, writer)

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



extract("A06F0049","A06F0049-data.txt")	



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











