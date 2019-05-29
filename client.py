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
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from email.utils import parseaddr

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
  #print("Commands not yet implemented")
  #sys.stdout.flush()
  inp = input("Email Address for return: ")
  com = "|EMAIL|"
  if not inp:
    print("No return address provided, quitting.\n")
    return
  email = parseaddr(inp)[1]
  if (not '@' in email or not '.' in email):
    print("Unacceptable email, quitting.\n")
    return
  com += email + '|'
  return com
    
  return com #Breaks if no content

def get_datablob():
  #print("File get not yet implemented")
  #sys.stdout.flush()
  fname = input("File: ")
  inf = open(fname,"rb")
  buf = inf.read(1)
  t = bytearray()
  while(buf):
    t += buf
    buf = inf.read(100)
  #return "lORem iPsUm" #Breaks if no content
  return t

def send_init(s,data):
  initpkt = InitPacket(commands,len(data))
  print("Sending InitPacket:\n\tCommands: "+ str(initpkt.commands) + "\n\tBlobsize: " + str(initpkt.blobsize) + "\n" )
  print("Data: " + str(data))
  #Send Data
  s.sendall(str(initpkt.commands).encode('latin-1'))
  print("Sent commands.\n")
  s.recv(BUFSIZE)
  s.sendall(str(initpkt.blobsize).encode('latin-1'))
  print("Sent size.\n")
  s.recv(BUFSIZE)
  print("Sent InitPacket")
  return initpkt.blobsize
  
def send_blob(s,data):
  
  dblob = DataBlob(data)
  print("Sending DataBlob:\n\tSize: "+str(dblob.size)+"\n\tHash: "+ str(dblob.md5hash) +"\n\tData: " + str(dblob.data))

  for i in range(dblob.size//BUFSIZE + 1):
    print("Sent: part " + str(i))
    s.sendall(dblob.data[i*BUFSIZE:(i+1)*BUFSIZE].encode('latin-1'))
    s.recv(BUFSIZE)
  print("Sent DataBlob")


def recv_reply(s,data):
  rep = s.recv(BUFSIZE).decode('latin-1')
  print("Recieved ReplyPacket Hash: " + str(rep) + "\n")
  ##os.flush()
  return (rep == hashlib.md5(data).hexdigest())

def send_AES(sock):
  public_key = sock.recv(BUFSIZE).decode('latin-1')
  AES_key = get_random_bytes(16)
  encryped_AES_key = PKCS1_OAEP.new(RSA.import_key(public_key)).encrypt(AES_key)
  AES_key_object = AES.new(AES_key, AES.MODE_EAX)
  sock.sendall(encryped_AES_key)
  sock.recv(BUFSIZE)
  sock.sendall(str(AES_key_object.nonce).encode('latin-1'))
  return AES_key_object, AES_key

def recv_data(sock, numpacks):
  datastr = ""
  for i in range(numpacks):
    print("Recieving part " + str(i))
    datastr = datastr + sock.recv(BUFSIZE).decode('latin-1')
    sock.sendall("ACK".encode('latin-1'))
  return datastr

if __name__ == "__main__":

  #log_file = open("log_" + datetime.datetime.today().isoformat().replace(":","-") + ".txt","w") #I think this will make an ISO timestamped logfile
  #sys.stdout = log_file #all "print"s go to a logfile
  print ("Client started:", datetime.datetime.today().isoformat(),"\n")
  sys.stdout.flush()
  
  #connect
  s = con()
  AES_init_bytes = get_random_bytes(16)
  private_AES_key_object = AES.new(AES_init_bytes, AES.MODE_EAX)
  AES_key_object, conn_AES = send_AES(s)
  print("AES key: " + str(conn_AES))
  print("AES nonce: " + str(AES_key_object.nonce))
  sys.stdout.flush()
  
  #Prompt user for commands
  commands = get_commands()

  #Create data object
  data = AES_encrypt(private_AES_key_object, get_datablob())
  
  size = send_init(s,data)
  send_blob(s,data.decode('latin-1'))
  
  #Wait for reply
  valid = recv_reply(s,data)
  print("Hash Comparison Check: " + str(valid) + "\n")
  sys.stdout.flush()
  
  #Recieve OTP
  otp = recv_data(s, size//BUFSIZE + 1)
  file = open("otp", 'w')
  file.write(otp)
  file.close()

  #Wait

  #Recieve OTP ^ Data
  xor = recv_data(s, size//BUFSIZE + 1)

  print("Recieved encoded: \n" + str(xor))
  sys.stdout.flush()
  
  otp_file = open("otp", 'r')
  otp = otp_file.read()
  data = ""
  for a, b in zip(xor, otp):
    data += str(int(a) ^ int(b))

  print("Read otp: \n" + otp)

  print("Got data: \n" + data)
  sys.stdout.flush()
  
  enc_data = ""
  for i in range(len(data)//8):
    enc_data += chr(int(data[i*8:i*8 + 8], 2))

  print("Encrypted data:" + enc_data)
  sys.stdout.flush()
  
  print(AES_decrypt(AES.new(AES_init_bytes, AES.MODE_EAX, private_AES_key_object.nonce), enc_data))
  s.close()
  print("Connection Closed")
  sys.stdout.flush()

  #sys.stdout = sys.__stdout__
  #log_file.close()
