from socket import *
import sys

server = socket(AF_INET, SOCK_STREAM)

hostname = str(sys.argv[1])
portnumber = int(sys.argv[2])
filename = str(sys.argv[3])

server.connect((hostname,portnumber))

message = "GET /" + filename + " HTTP/1.1\n\r\n"

server.sendall(message)


context = server.recv(4096)

print context
