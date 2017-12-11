
#! /usr/bin/python

import socket,os,sys,logging,serial,uiserialcont,shutil
from backarraycode import backarraycode 
from processing import errorhandling,csvread
from dbcodes import configdb as cdb
from dbcodes import nesterrdbwrite as errdb
errorfilepath="/home/nest/NEST/nest_python/config/error/"
configfile ="/home/nest/NEST/nest_python/config/configs/config.csv"
configwrite="/home/nest/NEST/configs/"
logging.basicConfig(filename='/var/log/nest/servers.log',level=logging.DEBUG)
sock=socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM)
server_address='/run/nest/socket_python_nest'
count =0
try:
	os.makedirs('/run/nest/')
except:
	pass	
if os.path.exists(server_address):
	os.remove(server_address)
sock.bind(server_address)
errarrayfn=errorhandling.errorHandle()
logging.info('serverupandrunning...')
confdb=cdb.SqLiteOperations()
configfilewrite="fileconfig"
def userInterupt():
		errdb.NestDbQuery()
                logging.info("DEBUG : PROGRAM STOPPED BY USER")
                uiserialcont.restartPgm()
                backarryclear=backarraycode.BackArray()
                backarryclear.restartPgm()
                errarrayfn.restartPgm()
                startup()



def startup():
	global configfilewrite,count	
	while True:
		datagram = sock.recv(8000)
		logging.info("data received")
		if os.path.isdir('/tmp/error'):
                        os.system('rm -rf /tmp/error')
		datagram=datagram.split(",")
		"datagram[0] >> configfilename"
		"datagram[1] >> pcbtotal"
		"datagram[2] >> pcbperpannel"
		"datagram[3] >> prefixlength"
		"datagram[4] >> firstdata"
		"datagram[5] >> datalength"
		"""if len(datagram) == 1:
			datagram = confdb.loadConf(datagram[0])
			print "DEBUG : DATAGRAM DB: " ,datagram"""
		if len(datagram) == 1:
			print "datagram is", datagram[0]
			chkconfig=configwrite+datagram[0]
			if os.path.isfile(chkconfig):
				shutil.copy(chkconfig,configfile)
                                logging.info("DEBUG : CONFIG FILE UPLOAD LOCATION")
                                datagram=csvread.readValues()
				os.remove(configfile)			
				
			
		else:   
			configfilewrite=configwrite+datagram[0]
			file=open(configfilewrite,'w+')
			file.write(datagram[0])
			file.write('\n')
			file.write(datagram[1])
			file.write('\n')
			file.write(datagram[2])
                        file.write('\n')
                        file.write(datagram[3])
			file.write('\n')
			file.write(datagram[4])
                        file.write('\n')
                        file.write(datagram[5])
			file.close()
			#confdb.InsertConfig(datagram[0],datagram[1],datagram[2],datagram[3],datagram[4],datagram[5])
		try:	
			barray,prefix,suffix=uiserialcont.processInit(datagram) # get prefix and suffix
			print logging.info("DEBUG : UPDATING SERIALREAD")
			errarrayfn=errorhandling.errorHandle()
			errarray=errarrayfn.readerror(errorfilepath) # read error from csv
			if errarray:
				try:
					errorarray=errarrayfn.extractdataerror(prefix,suffix,errarray) # generater array from csv
					print "DEBUG : EARRAY :", errorarray
					uiserialcont.genUpdatearray(errorarray) # pass it for processing
				
				except:
					file=open('/var/nest/tmp.tmp','w+')
                                	file.write('error')
                                	file.close()
					startup()
                                	break
	
			else:
				uiserialcont.genUpdatearray()
				print "DEBUG : STATNDING HERE"
		except:
			file=open('/var/nest/tmp.tmp','w+')
                        file.write('error')
                        file.close()
                        startup()
	
		break

	bar_serial=serial.Serial('/dev/ttyACM0',timeout=0)
	while True:
		
		if (os.path.isdir('/tmp/error')):
			os.system('rm -rf /tmp/error')
			userInterupt()
        	#print "DEBUG : READY TO SCAN ARRAY POPULATED.."
		try:
                	read=bar_serial.readline()
			if read:
				print "DEBUG : PRINT FROM SERIAL:"
                		val=uiserialcont.pre_suffix(read)

				if val == "ERROR":
					print "ERROR"
					"""
					file=open('/var/nest/tmp.tmp','w+')
					file.write('error')
					file.close() 
					"""
					pass
		except:
			file=open('/var/nest/tmp.tmp','w+')
                       	file.write('error')
                        file.close()
                        break


	startup()

startup()		

