import sys
import hashlib


class InitPacket:
  #this should store the details about the file to be sent & what to do with it
  def __init__(self):
    self.commands = ''
    self.blobsize = 0
    self.blob
  
class DataBlob:
  def __init__(self):
    self.data = []
    self.size = 0
    self.hash = 0
  def __init__(self,data):
    self.data = data
    self.size = sys.getsizeof(data)
    self.hash = hashlib.md5(data).hexdigest()
  def update(self,new):
    self.data += new
    
