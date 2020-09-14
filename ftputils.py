# FTP Utility functions
import re
import socket

FTP_PORT = 21
TEST_HOST = 'inet.cs.fiu.edu'

COMMAND_MAP = {
  'ls': 'LIST',
  'cd': 'CWD',
  'get': 'RETR',
  'put': 'STOR',
  'delete': 'DELE',
  'quit': 'QUIT',
}

# TODO: Add response validation
def parseHostAddressAndPort(response) :
  decodedResponse = response.decode(encoding='utf8')
  hostAddressGroups = re.findall(r'\(([0-9^,]+)\)', decodedResponse)
  stringHostAddress = hostAddressGroups[0].split(',')
  hostAddress = list(map(int, stringHostAddress))
  hostPort = (hostAddress[4] * 256) + hostAddress[5]
  return ('.'.join(stringHostAddress[0:4]), hostPort)

def getCommand(command):
  if (command not in COMMAND_MAP):
    return 'Error, unknown command'
  return COMMAND_MAP[command]

def getTCPSocket():
  return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#TODO: Implement parse with validation
def parseResponseStatusCode(response) :
  pass
