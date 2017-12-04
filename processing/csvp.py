import csv
a=[]
with open('abhi.csv','rb') as f:
     reader=csv.reader(f)
     i=1
     for coloumn in reader:
            a.append(coloumn[0])
	    
print a
