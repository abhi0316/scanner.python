 "code to receive all user_details"
#! /usr/bin/python

import socket,os,sys,logging,serial
from backarraycode import backarraycode 
from processing import uiserialcont,errorhandling 
bar_serial=serial.Serial('/dev/ttyACM0')
logging.basicConfig(filename='/var/log/nest/servers.log',level=logging.DEBUG)
sock=socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM)
server_address='/run/nest/socket_python_nest'
if os.path.exists(server_address):
	os.remove(server_address)
sock.bind(server_address)
logging.info('serverupandrunning...')
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
		file = datagram[0]
		configfile=f.open(file,'w')
		f.write(datagram[0],",",datagram[1],",",datagram[2],",",datagram[3],",",datagram[4],",",datagram[5],",",datagram[6])
		f.close()
		prefix,suffix=uiserialcont.processInit(datagram) # get prefix and suffix
		errarray=errorhandling.readerror(errorfilepath) # read error from csv
		errorarray=errorhandling.extractdataerror(prefix,suffix,errarray) # generater array from csv
		uiserialcont.genUpdatearray(errorarray) # pass it for processing
		break


def process_break():
	backarray=backarraycode.BackArray
	backarray.interupt_pause()




while True:
	read=bar_serial.readline()
	uiserialcont.pre_suffix(read,prefix,sufix)
