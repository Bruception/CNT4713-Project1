import sys
import ftputils
from ftpcontroller import FTPController

def initConnection():
  if (len(sys.argv) != 2):
    print('Error, no specified name or IP address of server.')
    sys.exit()
  hostName = sys.argv[1]
  if (hostName == 'test'):
    hostName = ftputils.TEST_HOST
  ftpController = FTPController(hostName)
  ftpController.connect()
  print(ftpController.dumpResponseBuffer())
  return ftpController

def promptLogin(ftpController):
  username = input('Please enter your username: ')
  password = input('Please enter your password: ')
  ftpController.login(username, password)
  print(ftpController.dumpResponseBuffer())

def readCommands(ftpController):
  readNext = True
  while(readNext):
    line = ftputils.getFTPLine()
    command, argument = ftputils.parseLine(line)
    ftpController.sendCommandAndGetResponse(command, argument)
    print(ftpController.dumpResponseBuffer())
    if (command == 'QUIT'):
      readNext = False

def main():
  ftpController = initConnection()
  promptLogin(ftpController)
  readCommands(ftpController)
  ftpController.quit()

main()
