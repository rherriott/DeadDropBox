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
  return "cmd1" #Breaks if no content

def get_datablob():
  print("File get not yet implemented")
  #os.flush()
  return "Test" #Breaks if no content

def send_init(s,data):
  initpkt = InitPacket(commands,len(data))
  print("Sending InitPacket:\n\tCommands: "+ str(initpkt.commands) + "\n\tBlobsize: " + str(initpkt.blobsize) + "\n" )
  #os.flush()
  #Send Data
  s.sendall(str(initpkt.commands).encode())
  print("Sent commands.\n")
  s.recv(BUFSIZE)
  s.sendall(str(initpkt.blobsize).encode())
  print("Sent size.\n")
  s.recv(BUFSIZE)
  print("Sent InitPacket")
  
def send_blob(s,data):
  dblob = DataBlob(data)
  print("Sending DataBlob:\n\tSize: "+str(dblob.size)+"\n\tHash: "+ str(dblob.md5hash) +"\n\tData: " + str(dblob.data))
  #os.flush()
  print(type(dblob.data))
  for i in range(dblob.size//BUFSIZE + 1):
    print("Sent: part " + str(i))
    s.sendall(dblob.data[i*BUFSIZE:(i+1)*BUFSIZE].encode())
    s.recv(BUFSIZE)
  print("Sent DataBlob")
  #os.flush()

def recv_reply(s,data):
  rep = s.recv(BUFSIZE).decode()
  print("Recieved ReplyPacket Hash: " + str(rep) + "\n")
  #os.flush()
  return (rep == hashlib.md5(data.encode()).hexdigest())

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
  print("Hash Comparison Check: " + str(valid) + "\n")
  #os.flush()
  s.close()
  print("Connection Closed")
  #os.flush()
  sys.stdout = sys.__stdout__
  #log_file.close()
