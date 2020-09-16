#FTP Client Controller
import socket
import ftputils
import sys

class FTPController:
  def __init__(self, host, port=ftputils.FTP_PORT):
    self.commandHost = host
    self.commandPort = port
    self.commandSocket = ftputils.getTCPSocket()
    self.commandSocketFile = None

  def connect(self):
    self.commandSocket.connect((self.commandHost, self.commandPort))
    self.commandSocketFile = self.commandSocket.makefile('r')
    print('Successfully connected to', self.commandHost + '.')
    return self.getResponse()

  def initPassiveMode(self):
    response = self.sendCommandAndGetResponse('PASV')
    dataAddress = ftputils.parseHostAddressAndPort(response)
    return dataAddress

  def login(self, username, password):
    response = self.sendCommandAndGetResponse('USER', username)
    if (response[0] == '3'): # 331 User name okay, need password.
      response = self.sendCommandAndGetResponse('PASS', password)
    if (ftputils.parseResponseStatusCode(response) != '230'):
      print('Invalid credentials.')
      sys.exit()
    return response

  def sendCommandAndGetResponse(self, command, argument=''):
    formattedCommand = ftputils.formatCommand(command, argument)
    self.commandSocket.sendall(formattedCommand)
    return self.getResponse()

  def getResponse(self):
    response = self.commandSocketFile.readline(ftputils.BYTES_PER_LINE)
    return ftputils.formatResponse(response)

  def quit(self):
    self.commandSocketFile.close()
    self.commandSocket.close()
