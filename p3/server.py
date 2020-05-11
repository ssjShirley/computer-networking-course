from socket import *
import sys
import helper

reload(sys)
sys.setdefaultencoding('utf8')

server = socket(AF_INET, SOCK_DGRAM)
server.bind(('',6789))
print("The server is ready to receive")

#receive SYN
clientm, address = server.recvfrom(1024)

server.settimeout(1)

sSeq=0
sAck=eval(clientm)['header'][4]
sLen=1
if(eval(clientm)['header'][1] == 1):
	serverm = { "header": (0,1,1,0,sLen,sSeq,sAck), "data": ''}
	server.sendto(str(serverm), address)
	# print (serverm['header'])


# receive ACK and GET
while True:
	try: 
		clientm, address = server.recvfrom(1024)		
		if (eval(clientm)['header'][0] == 0):
			print("connection establish")
		else:
		 	filename = eval(clientm)["data"].split()[1]
			print(filename)
        		f = open(filename[1:]) 
			break	
	except timeout:
		print("ACK or GET timeout. Resending..")
		server.sendto(str(serverm), address)
		# print (serverm['header'])

flag = 0
outputdata = ''
wholedata = """"""
while True:
	mms = 800
	if (flag == 0):	
		outputdata = f.read(mms)  
		wholedata = wholedata + outputdata		
		sLen=len(outputdata)			
		sSeq=sSeq + sLen
		sAck=sAck + eval(clientm)['header'][4]
	
	if (outputdata == ''):
		break		
	
	serverm = { "header": (0,0,1,0,sLen,sSeq,sAck), "data": outputdata}
	server.sendto(str(serverm), address)
	# print (serverm['header'])

	try:	
		clientm, address = server.recvfrom(1024)
		# print("receive"+str(eval(clientm)['header']))		
		flag = 0
	except timeout:
		print("Packet " + str(sSeq) + " timeout. Resending..")
		flag = 1	


# FIN
md5 = helper.getMD5(wholedata)
print("transmission finish")	
serverm = { "header": (0,0,1,1,1,sSeq,sAck), "data": md5}
server.sendto(str(serverm), address)
# print (serverm['header'])
while True:
	try:	
		clientm, address = server.recvfrom(1024)
		break	
	except timeout:
		print("FIN timeout. Resending..")
		server.sendto(str(serverm), address)
	
server.close()
sys.exit()
