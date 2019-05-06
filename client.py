# Client recieves arguements
# Client opens connection with server
# Client encrypts file
# Client sends file, arguments
# Client waits for server response
# if server reports all clear, destroy original file
# else, throw execption, release file

#the core server code
import socket
import sys
import os
import datetime
#from threading import *
from lib import * 
import hashlib
import keygen

###DEFINES
MAXWAITS = 10
BUFSIZE = 4096
#HOST = "127.0.0.1" 
#PORT = 4321 #I'm gonna keep this as the default port
###END DEFINES

def con():
  #get socket
  s = socket.socket() 
  #if any socket settings changes are needed, they go here
  #connect to host
  HOST = input("Host? (default is localhost)") #may have to fix these due to the janky way that I did logging
  PORT = input("Port? (default is 4321)")
  if not HOST:          #remember to change these to check formatting eventually
    HOST = socket.gethostbyname(socket.gethostname())
  if not PORT:
    PORT = 4321

  s.connect((HOST, PORT)) #https://docs.python.org/2/library/socket.html
  return s

def get_commands():
  print("Commands not yet implemented")
  #os.flush()
  return ""

def get_datablob():
  print("File get not yet implemented")
  #os.flush()
  return "Test"

def send_init(s,data):
  initpkt = InitPacket(commands,len(data))
  print("Sending InitPacket:\n\tCommands: "+ str(initpkt.commands) + "\n\tBlobsize: " + str(initpkt.blobsize) + "\n" )
  #os.flush()
  #Send Data
  s.sendall(str(initpkt.commands).encode())
  s.sendall(str(initpkt.blobsize).encode())
  print("Sent InitPacket")
  
def send_blob(s,data):
  dblob = DataBlob(data)
  print("Sending DataBlob:\n\tSize: "+str(dblob.size)+"\n\tHash: "+ str(dblob.md5hash) +"\n")
  #os.flush()
  s.send(dblob)
  print("Sent DataBlob")
  #os.flush()

def recv_reply(s,data):
  rep = s.recv(len(ReplyPacket))
  print("Recieved ReplyPacket:\n\tsuccess: " + str(rep.success) + "\n\tHash: " + str(rep.ret_hash) + "\n")
  #os.flush()
  return (ret_hash == hashlib.md5(data).hexdigest())

if __name__ == "__main__":

  #log_file = open("log_" + datetime.datetime.today().isoformat().replace(":","-") + ".txt","w") #I think this will make an ISO timestamped logfile
  #sys.stdout = log_file #all "print"s go to a logfile
  print ("Client started:", datetime.datetime.today().isoformat(),"\n")
  
  #connect
  s = con()
  commands = get_commands()
  data = get_datablob()
  send_init(s,data)
  send_blob(s,data)
  #Wait for reply
  valid = recv_reply(s,data)
  print("Hash Comparison Check: " + valid + "\n")
  #os.flush()
  s.close()
  print("Connection Closed")
  #os.flush()
  sys.stdout = sys.__stdout__
  #log_file.close()
