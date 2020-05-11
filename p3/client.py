from socket import *
import sys
import helper
import os

reload(sys)
sys.setdefaultencoding('utf8')

client = socket(AF_INET, SOCK_DGRAM)
client.settimeout(1)

hostname = str(sys.argv[1])
portnumber = int(sys.argv[2])
filename = str(sys.argv[3])
newfile = "new_"+filename

cSeq = 0
cAck = 0
cLen = 1
#SYN
clientm = {"header": (0,1,0,0,cLen,cSeq,cAck), "data": ''}
client.sendto(str(clientm), (hostname, portnumber))
# print(clientm['header'])
while True:
	try:
		serverm, addr = client.recvfrom(1024)
		break	
	except timeout:
		print("SYN timeout. Resending..")
		client.sendto(str(clientm), (hostname, portnumber))
		# print(clientm['header'])
		
#ACK
cSeq = cSeq+cLen
cAck = cAck+eval(serverm)["header"][5]
if (eval(serverm)["header"][1] == 1):
	clientm = { "header": (0,0,1,0,cLen,cSeq,cAck), "data": ''}
	client.sendto(str(clientm), (hostname, portnumber))
	# print(clientm['header'])

#GET
clientm = {"header": (1,0,1,0,1,cSeq,cAck), "data": "GET /" + filename + " HTTP/1.1\n\r\n"}
client.sendto(str(clientm), (hostname, portnumber))
# print(clientm['header'])
print("Sending message: \n" + clientm["data"])

if os.path.exists(newfile):
	os.remove(newfile)

writefile = open(newfile,'w')
filedata = """"""
prevdata = """"""
newdata = """"""

while True:
	try:
		prevdata = newdata
		serverm, addr = client.recvfrom(1024)
		if (eval(serverm)['header'][3] == 1):
			break	
		newdata = eval(serverm)['data']
		if (newdata != prevdata):
			filedata = filedata + newdata
			print(newdata)

	except timeout:
		print ("Packet " + str(cSeq) + ' timeout. Resending...')
		client.sendto(str(clientm), (hostname, portnumber))	
		# print(clientm['header'])
		continue	
	
	cSeq = cSeq+cLen
	cAck = cAck+eval(serverm)["header"][4]
	clientm = { "header": (0,0,1,0,cLen,cSeq,cAck), "data": ''}
	client.sendto(str(clientm), (hostname, portnumber))
	# print(clientm['header'])


# FIN
print("original MD5: " + eval(serverm)['data'])
print("new MD5: " + helper.getMD5(filedata))
writefile.write(filedata)
cSeq = cSeq+cLen
cAck = cAck+eval(serverm)["header"][4]
clientm = { "header": (0,0,1,1,cLen,cSeq,cAck), "data": ''}
client.sendto(str(clientm), (hostname, portnumber))
# print(clientm['header'])
while True:
	try:
		serverm, addr = client.recvfrom(1024)
		client.sendto(str(clientm), (hostname, portnumber))
		# print(clientm['header'])
	except timeout:
		break			

writefile.close()
client.close()
sys.exit()

