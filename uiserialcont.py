#! /usr/bin/python2
import RPi.GPIO as GPIO
"algorithm for barcode scanning"
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.OUT)

import numpy as np
import serial,socket,threading,time,logging
from dbcodes import nestdbwrite as db
from backarraycode import backarraycode as bcode
logging.basicConfig(filename='/var/log/nest/servers.log',level=logging.DEBUG)
newarray=[]
barray=[]
errlist=[]
count =0
global ptotal,pansz,barstart,prefix,datalen,suffix,barray
# initiating server for receiving from ui

def processInit(recv_buffer):
	global barray,pansz,barstart,barend,prefix,datalen,suffix
        ptotal= int(recv_buffer[1])
	pansz=int(recv_buffer[2])	
	barstart=int(recv_buffer[4])
	barend=barstart+ptotal
	prefix=int(recv_buffer[3])
	datalen=int(recv_buffer[5])
	suffix=prefix+datalen
	barray=np.arange(barstart,barend+1)
	return barray,prefix,suffix
errbar = []


def restartPgm():
	global errbar,newarray,barray,errlist,count
	newarray=[]
	barray=[]
	errlist=[]
	count =0



"""
#1D array filled with barcoe elements
barray = np.arange(barstart,barend+1)
#print "barray" ,barray#

#print alterarray(barray)
print "errbar",errbar
"""

#converts 1D array into 2D array
def alterarray(aray):
    global pansz
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

#print "orginal", alterarray(barray)

#creates the final array after inserting all errors
def errorarry(barray,errbar=0):
    # modarray = alterarray(barray) 
    if errbar and isinstance(errbar,list) :
		for i in errbar:
			print "DEBUG : ERRBAR NUM : " ,i
			if i not in errlist:
				errlist.append(i)
				print "ERRBAR :", errbar
        			modarray,errornum = inserror(i)
        			print "Number of error Barcodes",errornum
       	 			print "reshape array",modarray,modarray.size
    		
    

			else:
				logging.info("DEBUG: NO CHANGE TO ERR LIST ")
    		return modarray
    if errbar and isinstance(errbar,int):
          if errbar not in errlist:
		if errbar > int(errlist[-1]):
			errlist.append(errbar)
			modarray,errornum = inserror(errbar)
			return modarray
        	else:
			pass
	  else:
		pass
				
    
    else:
	return alterarray(barray)
# serches the barcode position in the array and extracts the row whwere it is found
def search (input,aray):
    coordinates = np.argwhere(aray == input)
    print "coordinates",coordinates
    return aray[coordinates[0,0]]



#input - 1d array filled with barcodes  and array of last error PCB's
# output a 2D array which is shifted according to the errror inserted

def genUpdatearray(errorinput=0):
 	global barray,newarray
	print "DEBUG : ERROR INPUT ",errorinput
	print "DEBUG : BARRAY FROM UISERIALCONT :", barray
	if not errorinput:	
     		newarray = errorarry(barray)
		print "DEBUG : 2D ARRAY NEWARRAY :", newarray
	else:
		newarray= errorarry(barray,errbar=errorinput)
		print "NEW ARRAY :" , newarray



def runtimeError(errorinput):
	global newarray
	newarray=errorarry(barray,errbar=errorinput)
		


# generating backup array to avoid multiple time writing to db
def check_array(input,pannel):
	global bcode
	arrayvar=bcode.BackArray()
	checkvar=arrayvar.checkarray(input)
	if len(checkvar) == 0:
		setarray = arrayvar.setarray(pannel,pansz)
		return True
	else:
		return False

#input - current scanned barcode and 2D shifted barcode


def pre_suffix(code):
	global count,datalen,newarray,prefix,suffix
	count=count+1
	try:
		addprefix=code[0:prefix]
		print "DEBUG : PREFIX LENGTH" ,prefix
		print "DEBUG : SUFFIX LENGTH" ,suffix
		print "DEBUG : PREFIX :",addprefix
		addsuffix=code[suffix:]
		print 'DEBUG : SUFFIX :' , addsuffix
		input=int(code[prefix:suffix])
		print "DEBUG : ENTERED INPUT IS :", input	
		pannel = search(input,newarray)
		chkbarr=check_array(input,pannel)
		if chkbarr:
			for i in range(0,len(pannel)):
				if int(pannel[i])==0:
					pannel_f="ERROR"
				else:
					pan=str(int(pannel[i])).zfill(datalen)
					pannel_f=addprefix+pan+addsuffix
				print "DEBUG : COMPUTEDOUT : ",pannel_f
				db.NestDbInsert(count,pannel_f)
			logging.info( "DEBUG : WROTE TO DB...")
			GPIO.output(14,True)
			time.sleep(4)
			GPIO.output(14,False)
			time.sleep(4)
			logging.info( "DEBUG : BEEP COMPLETE ")
		else:
			count=count-1

	except:
		val="ERROR"
		return val




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

