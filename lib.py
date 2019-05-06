import sys
import hashlib

class InitPacket:
  #this should store the details about the file to be sent & what to do with it
  def __init__(self,commands='',blobsize=0):
    self.commands = commands
    self.blobsize = blobsize
  
class DataBlob:
  def __init__(self):
    self.data = []
    self.size = 0
    self.md5hash = 0
  def __init__(self,data = None):
    if data is None:
      self.data = []
      self.size = 0
      self.md5hash = 0
    else:
      self.data = data
      self.size = len(data)
      self.md5hash = hashlib.md5(data.encode()).hexdigest()
  def update(self,new):
    self.data += new
    self.size = sys.getsizeof(data)
    self.md5hash = hashlib.md5(data.encode()).hexdigest()

class ReplyPacket:
  def __init__(self, success = False, ret_hash = hashlib.md5("fug lol".encode()).hexdigest()):
    self.success = success
    self.ret_hash = ret_hash
    
