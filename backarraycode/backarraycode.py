"code for creating backup array"

import numpy as np
import backarraydb as bdb
backarray=0
count=0
emptyarray=[]
global np

class BackArray:
	
	
	def setarray(self,newarray,coloumn):
		global np,backarray,count
		count=count+1		
		try:
			if backarray == 0:
				backarray=np.array(newarray)
		except:
			backarray=np.append(backarray,newarray)
			backarray=np.resize(backarray,(count,coloumn))
			print backarray
	

	def checkarray(self,input):
		global backarray,emptyarray
		print backarray
		aryexist=np.argwhere(backarray == input)
		print aryexist
		if len(aryexist) == 0:
			print "not found"
		return aryexist
	

	def interupt_pause():
		backarray=backarray.ravel()
		for i in range(0,len(backarray)):
			bdb.backarrayInsert(backarray[i])