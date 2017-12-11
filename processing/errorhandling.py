import csv
import os
errarray=[] # array of errors
tmperrarray=[]

class errorHandle():

	def readerror(self,filepath):
		filenames=os.listdir(filepath)
		try:
			filename=filepath+filenames[0]
			print "DEBUG : FILE NAME IS",filename
				
			with open (filename,'rb') as f:
				reader=csv.reader(f)
				for coloumn in reader:
					coloumnval=coloumn[0].split()
					if coloumnval:
						tmperrarray.append(coloumnval)
				os.remove(filename)
				return tmperrarray
		except:
			print "DEBUG : ERROR OCCURED IN OPEN FILE"
			array=0
			return array 



	def extractdataerror(self,prefix,suffix,array):
		global errarray
		print len(array)
       		for i in range(0,len(array)):
			tmparray=array[i]
			errarray.append(int(tmparray[prefix:suffix]))
		errarray=sorted(errarray)
		return errarray


	def restartPgm(self):
		global errarray,tmperrarray
		errarray=[]
		tmperrarray=[]
