import csv

filepath='/home/nest/NEST/nest_python/config/config.csv'
datagram=[]
def readValues():
	with open (filepath,'rb') as f:
                        reader=csv.reader(f)
                        for coloumn in reader:
                                datagram.append(coloumn[0])
                        return datagram

