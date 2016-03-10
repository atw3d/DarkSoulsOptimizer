#!/usr/bin/python

import sys
import math
import os
				
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
		#ATW 2/27; using lists to store 3 best sets instead of strings for 1
		# fltBestArmor = 0.0
		# fltWeight = 0.0
		strBestHelm = ""
		strBestChest = ""
		strBestGauntlet = ""
		strBestGreaves = ""
		
		lstfltBestArmor = [0.0,0.0,0.0]
		lstfltWeight = [0.0,0.0,0.0]
		lststrBestHelm = ['','','']
		lststrBestChest = ['','','']
		lststrBestGauntlet = ['','','']
		lststrBestGreaves = ['','','']
		
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


		#Inputs
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
					lstOwnedHelms.remove(strAuxInput)
				elif strAuxInput in lstOwnedChests:
					lstOwnedChests.remove(strAuxInput)
				elif strAuxInput in lstOwnedGauntlets:
					lstOwnedGauntlets.remove(strAuxInput)
				elif strAuxInput in lstOwnedGreaves:
					lstOwnedGreaves.remove(strAuxInput)
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
		#ATW 2/27; REMOVE; moved to above input logic, take out of lists in place
		# if len(lstPreventHelms) > 0:
			# for each in lstPreventHelms:
				# lstOwnedHelms.remove(each)
		# if len(lstPreventChests) > 0:
			# for each in lstPreventChests:
				# lstOwnedChests.remove(each)
		# if len(lstPreventGauntlets) > 0:
			# for each in lstPreventGauntlets:
				# lstOwnedGauntlets.remove(each)
		# if len(lstPreventGreaves) > 0:
			# for each in lstPreventGreaves:
				# lstOwnedGreaves.remove(each)
				
		#ATW 2/27; define dictIndex["PdefBase"] & dictIndex["Weight"] before loops for better performance
		strDictPDefBaseIndex = dictIndex["PdefBase"]
		strDictWeightIndex = dictIndex["Weight"]
		
		for curHelm in lstOwnedHelms:
			for curChest in lstOwnedChests:
				for curGauntlet in lstOwnedGauntlets:
					for curGreave in lstOwnedGreaves:						
						fltCurArmor = (float(dictMasterHelms[curHelm][strDictPDefBaseIndex]) + \
									   float(dictMasterChests[curChest][strDictPDefBaseIndex]) + \
									   float(dictMasterGreaves[curGreave][strDictPDefBaseIndex]) + \
									   float(dictMasterGauntlets[curGauntlet][strDictPDefBaseIndex]))
									  
						fltCurWeight = float(dictMasterHelms[curHelm][strDictWeightIndex]) + \
									   float(dictMasterChests[curChest][strDictWeightIndex]) + \
									   float(dictMasterGauntlets[curGauntlet][strDictWeightIndex]) + \
									   float(dictMasterGreaves[curGreave][strDictWeightIndex]) + \
									   fltWeaponsWeight
						
						#ATW 2/21; removing fltEncScaling calculation, not needed
						#if fltCurWeight < (fltMaxWeight*fltEncScaling*fltMaxPercent) and fltCurArmor > fltBestArmor:
						
						#ATw 2/27; new logic to support lists of 3 best armor sets
						if fltCurWeight < (fltMaxWeight*fltMaxPercent):
							if fltCurArmor > lstfltBestArmor[0]:
								#under weight, better armor rating than best
								lstfltBestArmor[2] = lstfltBestArmor[1]
								lstfltBestArmor[1] = lstfltBestArmor[0]
								lstfltBestArmor[0] = fltCurArmor
								
								lstfltWeight[2] = lstfltWeight[1]
								lstfltWeight[1] = lstfltWeight[0]
								lstfltWeight[0] = fltCurWeight
								lststrBestHelm[2] = lststrBestHelm[1]
								lststrBestHelm[1] = lststrBestHelm[0]
								lststrBestHelm[0] = curHelm
								lststrBestChest[2] = lststrBestChest[1]
								lststrBestChest[1] = lststrBestChest[0]
								lststrBestChest[0] = curChest
								lststrBestGauntlet[2] = lststrBestGauntlet[1]
								lststrBestGauntlet[1] = lststrBestGauntlet[0]
								lststrBestGauntlet[0] = curGauntlet
								lststrBestGreaves[2] = lststrBestGreaves[1]
								lststrBestGreaves[1] = lststrBestGreaves[0]
								lststrBestGreaves[0] = curGreave
							
							elif fltCurArmor > lstfltBestArmor[1]:
								#under weight, better armor rating 2nd best
								lstfltBestArmor[2] = lstfltBestArmor[1]
								lstfltBestArmor[1] = fltCurArmor
								lstfltWeight[2] = lstfltWeight[1]
								lstfltWeight[1] = fltCurWeight
								
								lststrBestHelm[2] = lststrBestHelm[1]
								lststrBestHelm[1] = curHelm
								lststrBestChest[2] = lststrBestChest[1]
								lststrBestChest[1] = curChest
								lststrBestGauntlet[2] = lststrBestGauntlet[1]
								lststrBestGauntlet[1] = curGauntlet
								lststrBestGreaves[2] = lststrBestGreaves[1]
								lststrBestGreaves[1] = curGreave
							elif fltCurArmor > lstfltBestArmor[2]:
								#under weight, better armor rating than 3rd best
								lstfltBestArmor[2] = fltCurArmor
								lstfltWeight[2] = fltCurWeight
								
								lststrBestHelm[2] = curHelm
								lststrBestChest[2] = curChest
								lststrBestGauntlet[2] = curGauntlet
								lststrBestGreaves[2] = curGreave
		#End iteration
		
		#print results
		#
		#ATW 2/27; changed to fit 3 columns of results
		print
		# print "Best Armor: " + str(fltBestArmor)
		# print "Weight: " + str(fltWeight)
		# print "Weapons: " + str(fltWeaponsWeight)
		# print "----- ----- -----"
		# print strBestHelm
		# print strBestChest
		# print strBestGauntlet
		# print strBestGreaves
		
		intJust = 35
		print "{}{}{}{}".format("Best Armor:".ljust(15),str(lstfltBestArmor[0]).ljust(intJust),str(lstfltBestArmor[1]).ljust(intJust),str(lstfltBestArmor[2]).ljust(intJust))
		print "{}{}{}{}".format("Weight:".ljust(15),str(lstfltWeight[0]).ljust(intJust),str(lstfltWeight[1]).ljust(intJust),str(lstfltWeight[2]).ljust(intJust))
		print "{}{}{}{}".format("-----".ljust(15),"-----".ljust(intJust),"-----".ljust(intJust),"-----".ljust(intJust))
		print "{}{}{}{}".format("".ljust(15),lststrBestHelm[0].ljust(intJust),lststrBestHelm[1].ljust(intJust),lststrBestHelm[2].ljust(intJust))
		print "{}{}{}{}".format("".ljust(15),lststrBestChest[0].ljust(intJust),lststrBestChest[1].ljust(intJust),lststrBestChest[2].ljust(intJust))
		print "{}{}{}{}".format("".ljust(15),lststrBestGauntlet[0].ljust(intJust),lststrBestGauntlet[1].ljust(intJust),lststrBestGauntlet[2].ljust(intJust))
		print "{}{}{}{}".format("".ljust(15),lststrBestGreaves[0].ljust(intJust),lststrBestGreaves[1].ljust(intJust),lststrBestGreaves[2].ljust(intJust))
		
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

