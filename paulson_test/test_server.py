import socket

sock = socket.socket()
host = socket.gethostname()
port = 20
sock.bind((host, port))

sock.listen(10)

while True:
    conn, addr = sock.accept()
    print("Recieved connection from ", addr)
    conn.send(b"Connection accepted")
    conn.close()
