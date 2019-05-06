#the core server code
import socket
import sys
import os
import datetime
from threading import *
import lib #I have no goddamn idea how importing modules works
import hashlib
import keygen

###DEFINES
NUMTHREADS = 1 #actual running, 10 maybe? 1 for now since we just need to test that it works at all
MAXWAITS = 10
HOST = socket.gethostbyname(socket.gethostname())
PORT = 4321
BUFSIZE = 4096
###END DEFINES


def generateOTP(name,length): #returns name of file holding generated One Time Pad   
	otpname = name + ".OTPkey"
	otp = open(otpname, "wb")
	otp.write(os.urandom(length))
	otp.close()
	return otpname

def applyOTP(name,otpname): #returns false if infile is empty, name of file holding result otherwise
	resname = name + "_x_" + otpname
	f1 = open(name,"rb")
	f2 = open(otpname,"rb")
	out = open(resname,"wb")
	byte1 = f1.read(1)
	byte2 = f2.read(1)
	if (not byte1 or not byte2):
		return False
	while(byte1 and byte2):
		bout = bytes([ord(byte1) ^ ord(byte2)])
		out.write(bout)
		byte1 = f1.read(1)
		byte2 = f2.read(1)
	if (not byte1 and byte2):
		print("WARN: infile shorter than key!")
	if (byte1 and not byte2):
		print("WARN: key shorter than infile!")
	#log_file.flush()
	f1.close()
	f2.close()
	out.close()
	return resname 

def connHandler(): #this pretty much needs to be rewritten near-entirely
	def fail():
		print ("Sending Fail Packet\n")
		conn.send(lib.ReplyPacket())
	s = socket.socket()
	s.bind((HOST, PORT))
	s.listen(MAXWAITS)
	thisthread = str(current_thread())
	print("Thread #" , thisthread ,": Handler started\n")
	#log_file.flush()
	conn, addr = s.accept()
	print("Thread #", thisthread ,":",addr, "connected\n")
	#instantiate datablob for all this initial packet to go into
	init_commands = conn.recv(BUFSIZE).decode()
	print("Recieved commands: " + str(init_commands) + "\n")
	conn.sendall("ACK".encode())
	init_size = conn.recv(BUFSIZE).decode()
	conn.sendall("ACK".encode())
	print("Recieved size: " + str(init_size) + "\n")
	init_data = lib.InitPacket(init_commands, init_size)
	if not init_data:
		print("Thread #", thisthread ,":","Failed, no data recieved\n")
		return
	print("Thread #", thisthread ,":","Received connect from ", repr(addr), "\n")
	print("Thread #", thisthread ,":","\tblob size: ", init_data.blobsize)
	datastr = ""
	for i in range(int(init_data.blobsize)//BUFSIZE + 1):
		print("Recieving part " + str(i))
		datastr = datastr + conn.recv(BUFSIZE).decode()
		conn.sendall("ACK".encode())
	blob_data = lib.DataBlob(datastr)
	print("Created datablob\n")
	if not blob_data:
		print ("Thread #", thisthread ,":","Failed, blob data not recieved\n")
		fail()
		return
	#pull the data from the blob
	if (blob_data.md5hash != hashlib.md5(blob_data.data.encode()).hexdigest()):
		print ("Thread #", thisthread ,":","Failed, hashes do not match:", blob_data.hash , "vs." , hashlib.md5(blob_data.hash).hexdigest(), "\n")
		fail()
		return
	#log_file.flush()
	#temporary: write the file to disk
	outfile = open("testoutputdata.blobfile","w+b")
	outfile.write(blob_data.data.encode())
	outfile.close()
	print ("Thread #", thisthread ,":","Wrote recieved data to file\n")
	#send reply
	lib.ReplyPacket(True, blob_data.md5hash)
	conn.send(blob_data.md5hash.encode())
	print ("Thread #", thisthread ,":","Sent success packet\n")
	
	conn.close()
	s.close()
	print ("Thread #", thisthread ,":","closed\n")
	#log_file.flush()

def listenerThreads():
	th = []
	for i in range(NUMTHREADS): #for the constant version of this use threading.activeCount() in a loop
		thr = Thread(target=connHandler, args = ())
		thr.start()
		th.append(thr)
	#log_file.flush()
	for thred in th:
		while thred.isAlive():
			pass


if __name__ == "__main__":
	#log_file = open("log_" + datetime.datetime.today().isoformat().replace(":","-") + ".txt","w") #I think this will make an ISO timestamped logfile
	#sys.stdout = log_file #all "print"s go to a logfile
	print ("Server started:", datetime.datetime.today().isoformat(),"\n")
	listenerThreads()
	print("Server Closed\n")
	sys.stdout = sys.__stdout__
	#log_file.close()
