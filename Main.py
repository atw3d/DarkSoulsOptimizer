#!/usr/bin/python

import sys
import math
import os

#ATW 2/21; Removing from build, not currently used; Should be pulled into its own class
# def GetFloat(strPrompt):
	## returns int if given numeric; will cycle until given good value
	# while true:
		# strInput = raw_input(strPrompt)
		# if strInput == "exit":
			# flMasterHelms.close()
			# flMasterChests.close()
			# flMasterGauntlets.close()
			# flMasterGreaves.close()
			# sys.exit()
		# else:
			## Try to convert to given return type
			# try:
				# strReturnVal = float(strInput)
			# except ValueError:
				# print "Must enter a numeric value."

				
# def GetInt(strPrompt):
	## returns int if given numeric; will cycle until given good value
	# while true:
		# strInput = raw_input(strPrompt)
		# if strInput == "exit":
			# flMasterHelms.close()
			# flMasterChests.close()
			# flMasterGauntlets.close()
			# flMasterGreaves.close()
			# sys.exit()
		# else:
			## Try to convert to given return type
			# try:
				# strReturnVal = int(strInput)
			# except ValueError:
				# print "Must enter an integer value."

				
def TestOwned(lstOwned, helms={}, chests={}, gauntlets={}, greaves={}):
	lstMasterNames = []
	for helm in helms:
		lstMasterNames.append(helm.lower())
	for chest in chests:
		lstMasterNames.append(chest.lower())
	for gauntlet in gauntlets:	
		lstMasterNames.append(gauntlet.lower())
	for greave in greaves:
		lstMasterNames.append(greave.lower())
	
	strErrors = ""
	for owned in lstOwned:
		if owned.lower() not in lstMasterNames:
			strErrors = strErrors + owned + os.linesep
	if strErrors != "":
		print "These items do not exist in Master Lists:"
		print strErrors
#End TestOwned()

def CreateOwnedLists(flOwnedMaster):
	#returns lists in order: 
	lstOwnedHelms = []
	lstOwnedChests = []
	lstOwnedGauntlets = []
	lstOwnedGreaves = []
	
	strCurrentList = ""
	for strItemLine in flOwnedMaster:
		strItem = strItemLine.lstrip('#').rstrip()
		if strItemLine.startswith('#'):
			if strItem == "Helms" or strItem == "Chests" or strItem == "Gauntlets" or strItem == "Greaves":
				#Header line (Helms, Chests, Gauntlets, Greaves)
				strCurrentList = strItem
			else:
				#commented out item
				continue
		else:
			#item line
			if strCurrentList == "Helms":
				lstOwnedHelms.append(strItem)
			elif strCurrentList == "Chests":
				lstOwnedChests.append(strItem)
			elif strCurrentList == "Gauntlets":
				lstOwnedGauntlets.append(strItem)
			elif strCurrentList == "Greaves":
				lstOwnedGreaves.append(strItem)
			else:
				print "Error in xxx_owned.txt" + os.linesep
				True
	return lstOwnedHelms, lstOwnedChests, lstOwnedGauntlets, lstOwnedGreaves
#End CreateOwnedLists

def main():
	while True:
		#vars for final build
		#
		fltBestArmor = 0.0
		fltWeight = 0.0
		strBestHelm = ""
		strBestChest = ""
		strBestGauntlet = ""
		strBestGreaves = ""
		#ATW 2/21; ADD; new functionality to prevent pieces of armor
		lstPreventHelms = []
		lstPreventChests = []
		lstPreventGauntlets = []
		lstPreventGreaves = []
			
			
		#open files for use, discard first header line
		#
		flMasterHelms = open('DS'+strVer+'_Helms.csv','r')
		#ATW 2/21; first header used to create dictionary of [column:index]; created strArmorHeader
		strArmorHeader = flMasterHelms.readline()
		flMasterGauntlets = open('DS'+strVer+'_Gauntlets.csv','r')
		flMasterGauntlets.readline()
		flMasterChests = open('DS'+strVer+'_Chests.csv','r')
		flMasterChests.readline()
		flMasterGreaves = open('DS'+strVer+'_Greaves.csv','r')
		flMasterGreaves.readline()
		
		flOwned = open('DS' + strVer + '_' + strUser + '_owned.txt', 'r')
			
			
		#Create dictionary of column name:index
		#
		lstColNames = strArmorHeader.rstrip().split(',')
		dictIndex = {}
		for colName in lstColNames:
			dictIndex[colName] = lstColNames.index(colName)
		
		
		#Append all items to appropriate list of lists
		#
		for curHelm in flMasterHelms:
			lstCurHelm = curHelm.rstrip().split(',')
			dictMasterHelms[lstCurHelm[0]] = lstCurHelm
		for curChest in flMasterChests:
			lstCurChest = curChest.rstrip().split(',')
			dictMasterChests[lstCurChest[0]] = lstCurChest
		for curGauntlet in flMasterGauntlets:
			lstCurGauntlet = curGauntlet.rstrip().split(',')
			dictMasterGauntlets[lstCurGauntlet[0]] = lstCurGauntlet
		for curGreave in flMasterGreaves:
			lstCurGreave = curGreave.rstrip().split(',')
			dictMasterGreaves[lstCurGreave[0]] = lstCurGreave
					
		lstOwnedHelms, lstOwnedChests, lstOwnedGauntlets, lstOwnedGreaves = CreateOwnedLists(flOwned)
		
		
		#Test to see if lstOwned contains items not in Master lists
		#
		TestOwned(lstOwnedHelms+lstOwnedChests+lstOwnedGauntlets+lstOwnedGreaves,\
				  dictMasterHelms, dictMasterChests, dictMasterGauntlets, dictMasterGreaves)


		#inputs
		#
		fltMaxWeight = float(raw_input("Maximum Weight: "))
		fltMaxPercent = float(raw_input("Max Encumerance %: ")) * 0.01
		#ATW 2/21; not needed, ring encumberance is pre-calculated in Max Weight
		#ltEncScaling = float(raw_input("Ring Encumberance increase %: ")) * 0.01 + 1.0
		fltWeaponsWeight = float(0.0)
		while True:
			strAuxInput = raw_input("Weapon/shield/ring weight: ")
			if strAuxInput == '.':
				break
			elif strAuxInput == '':
				continue
			elif strAuxInput == 'exit':
				sys.exit()
			elif not (strAuxInput.replace('.','')).isdigit():
				print "not a digit"
				continue
			else:
				fltWeaponsWeight += float(strAuxInput)
		while True:
			strAuxInput = raw_input("Required armor: ")
			if strAuxInput == '.':
				break
			elif strAuxInput == '':
				continue
			elif strAuxInput == 'exit':
				sys.exit()
			else:
				#test for existence
				if strAuxInput not in lstOwnedHelms + lstOwnedChests + lstOwnedGauntlets + lstOwnedGreaves:
					print strAuxInput + " does not exist in owned armor pieces."
				else:
					if strAuxInput in lstOwnedHelms:
						strBestHelm = strAuxInput
					elif strAuxInput in lstOwnedChests:
						strBestChest = strAuxInput
					elif strAuxInput in lstOwnedGauntlets:
						strBestGauntlet = strAuxInput
					elif strAuxInput in lstOwnedGreaves:
						strBestGreaves = strAuxInput
					else:
						print "Error in matching required input to _owned.txt"
		#ATW 2/21; ADD; new functionality to prevent pieces of armor
		while True:
			strAuxInput = raw_input("Prevent armor: ")
			if strAuxInput == '.':
				break
			elif strAuxInput == '':
				continue
			elif strAuxInput == 'exit':
				sys.exit()
			else:
				if strAuxInput in lstOwnedHelms:
						lstPreventHelms.append(strAuxInput)
				elif strAuxInput in lstOwnedChests:
					lstPreventChests.append(strAuxInput)
				elif strAuxInput in lstOwnedGauntlets:
					lstPreventGauntlets.append(strAuxInput)
				elif strAuxInput in lstOwnedGreaves:
					lstPreventGreaves.append(strAuxInput)
				else:
					print "Error in matching prevented input to _owned.txt"
		
		#iterate through all possibilities, find max armor
		#
		#if a armor piece has been chosen, restrict armor type list
		if strBestHelm != "":
			lstOwnedHelms = [strBestHelm]
		if strBestChest != "":
			lstOwnedChests = [strBestChest]
		if strBestGauntlet != "":
			lstOwnedGauntlets = [strBestGauntlet]
		if strBestGreaves != "":
			lstOwnedGreaves = [strBestGreaves]
		
		#ATW 2/21; ADD; new functionality to prevent pieces of armor
		if len(lstPreventHelms) > 0:
			for each in lstPreventHelms:
				lstOwnedHelms.remove(each)
		if len(lstPreventChests) > 0:
			for each in lstPreventChests:
				lstOwnedChests.remove(each)
		if len(lstPreventGauntlets) > 0:
			for each in lstPreventGauntlets:
				lstOwnedGauntlets.remove(each)
		if len(lstPreventGreaves) > 0:
			for each in lstPreventGreaves:
				lstOwnedGreaves.remove(each)
				
		for curHelm in lstOwnedHelms:
			for curChest in lstOwnedChests:
				for curGauntlet in lstOwnedGauntlets:
					for curGreave in lstOwnedGreaves:
						fltCurArmor = (float(dictMasterHelms[curHelm][dictIndex["PdefBase"]]) + \
									   float(dictMasterChests[curChest][dictIndex["PdefBase"]]) + \
									   float(dictMasterGreaves[curGreave][dictIndex["PdefBase"]]) + \
									   float(dictMasterGauntlets[curGauntlet][dictIndex["PdefBase"]]))
									  
						fltCurWeight = float(dictMasterHelms[curHelm][dictIndex["Weight"]]) + \
									   float(dictMasterChests[curChest][dictIndex["Weight"]]) + \
									   float(dictMasterGauntlets[curGauntlet][dictIndex["Weight"]]) + \
									   float(dictMasterGreaves[curGreave][dictIndex["Weight"]]) + \
									   fltWeaponsWeight
						
						#ATW 2/21; removing fltEncScaling calculation, not needed
						#if fltCurWeight < (fltMaxWeight*fltEncScaling*fltMaxPercent) and fltCurArmor > fltBestArmor:
						if fltCurWeight < (fltMaxWeight*fltMaxPercent) and fltCurArmor > fltBestArmor:
							#under weight, better armor rating
							#print "New Armor"
							fltBestArmor = fltCurArmor
							fltWeight = fltCurWeight
							
							strBestHelm = curHelm
							strBestChest = curChest
							strBestGauntlet = curGauntlet
							strBestGreaves = curGreave
		#End iteration
		
		#print results
		#
		print
		print "Best Armor: " + str(fltBestArmor)
		print "Weight: " + str(fltWeight)
		print "Weapons: " + str(fltWeaponsWeight)
		print "----- ----- -----"
		print strBestHelm
		print strBestChest
		print strBestGauntlet
		print strBestGreaves
		
		strInput = raw_input("exit:")
		if strInput.lower() == "exit":
			flMasterHelms.close()
			flMasterChests.close()
			flMasterGauntlets.close()
			flMasterGreaves.close()
			sys.exit()
		else:
			print
			print
#end Main()


#Start Program
print "Dark Souls Optimizer ver. 1.0.0.2"
print "-------------------" + os.linesep

strUser = raw_input("User: ")
if strUser.lower() == "exit":
	sys.exit()
strVer = raw_input("Dark Souls (1/2): ")
if strVer.lower() == "exit":
	sys.exit()
print "-------------------"

#declare global vars
#	
lstOwnedHelms = []
lstOwnedChests = []
lstOwnedGauntlets = []
lstOwnedGreaves = []

dictMasterHelms = {}
dictMasterChests = {}
dictMasterGreaves = {}
dictMasterGauntlets = {}

#Main functionality
main()

