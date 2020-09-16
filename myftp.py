import sys
import ftputils
from ftpcontroller import FTPController

def initConnection():
  if (len(sys.argv) != 2):
    print('Error, no specified name or IP address of server.')
    return
  hostName = sys.argv[1]
  if (hostName == 'test'):
    hostName = ftputils.TEST_HOST
    ftpController = FTPController(hostName)
    print(ftpController.connect())
    return ftpController
  else:
    print('Invalid host name specified, exiting.')
    return None

def promptLogin(ftpController):
  username = input('Please enter your username: ')
  password = input('Please enter your password: ')
  loginStatusCode = ftpController.login(username, password)
  print(loginStatusCode)
  return loginStatusCode

def readCommands(ftpController):
  readNext = True
  while(readNext):
    line = ftputils.getFTPLine()
    command, argument = ftputils.parseLine(line)
    response = ftpController.sendCommandAndGetResponse(command, argument)
    print(response)
    if (command == 'QUIT'):
      readNext = False

def main():
  ftpController = initConnection()
  if (ftpController == None):
    return
  loginStatusCode = promptLogin(ftpController)
  if (ftputils.parseResponseStatusCode(loginStatusCode) == '230'):
    readCommands(ftpController)
  ftpController.quit()

main()
