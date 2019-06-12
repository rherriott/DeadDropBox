import sys
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

def send_file_email(email_server,email_port,email_user,email_pass,email_to,email_subj,email_msg):
  mail = MIMEMultipart()
  mail['From'] = email_user
  mail['To'] = email_to
  mail['Subject'] = email_subj
  mail.attach(MIMEText(email_msg,'plain'))
  email_contents = mail.as_string()
  srv = smtplib.SMTP(email_server,email_port)
  srv.starttls()
  srv.login(email_user,email_pass)
  srv.sendmail(email_user,email_to,email_contents)
  srv.quit()

def mail_test():
 send_file_email('smtp.gmail.com',587,'tt4631309@gmail.com','ddb_src_pass','tt4631309@gmail.com','test','test test test test')
