#FTP Client Controller
import socket
import ftputils

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

  def login(self, username, password):
    response = self.sendCommandAndGetResponse('USER', username)
    if (response[0] == '3') : # 331 User name okay, need password.
      response = self.sendCommandAndGetResponse('PASS', password)
    return response

  def sendCommandAndGetResponse(self, command, argument=''):
    formattedCommand = ftputils.formatCommand(command, argument)
    self.commandSocket.sendall(formattedCommand)
    return self.getResponse()

  def getResponse(self):
    response = self.commandSocketFile.readline(ftputils.BYTES_PER_LINE)
    return ftputils.formatResponse(response)

  def quit(self):
    response = self.sendCommandAndGetResponse('QUIT')
    self.commandSocketFile.close()
    self.commandSocket.close()
    return response
