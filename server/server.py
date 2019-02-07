#the core server code
import socket
import sys
import datetime
from threading import Thread

###DEFINES
NUMTHREADS = 10
MAXWAITS = 4
HOST = "127.0.0.1" 
PORT = 4321
###END DEFINES



log_file = open("log_" + datetime.now().isoformat() + ".log","w") #I think this will make an ISO timestamped logfile
sys.stdout = log_file #all "print"s go to a logfile

def clientHandler():
    thisthread = str(threading.current_thread())
    
    print "Thread #", thisthread ,": Handler started"
    conn, addr = s.accept()
    print "Thread #", thisthread ,": ",addr, " connected"
    #instantiate datablob for all this initial packet to go into
    
    
    data = conn.recv(1024) #change this t whatever the size of the datatructure we use to start the conn is
    if not data:
        break
    print "Received connect from ", repr(addr)
    #write the data to the blob
        


s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(MAXWAITS) 

print "Server start: ", datetime.now.isoformat()

for i in range(NUMTHREADS):
    Thread(target=clientHandler).start()

s.close()

sys.stdout = sys.__stdout__
log_file.close()
