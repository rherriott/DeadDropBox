#the core server code
import socket
import sys
import os
import datetime
from threading import *
import lib #I have no goddamn idea how importing modules works
import hashlib
import keygen
import math
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

###DEFINES
NUMTHREADS = 1 #actual running, 10 maybe? 1 for now since we just need to test that it works at all
MAXWAITS = 10
HOST = socket.gethostbyname(socket.gethostname())
PORT = 4321
BUFSIZE = 4096
OTP_KEY_EXTENSION = ".OTPkey"
GLOBAL_THREADNO = 0
###END DEFINES


def generateOTP(name,length): #returns name of file holding generated One Time Pad
	length = math.ceil(length/8) * 8
	otpname = name + OTP_KEY_EXTENSION
	otpfile = open(otpname, "wb")
	print("Length: " + str(length))
	otp = str(bin(keygen.__getLargeRandom(length)))
	print("Generated: " + otp)
	otpfile.write(otp[2:].encode())
	otpfile.close()
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

def recieve_commands(conn):
	init_commands = conn.recv(BUFSIZE).decode()
	print("Recieved commands: " + str(init_commands) + "\n")
	conn.sendall("ACK".encode())
	return init_commands

def recieve_size(conn):
	init_size = conn.recv(BUFSIZE).decode()
	conn.sendall("ACK".encode())
	print("Recieved size: " + str(init_size) + "\n")
	return init_size

def recieve_data(conn, numpacks):
	datastr = ""
	for i in range(numpacks):
		print("Recieving part " + str(i))
		datastr = datastr + conn.recv(BUFSIZE).decode()
		conn.sendall("ACK".encode())
	return datastr

def get_AES_key(conn):
        if not (os.path.isfile("public_key.pem")):
              RSA_key = RSA.generate(1024)
              private_key = RSA_key.export_key()
              private_file = open("private_key.pem", "wb")
              private_file.write(private_key)

              public_key = RSA_key.publickey().export_key()
              public_file = open("public_key.pem", "wb")
              public_file.write(public_key)
              
        #public_key = RSA.import_key(open("public_key.pem").read())
        public_key = open("public_key.pem").read()
        conn.sendall(public_key.encode())
        encrypted_AES_key = conn.recv(BUFSIZE)
        private_key = RSA.import_key(open("private_key.pem").read())
        return PKCS1_OAEP.new(private_key).decrypt(encrypted_AES_key)

def connHandler(): 
	global GLOBAL_THREADNO
	threadno = str(GLOBAL_THREADNO + 1)
	GLOBAL_THREADNO += 1
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

        #Key Exchange
	k_AES = get_AES_key(conn)
	print("AES key: " + str(k_AES))
        
	#Send initial packet
	init_commands = recieve_commands(conn)
	init_size = recieve_size(conn)
	init_data = lib.InitPacket(init_commands, init_size)
	if not init_data:
		print("Thread #", thisthread ,":","Failed, no data recieved\n")
		return
	print("Thread #", thisthread ,":","Received connect from ", repr(addr), "\n")
	print("Thread #", thisthread ,":","\tblob size: ", init_data.blobsize)
	datastr = recieve_data(conn, int(init_data.blobsize)//BUFSIZE + 1)
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
	
	#send reply
	conn.send(blob_data.md5hash.encode())
	print ("Thread #", thisthread ,":","Sent success packet\n")
	
	#Convert data to binary
	blob_data = lib.DataBlob(''.join(format(ord(i),'b') for i in blob_data.data))
	print("Data: " + blob_data.data)
	#Generate OTP of correct length
	generateOTP(threadno, blob_data.size)
	otpfile = open(threadno + OTP_KEY_EXTENSION, "r")
	otp = otpfile.read()
	print("OTP:  " + otp)
	otpfile.seek(0)
		
	outfile = open("testoutputdata.blobfile","w+b")
	data_bin = blob_data.data
	if int(data_bin, 2) % 8 != 0:
		data_bin = "0" * (8 - (int(data_bin, 2) % 8)) + data_bin
	otp_bin = otp
	#data_bin = ''.join(format(ord(i),'b') for i in blob_data.data)
	#otp_bin = ''.join(format(ord(i),'b') for i in otp)
	print("Data_binary: " + data_bin)
	print("OTP_binary:  " + otp)
	encstr = ""
	for a, b in zip(data_bin, otp_bin):
		encstr += str(int(a) ^ int(b))
	print("outp1:       " + encstr)
	outfile.write(encstr.encode())
	outfile.close()
	print ("Thread #", thisthread ,":","Wrote recieved data to file\n")

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
	for thread in th:
		while thread.isAlive():
			pass


if __name__ == "__main__":
	#log_file = open("log_" + datetime.datetime.today().isoformat().replace(":","-") + ".txt","w") #I think this will make an ISO timestamped logfile
	#sys.stdout = log_file #all "print"s go to a logfile
	print ("Server started:", datetime.datetime.today().isoformat(),"\n")
	listenerThreads()
	print("Server Closed\n")
	sys.stdout = sys.__stdout__
	#log_file.close()
