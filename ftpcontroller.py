#FTP Client Controller
import socket
import ftputils
import sys

class FTPController:
  def __init__(self, host, port=ftputils.FTP_PORT):
    self.commandHost = host
    self.commandPort = port
    self.responseBuffer = []
    self.commandSocket = None
    self.commandSocketFile = None

  def connect(self):
    self.commandSocket = ftputils.getTCPSocket()
    self.commandSocket.connect((self.commandHost, self.commandPort))
    self.commandSocketFile = self.commandSocket.makefile('r')
    self.appendToBuffer(f'Successfully connected to {self.commandHost}.')
    self.appendToBuffer(self.getResponse())

  def initPassiveMode(self):
    response = self.sendCommandAndGetResponse('PASV')
    dataAddress = ftputils.parseHostAddressAndPort(response)
    return dataAddress

  def login(self, username, password):
    response = self.sendCommandAndGetResponse('USER', username)
    if (response[0] == '3'): # 331 User name okay, need password.
      response = self.sendCommandAndGetResponse('PASS', password)
    if (ftputils.parseResponseStatusCode(response) != '230'): # 230 User logged in, proceed. Logged out if appropriate.
      self.quit()
      sys.exit(self.dumpResponseBuffer())

  def sendCommandAndGetResponse(self, command, argument=''):
    formattedCommand = ftputils.formatCommand(command, argument)
    self.commandSocket.sendall(formattedCommand)
    response = self.getResponse()
    self.appendToBuffer(response)
    return response

  def getResponse(self):
    response = self.commandSocketFile.readline(ftputils.BYTES_PER_LINE)
    return response

  def appendToBuffer(self, response):
    # Filter responses we do not want the user to see.
    if (not ftputils.parseResponseStatusCode(response) in ftputils.FILTER_CODES):
      self.responseBuffer.append(ftputils.formatResponse(response))

  def dumpResponseBuffer(self):
    response = '\n'.join(self.responseBuffer)
    self.responseBuffer.clear()
    return response

  def quit(self):
    self.commandSocketFile.close()
    self.commandSocket.close()
