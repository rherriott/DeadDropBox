import socket

BUFSIZE = 4096
#RSA_PUBLIC_KEY, RSA_MOD, RSA_PRIVATE_KEY = getRSAKeypair(1024)
RSA_PUBLIC_KEY, RSA_MOD = 10, 20

sock = socket.socket()
host = socket.gethostname()
port = 20

#Establish connection
sock.connect((host, port))

#Recieve ACK
ack = sock.recv(BUFSIZE).decode()
if ack != "ACK":
	print("Connection failed.")
	sock.close()

print(ack)
# Send RSA keys
sock.sendall((str(RSA_PUBLIC_KEY) + "|" + str(RSA_MOD)).encode())
# Recieve AES key
CONN_AES = sock.recv(BUFSIZE).decode()
print(str(CONN_AES))


sock.close()

