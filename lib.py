import sys
import hashlib
from Crypto.Cipher import AES

class InitPacket:
  #this should store the details about the file to be sent & what to do with it
  def __init__(self,commands='',blobsize=0):
    self.commands = commands
    self.blobsize = blobsize
  
class DataBlob:
  def __init__(self,data = None):
    if data is None:
      self.data = []
      self.size = 0
      self.md5hash = 0
    else:
      self.data = data
      self.size = len(data)
      self.md5hash = hashlib.md5(data.encode('latin-1')).hexdigest()
  def update(self,new):
    self.data += new
    self.size = len(data)
    self.md5hash = hashlib.md5(data.encode('latin-1')).hexdigest()

class ReplyPacket:
  def __init__(self, success = False, ret_hash = hashlib.md5("fug lol".encode('latin-1')).hexdigest()):
    self.success = success
    self.ret_hash = ret_hash


def AES_encrypt(key, data):
  a = key.encrypt(data.encode('latin-1'))
  print(type(a))
  return a


def AES_decrypt(key, data):
  return key.decrypt(data.encode('latin-1'))
