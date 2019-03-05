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
from lib import * 
import hashlib

###DEFINES
MAXWAITS = 4
#HOST = "127.0.0.1" 
#PORT = 4321 #I'm gonna keep this as the default port
###END DEFINES

def get_commands():
  print("Commands not yet implemented")
  os.flush()
  return ""

def get_datablob():
  print("File get not yet implemented")
  os.flush
  return "Test"

log_file = open("log_" + datetime.datetime.today().isoformat().replace(":","-") + ".txt","w") #I think this will make an ISO timestamped logfile
sys.stdout = log_file #all "print"s go to a logfile

print ("Client started:", datetime.datetime.today().isoformat(),"\n")

#get socket
s = socket(AF_INET, SOCK_STREAM) 
#if any socket settings changes are needed, they go here
#connect to host
HOST = input("Host? (default is localhost)") #may have to fix these due to the janky way that I did logging
PORT = input("Port? (default is 4321)")
if not HOST:
  HOST = "localhost"
if not PORT:
  PORT = 4321
s.connect((HOST, PORT)) #https://docs.python.org/2/library/socket.html
commands = get_commands()
data = get_data()
initpkt = InitPacket(commands,len(data))
print("Sending InitPacket:\n\tCommands: "+ initpkt.commands + "\n\tBlobsize: " + self.blobsize + "\n" )
os.flush()
s.send(initpkt)
print("Sent InitPacket") 
dblob = DataBlob(data)
print("Sending DataBlob:\n\tSize: "+dblob.size+"\n\tHash: "+ dblob.md5hash+"\n")
os.flush()

s.send()
rep = s.recv(len(ReplyPacket))
print("Recieved ReplyPacket:\n\tsuccess: " + rep.success + "\n\tHash: " + rep.ret_hash + "\n")
os.flush()
print()

print("Connection Closed")
sys.stdout = sys.__stdout__
log_file.close()

