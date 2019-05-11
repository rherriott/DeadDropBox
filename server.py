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
	otpfile.write(otp[2:].encode('latin-1'))
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
	init_commands = conn.recv(BUFSIZE).decode('latin-1')
	print("Recieved commands: " + str(init_commands) + "\n")
	conn.sendall("ACK".encode('latin-1'))
	return init_commands

def recieve_size(conn):
	init_size = conn.recv(BUFSIZE).decode('latin-1')
	conn.sendall("ACK".encode('latin-1'))
	print("Recieved size: " + str(init_size) + "\n")
	return init_size

def recieve_data(conn, numpacks):
	datastr = ""
	for i in range(numpacks):
		print("Recieving part " + str(i))
		datastr = datastr + conn.recv(BUFSIZE).decode('latin-1')
		conn.sendall("ACK".encode('latin-1'))
	return datastr

def send_data(conn, data):
        print("Sending Data...")
        for i in range(len(data)//BUFSIZE + 1):
                print("Sent: part " + str(i))
                conn.sendall(data[i*BUFSIZE:(i+1)*BUFSIZE].encode('latin-1'))
                conn.recv(BUFSIZE)
        print("Sent all: " + data)

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
        conn.sendall(public_key.encode('latin-1'))
        encrypted_AES_key = conn.recv(BUFSIZE)
        conn.sendall("0".encode('latin-1'))
        nonce = conn.recv(BUFSIZE)
        private_key = RSA.import_key(open("private_key.pem").read())
        k_AES = PKCS1_OAEP.new(private_key).decrypt(encrypted_AES_key)
        return AES.new(k_AES, AES.MODE_EAX, nonce), k_AES

def connHandler(): 
	global GLOBAL_THREADNO
	threadno = str(GLOBAL_THREADNO + 1)
	GLOBAL_THREADNO += 1
	def fail():
		print ("Sending Fail Packet\n")
		#conn.send(lib.ReplyPacket())
	
	s = socket.socket()
	s.bind((HOST, PORT))
	s.listen(MAXWAITS)
	thisthread = str(current_thread())
	print("Thread #" , thisthread ,": Handler started\n")
	sys.stdout.flush()

	conn, addr = s.accept()
	print("Thread #", thisthread ,":",addr, "connected\n")
	sys.stdout.flush()

        #Key Exchange
	AES_key_object, k_AES = get_AES_key(conn)
	print("AES key: " + str(k_AES))
	print("AES nonce: " + str(AES_key_object.nonce))
	sys.stdout.flush()
        
	#Send initial packet
	init_commands = recieve_commands(conn)
	init_size = recieve_size(conn)
	init_data = lib.InitPacket(init_commands, init_size)
	if not init_data:
		print("Thread #", thisthread ,":","Failed, no data recieved\n")
		return
	print("Thread #", thisthread ,":","Received connect from ", repr(addr), "\n")
	print("Thread #", thisthread ,":","\tblob size: ", init_data.blobsize)
	sys.stdout.flush()
	datastr = recieve_data(conn, int(init_data.blobsize)//BUFSIZE + 1)

        #Recieve file
	blob_data = lib.DataBlob(datastr)
	print("Created datablob\n")
	if not blob_data:
		print ("Thread #", thisthread ,":","Failed, blob data not recieved\n")
		fail()
		return
	
	#pull the data from the blob
	if (blob_data.md5hash != hashlib.md5(blob_data.data.encode('latin-1')).hexdigest()):
		print("Thread #", thisthread ,":","Failed, hashes do not match:", blob_data.md5hash, "vs." , hashlib.md5(blob_data.md5hash.encode('latin-1')).hexdigest(), "\n")
		print("Data: " +  str(blob_data.data))
		fail()
		return
	sys.stdout.flush()
	#send reply
	conn.send(blob_data.md5hash.encode('latin-1'))
	print ("Thread #", thisthread ,":","Sent success packet\n")
	sys.stdout.flush()
	#Convert data to binary
	blob_data = lib.DataBlob(''.join(format(ord(i),'b').zfill(8) for i in blob_data.data))
	print("Data: " + blob_data.data)
	
	#Generate OTP of correct length
	generateOTP(threadno, blob_data.size)
	otpfile = open(threadno + OTP_KEY_EXTENSION, "r")
	otp = otpfile.read()
	print("OTP:  " + otp)
	otpfile.seek(0)
		
	outfile = open(str(threadno) + ".blobfile","w+b")
	data_bin = blob_data.data
	#if int(data_bin, 2) % 8 != 0:
		#print("Adding " + str(8 - (int(data_bin, 2) % 8)) + " 0s")
		#data_bin = "0" * (8 - (int(data_bin, 2) % 8)) + data_bin
	otp_bin = otp
	#data_bin = ''.join(format(ord(i),'b') for i in blob_data.data)
	#otp_bin = ''.join(format(ord(i),'b') for i in otp)
	print("Data_binary: " + data_bin)
	print("OTP_binary:  " + otp)
	sys.stdout.flush()
	encstr = ""
	for a, b in zip(data_bin, otp_bin):
		encstr += str(int(a) ^ int(b))
	print("outp1:       " + encstr)
	outfile.write(encstr.encode('latin-1'))
	outfile.close()
	print ("Thread #", thisthread ,":","Wrote recieved data to file\n")
	sys.stdout.flush()
        #Send OTP
	send_data(conn, otp_bin)
	print("Sending ...")
	sys.stdout.flush()
        #Wait for some time
	
	#Reread file
	infile = open(str(threadno) + ".blobfile","r")
	enc = infile.read()
	print("Sending encoded...")
	sys.stdout.flush()
	send_data(conn, enc)
	
	conn.close()
	s.close()
	print ("Thread #", thisthread ,":","closed\n")
	sys.stdout.flush()
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
	sys.stdout.flush()
	#os.flush()
	listenerThreads()
	print("Server Closed\n")
	sys.stdout.flush()
	#os.flush()
	sys.stdout = sys.__stdout__
	#log_file.close()
