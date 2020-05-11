import sys
from socket import *
import time

clientsocket = socket(AF_INET, SOCK_DGRAM)

hostname = str(sys.argv[1])
portnumber = int(sys.argv[2])

i = 0
while(i<10):
	i = i + 1
	starttime = time.time()
	local_time = time.ctime()
	message = "Reply from " + str(hostname)+ ": "+ "Ping " + str(i) + " "+str(local_time)
	clientsocket.sendto(message,(hostname,portnumber))

	clientsocket.settimeout(1)
	
	try:
		data, addr = clientsocket.recvfrom(1024)
		receivetime = time.time()
		rttime = receivetime - starttime
		print(data + '\nRTT: ' + str(rttime))
	except timeout:
		print('Request timed out')
		continue

clientsocket.close() 	
