import socket,uiserialcont
sock=socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM)
server_address='/run/nest/socket_error_nest.Socket'
while True:
		datagram =sock.recv(1024)
		if len(datagram) == 2:
			uiserialcont.runtimeError(int(datagram[1]))
		else: 
			startupserver.userInterupt()
