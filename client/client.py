# Client recieves arguements
# Client opens connection with server
# Client encrypts file
# Client sends file, arguments
# Client waits for server response
# if server reports all clear, destroy original file
# else, throw execption, release file

# the core client 
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 4321        # The port used by the server

log_file = open("log_" + datetime.now().isoformat() + ".log","w") #I think this will make an ISO timestamped logfile
sys.stdout = log_file #all "print"s go to a logfile

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)

print "Client Online: ", datetime.now.isoformat()