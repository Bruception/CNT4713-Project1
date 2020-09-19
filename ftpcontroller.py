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

  # TODO: Handle invalid host
  def connect(self):
    self.commandSocket = ftputils.getTCPSocket()
    try:
        self.commandSocket.connect((self.commandHost, self.commandPort))
        self.commandSocketFile = self.commandSocket.makefile('r')
        self.appendToBuffer(f'Successfully connected to {self.commandHost}.')
    except Exception:
        sys.exit(f'Something went wrong connecting to host \'{commandHost}\'.')
    return self.getResponse()

  def login(self, username, password):
    response = self.sendCommandAndGetResponse('USER', username)
    # 331 User name okay, need password.
    if (ftputils.parseResponseStatusCode(response) == '331'):
      response = self.sendCommandAndGetResponse('PASS', password)
    # 230 User logged in, proceed. Logged out if appropriate.
    if (ftputils.parseResponseStatusCode(response) != '230'):
      self.quit()
      sys.exit(self.dumpResponseBuffer())

  """
  We need to issue a PASV command first before any data transfer happens
  PASV response is in the form of: 227 Entering Passive Mode (h1,h2,h3,h4,p1,p2).
  From (h1,h2,h3,h4,p1,p2) we can derive host address and port, so we parse it with parseHostAddressAndPort
  We create a socket to receive/send data from/to the FTP server
  """
  # TODO: Handle failing socket
  def initDataCommand(self, command, argument):
    pasvResponse = self.sendCommandAndGetResponse('PASV')
    dataAddress = ftputils.parseHostAddressAndPort(pasvResponse)
    dataSocket = ftputils.getTCPSocket()
    dataSocket.connect(dataAddress)
    formattedCommand = ftputils.formatCommand(command, argument)
    self.commandSocket.sendall(formattedCommand)
    response = self.getResponse()
    # 550 Requested action not taken. File unavailable (e.g., file not found, no access).
    if (ftputils.parseResponseStatusCode(response) == '550'):
      return response
    return self.handleDataCommand(command, argument, dataSocket)

  def handleDataCommand(self, command, argument, dataSocket):
    if (command == 'LIST' or command == 'RETR'):
      return self.readData(command, argument, dataSocket)
    return self.sendData(argument, dataSocket)

  def readData(self, command, argument, dataSocket):
    dataBuffer = []
    while True:
      line = dataSocket.recv(ftputils.BYTES_PER_LINE)
      if (not line):
        break
      dataBuffer.append(line)
    dataSocket.close()
    # We want to append the results of LIST to the response buffer
    if (command == 'LIST'):
      data = ftputils.joinDataLines(dataBuffer)
      self.appendToBuffer(data)
    else:
      ftputils.writeToFile(argument, dataBuffer)
    return self.getResponse()

  # TODO Handle missing file
  def sendData(self, argument, dataSocket):
    try:
      sourceFile = open(argument, 'rb')
    except FileNotFoundError:
      dataSocket.close()
      self.sendCommandAndGetResponse('ABOR')
      self.dumpResponseBuffer()
      errorString = f'File \'{argument}\' not found within current directory.'
      self.appendToBuffer(errorString)
      return errorString
    while True:
      line = sourceFile.read(ftputils.BYTES_PER_LINE)
      if (not line):
        break
      dataSocket.sendall(line)
    dataSocket.close()
    sourceFile.close()
    return self.getResponse()

  def sendCommandAndGetResponse(self, command, argument=''):
    formattedCommand = ftputils.formatCommand(command, argument)
    if (command in ftputils.DATA_COMMANDS):
      return self.initDataCommand(command, argument)
    self.commandSocket.sendall(formattedCommand)
    return self.getResponse()

  def getResponse(self):
    response = self.commandSocketFile.readline(ftputils.BYTES_PER_LINE)
    self.appendToBuffer(response)
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
