import socket
import keygen

BUFSIZE = 4096
#RSA_PUBLIC_KEY, RSA_MOD, RSA_PRIVATE_KEY = getRSAKeypair(1024)
#CONN_RSA = -1
#CONN_MOD = -1
#CONN_AES = -1
CONN_AES = 30

sock = socket.socket()
host = socket.gethostname()
port = 20
sock.bind((host, port))

sock.listen(10)

#Establish connection
conn, addr = sock.accept()
print("Recieved connection from ", addr)
#Send ACK
conn.sendall("ACK".encode())
#Recieve RSA keys
RSA_keys = conn.recv(BUFSIZE).decode()
CONN_RSA, CONN_MOD = RSA_keys.split('|')
print("Key: " + str(CONN_RSA) + ", Modulus: " + str(CONN_MOD))
# Send AES key
conn.sendall(str(CONN_AES).encode())
conn.close()
