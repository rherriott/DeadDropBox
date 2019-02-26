# Client recieves arguements
# Client opens connection with server
# Client encrypts file
# Client sends file, arguments
# Client waits for server response
# if server reports all clear, destroy original file
# else, throw execption, release file

#the core server code
from socket import *
import sys
import os
import datetime
#from threading import *
import lib 
import hashlib

###DEFINES
MAXWAITS = 4
HOST = "127.0.0.1" 
PORT = 4321
###END DEFINES

log_file = open("log_" + datetime.datetime.today().isoformat().replace(":","-") + ".txt","w") #I think this will make an ISO timestamped logfile
sys.stdout = log_file #all "print"s go to a logfile

print ("Client started:", datetime.datetime.today().isoformat(),"\n")

#get socket
s = socket(AF_INET, SOCK_STREAM)
#connect to host
s.connect((HOST, PORT)) #https://docs.python.org/2/library/socket.html

print("Connection Closed")
sys.stdout = sys.__stdout__
log_file.close()
