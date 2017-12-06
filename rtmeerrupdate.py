import socket,uiserialcont

sock=socket.socket(socket.AF_UNIX,socket.SOCK_DGRAM)
server_address='/tmp/nest/sock_python_error'
while True:
		datagram =sock.recv(1024)
		runtimeError(int(datagram))
