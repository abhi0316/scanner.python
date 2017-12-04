#! /usr/bin/python2
"algorithm for barcode scanning"
import numpy as np
import serial,socket,threading,time
from dbcodes import nestdbwrite as db
from backarraycode import backarraycode as bcode

errlist=[]

global ptotal,pansz,barstart,prefix,datalen,suffix,barray
# initiating server for receiving from ui

def processInit(rec_buffer):
        ptotal= int(recv_buffer[0])
	pansz=int(recv_buffer[1])	
	barstart=int(recv_buffer[3])
	barend=barstart+ptotal
	prefix=int(recv_buffer[2])
	datalen=int(recv_buffer[4])
	suffix=prefix+datalen
	barray=np.arange(barstart,barend+1)
	return prefix,suffix
errbar = []

"""
#1D array filled with barcoe elements
barray = np.arange(barstart,barend+1)
#print "barray" ,barray#

#print alterarray(barray)
print "errbar",errbar
"""

#converts 1D array into 2D array
def alterarray(aray):
    pad = np.zeros(abs(aray.size%pansz - pansz))
    aray= np.append(aray,pad)
    # padded = abs(aray.size%pansz - pansz)
    newarray = np.resize(aray,((aray.size/pansz,pansz)))
    return newarray

#insert zeros after the last scanned error barcode and return a new array
def inserror(errorcode):
    global  barray
    foundpos = int(np.argwhere(barray == errorcode))+1
    print"error pos found",foundpos
    errnum = (pansz-foundpos%pansz)
    if foundpos%pansz ==0:
        errnum = 0
    print "errorcode",errorcode
    for i in range(errnum):
        print "current errnum",errnum
        barray=np.insert(barray,foundpos,0)
    modarray= alterarray(barray)
    return modarray,errnum
    # print "inserr bararray",barray
    # alterarray(barray)

print "orginal", alterarray(barray)

#creates the final array after inserting all errors
def errorarry(barray,errbar=0):
    # modarray = alterarray(barray)
    if errbar:
		if errbar not in errlist:
			errlist.append(errbar)
			print "ERRBAR", errbar
        		modarray,errornum = inserror(errbar)
        		print "Number of error Barcodes",errornum
       	 		print "reshape array",modarray,modarray.size
    			return modarray
    

		else:
			print "nothing to change"
    else:
	return alterarray(barray)
# serches the barcode position in the array and extracts the row whwere it is found
def search (input,aray):
    coordinates = np.argwhere(aray == input)
    print "coordinates",coordinates
    return aray[coordinates[0,0]]



#input - 1d array filled with barcodes  and array of last error PCB's
# output a 2D array which is shifted according to the errror inserted

def genUpdatearray(errorinput):
	
	newarray = errorarry(barray)
	newarray= errorarry(barray,errbar=errorinput)
	print "NEW ARRAY" , newarray


# generating backup array to avoid multiple time writing to db
def check_array(input,pannel):
	global bcode
	arrayvar=bcode.BackArray()
	checkvar=arrayvar.checkarray(input)
	if len(checkvar) == 0:
		arrayvar.setarray(pannel,pansz)
		return True
	else:
		return False

#input - current scanned barcode and 2D shifted barcode


def pre_suffix(code,pcount,scount):
	global count,datalen 
	count=count+1
	addprefix=code[0:pcount]
	print "PREFIX",addprefix
	addsuffix=code[scount:]
	print 'SUFFIX' , addsuffix
	input=int(code[pcount:scount])
	print "ENTERED INPUT IS ", input	
	pannel = search(input,newarray)
	chkbarr=check_array(input,pannel)
	if chkbarr:
		for i in range(0,len(pannel)):
			if int(pannel[i])==0:
				pannel_f="ERROR"
			else:
				pan=str(int(pannel[i])).zfill(datalen)
				pannel_f=addprefix+pan+addsuffix
			print "computedout",pannel_f
			db.NestDbInsert(count,pannel_f)
		print "WROTE TO DB..."
	else:
		count=count-1






"""		
	# np.array([backarray,pannel])
def server_threading():
	serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
	host = 'localhost'
	port = 8888
	print "thread started at 8888"
# bind to the port
	serversocket.bind((host, port))

# queue up to 5 requests
	serversocket.listen(5)

	while True:
    	# establish a connection
    		clientfordata,addr = serversocket.accept()
    		print("Got a connection from %s" % str(addr))
		global newarray
	    	while True:
    			recv_data=clientfordata.recv(1024)
			print "recv_data" ,recv_data
        		errorinput= int(recv_data)
			newarray=errorarry(barray,errbar=errorinput)
        		print "fromThreaded:",newarray
			break

"""

"""
t = threading.Thread(target=server_threading)
t.start()
  """

