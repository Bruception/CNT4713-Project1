import sys
import ftputils
from ftpcontroller import FTPController

def main():
  if (len(sys.argv) != 2) :
    print('Error, no specified name or IP address of server.')
    return
  hostName = sys.argv[1]
  if (hostName == 'test'):
    hostName = ftputils.TEST_HOST
  ftpController = FTPController(hostName)
  print(hostName)

main()
