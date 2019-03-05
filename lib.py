import sys
import hashlib



class InitPacket:
  #this should store the details about the file to be sent & what to do with it
  def __init__(self):
    self.commands = ''
    self.blobsize = 0
  def __init__(self,commands,blobsize):
    self.commands = commands
    self.blobsize = blobsize
  
class DataBlob:
  def __init__(self):
    self.data = []
    self.size = 0
    self.md5hash = 0
  def __init__(self,data):
    self.data = data
    self.size = sys.getsizeof(data)
    self.md5hash = hashlib.md5(data).hexdigest()
  def update(self,new):
    self.data += new
    self.size = sys.getsizeof(data)
    self.md5hash = hashlib.md5(data).hexdigest()

class ReplyPacket:
  def __init__(self):
    self.success = False
    self.ret_hash = hashlib.md5("fug lol").hexdigest()
  def __init__(self, success, ret_hash):
    self.success = success
    self.ret_hash = ret_hash
    
