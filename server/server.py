#the core server code
import socket
import sys
import datetime
from threading import Thread
from ../ import lib as lib
import hashlib

###DEFINES
NUMTHREADS = 10
MAXWAITS = 4
HOST = "127.0.0.1" 
PORT = 4321
###END DEFINES



log_file = open("log_" + datetime.now().isoformat() + ".log","w") #I think this will make an ISO timestamped logfile
sys.stdout = log_file #all "print"s go to a logfile

def connHandler():
    def fail() :
        print "Sending Fail Packet"
        conn.send(lib.ReplyPacket())
        break
        
    thisthread = str(threading.current_thread())
    
    print "Thread #", thisthread ,": Handler started\n"
    conn, addr = s.accept()
    print "Thread #", thisthread ,":",addr, "connected\n"
    #instantiate datablob for all this initial packet to go into
    
    init_date = lib.InitPacket()
    init_data = conn.recv(sys.getsizeof(lib.InitPacket)) #change this to whatever the size of the datatructure we use to start the conn is
    if not init_data:
        print "Failed, no data recieved\n"
        break
    print "Received connect from ", repr(addr), "\n"
    print "\tblob size: ", init_data.size
    blob_data = lib.DataBlob()
    blob_data = conn.recv(init_data.size)
    if not blob_data:
        print "Failed, blob data not recieved\n"
        fail()
        break
    #pull the data from the blob
    if (blob_data.size != sys.getsizeof(blob_data.data))
        print "Failed, blob data not correct length:", blob_data.size , "vs.", sys.getsizeof(blob_data.data) , "\n"
        fail()
        break
    if (blob_data.hash != hashlib.md5(blob_data.hash).hexdigest())
        print "Failed, hashes do not match:", blob_data.hash , "vs." , hashlib.md5(blob_data.hash).hexdigest(), "\n"
        fail()
        break
    #temporary: write the file to disk
    outfile = open("testoutputdata.blobfile","w+b")
    outfile.write(blob_data.data)
    outfile.close()
    
    #send reply
    reply = lib.ReplyPacket(true,blob_data.hash)
    conn.send(reply)
    
    conn.close()

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(MAXWAITS) 

print "Server start:", datetime.now.isoformat()

for i in range(NUMTHREADS):
    Thread(target=connHandler).start()

s.close()

sys.stdout = sys.__stdout__
log_file.close()
