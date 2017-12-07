import csv
errarray=[] # array of errors
tmperrarray=[]

class errorHandle():

	def readerror(self,filepath):
		with open (filepath,'rb') as f:
			reader=csv.reader(f)
			for coloumn in reader:
				tmperrarray.append(coloumn[0])
			return tmperrarray




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
