
#! /usr/bin/python

import socket,os,sys,logging,serial,uiserialcont
from backarraycode import backarraycode 
from processing import errorhandling
from dbcodes import configdb as cdb
errorfilepath="/home/nest/NEST/nest_python/config/error.csv"
file ="config/"
bar_serial=serial.Serial('/dev/ttyACM0')
logging.basicConfig(filename='/var/log/nest/servers.log',level=logging.DEBUG)
sock=socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM)
server_address='/run/nest/socket_python_nest'
if os.path.exists(server_address):
	os.remove(server_address)
sock.bind(server_address)
logging.info('serverupandrunning...')
confdb=cdb.SqLiteOperations()

while True:
		datagram = sock.recv(8000)
		logging.info("data received")
		datagram=datagram.split(",")
		"datagram[0] >> configfilename"
		"datagram[1] >> pcbtotal"
		"datagram[2] >> pcbperpannel"
		"datagram[3] >> prefixlength"
		"datagram[4] >> firstdata"
		"datagram[5] >> datalength"
		if len(datagram) == 1:
			datagram = confdb.loadConf(datagram[0])
			print "DEBUG : DATAGRAM DB: " ,datagram
		else:
			confdb.InsertConfig(datagram[0],datagram[1],datagram[2],datagram[3],datagram[4],datagram[5])

		barray,prefix,suffix=uiserialcont.processInit(datagram) # get prefix and suffix
		print "DEBUG : BARRAY :", barray
		errarrayfn=errorhandling.errorHandle()
		errarray=errarrayfn.readerror(errorfilepath) # read error from csv
		errorarray=errarrayfn.extractdataerror(prefix,suffix,errarray) # generater array from csv
		print "DEBUG : EARRAY :", errorarray
		uiserialcont.genUpdatearray(errorarray) # pass it for processing
		break


def process_break():
	backarray=backarraycode.BackArray
	backarray.interupt_pause()




while True:
	print "DEBUG : READY TO SCAN ARRAY POPULATED.."
	read=bar_serial.readline()
	uiserialcont.pre_suffix(read,prefix,suffix)
