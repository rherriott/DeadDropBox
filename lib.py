import sys
import hashlib
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
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
  def __init__(self, success = False, ret_hash = hashlib.md5("error".encode('latin-1')).hexdigest()):
    self.success = success
    self.ret_hash = ret_hash


def AES_encrypt(key, data):
  a = key.encrypt(data)
  print(type(a))
  return a


def AES_decrypt(key, data):
  return key.decrypt(data.encode('latin-1'))

def send_file_email(email_server,email_port,email_user,email_pass,email_to,email_subj,email_msg,email_filename):
  mail = MIMEMultipart()
  mail['From'] = email_user
  mail['To'] = email_to
  mail['Subject'] = email_subj
  mail.attach(MIMEText(email_msg,'plain'))
  atmt = open(email_filename,'rb')
  part = MIMEBase("application",'octet-stream')
  part.set_payload(atmt.read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition','attachment; filename='+email_filename)
  mail.attach(part)
  email_contents = mail.as_string()
  srv = smtplib.SMTP(email_server,email_port)
  srv.starttls()
  srv.login(email_user,email_pass)
  srv.sendmail(email_user,email_to,email_contents)
  srv.quit()

def send_file_email_quick(address,filename):
 send_file_email('smtp.gmail.com',587,'tt463'+'1309'+'@gm'+'ail.com','ddb_'+'sr'+'c_pass',address,'Your data','Your OTP:',filename)

def mail_test():
 send_file_email('smtp.gmail.com',587,'tt4'+'631309@gm'+'ail.com','dd'+'b_src_p'+'ass','tt46'+'31309@'+'gm'+'ail.'+'com','test','test test test test','requirements.txt')

def wait_dhms(days,hours,minutes,seconds):
  hours = hours + days*24
  minutes = minutes + hours*60
  seconds = seconds + minutes*60
  time.sleep(seconds)
