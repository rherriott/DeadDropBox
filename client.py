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

def con():
  #get socket
  s = socket(AF_INET, SOCK_STREAM) 
  #if any socket settings changes are needed, they go here
  #connect to host
  HOST = input("Host? (default is localhost)") #may have to fix these due to the janky way that I did logging
  PORT = input("Port? (default is 4321)")
  if not HOST:          #remember to change these to check formatting eventually
    HOST = "localhost"
  if not PORT:
    PORT = 4321
  try:
    s.connect((HOST, PORT)) #https://docs.python.org/2/library/socket.html
  except socket.error:
    print("Socket failed to connect, quitting.\n")
    raise SystemExit(1)
  return s

def get_commands():
  print("Commands not yet implemented")
  os.flush()
  return ""

def get_datablob():
  print("File get not yet implemented")
  os.flush
  return "Test"

def send_init(s,data):
  initpkt = InitPacket(commands,len(data))
  print("Sending InitPacket:\n\tCommands: "+ initpkt.commands + "\n\tBlobsize: " + self.blobsize + "\n" )
  os.flush()
  #Send Data
  s.send(initpkt)
  print("Sent InitPacket")
  
def send_blob(s,data):
  dblob = DataBlob(data)
  print("Sending DataBlob:\n\tSize: "+dblob.size+"\n\tHash: "+ dblob.md5hash+"\n")
  os.flush()
  s.send(dblob)
  print("Sent DataBlob")
  os.flush()

def recv_reply(s,data):
  rep = s.recv(len(ReplyPacket))
  print("Recieved ReplyPacket:\n\tsuccess: " + rep.success + "\n\tHash: " + rep.ret_hash + "\n")
  os.flush()
  return (ret_hash == hashlib.md5(data).hexdigest())

if __name__ == "__main__":

  log_file = open("log_" + datetime.datetime.today().isoformat().replace(":","-") + ".txt","w") #I think this will make an ISO timestamped logfile
  sys.stdout = log_file #all "print"s go to a logfile
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
  os.flush()
  s.close()
  print("Connection Closed")
  os.flush()
  sys.stdout = sys.__stdout__
  log_file.close()
