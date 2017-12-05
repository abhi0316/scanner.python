import csv
errarray=[] # array of errors


class errorHandle():

	def readerror(self,filepath):
		with open (filepath,'rb') as f:
			reader=csv.reader(f)
			for coloumn in reader:
				errarray.append(coloumn[0])
			return errarray




	def extractdataerror(prefix,suffix,array):
		for i in len(array):
			tmparray=array[i]
			errarray.append(int(tmparray[prefix:suffix]))
		return errarray

