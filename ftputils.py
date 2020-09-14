# FTP Utility functions
import re
import socket

FTP_PORT = 21
TEST_HOST = 'inet.cs.fiu.edu'
BYTES_PER_LINE = 4096

COMMAND_MAP = {
  'ls': {
    'command': 'LIST',
    'argument': False,
  },
  'cd': {
    'command': 'CWD',
    'argument': True,
  },
  'get': {
    'command': 'RETR',
    'argument': True,
  },
  'put': {
    'command': 'STOR',
    'argument': True,
  },
  'delete': {
    'command': 'DELE',
    'argument': True,
  },
  'quit': {
    'command': 'QUIT',
    'argument': False,
  },
}

# TODO: Add response validation
def parseHostAddressAndPort(response) :
  decodedResponse = response.decode(encoding='utf8')
  hostAddressGroups = re.findall(r'\(([0-9^,]+)\)', decodedResponse)
  stringHostAddress = hostAddressGroups[0].split(',')
  hostAddress = list(map(int, stringHostAddress))
  hostPort = (hostAddress[4] * 256) + hostAddress[5]
  return ('.'.join(stringHostAddress[0:4]), hostPort)

def formatResponse(response):
  if (response[-1] == '\n') :
    response = response[0:-1]
  return response

def parseLine(line):
  splitLine = line.split(' ')
  return getCommandAndArgument(splitLine)

def getCommandAndArgument(line):
  userCommand = line[0]
  if (userCommand not in COMMAND_MAP) :
    return (f'Unknown command {userCommand}.', '')
  commandData = COMMAND_MAP[userCommand]
  command = commandData['command']
  expectingArgument = commandData['argument']
  if (expectingArgument and len(line) == 1) :
    return (f'Argument expected for command {userCommand}.', '')
  if (not expectingArgument and len(line) >= 2) :
    return (f'Argument not expected for command {userCommand}.', '')
  return (command, line[1] if expectingArgument else '')

def formatCommand(command, argument=''):
  return f'{command} {argument}\r\n'.encode()

def getTCPSocket():
  return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def getFTPLine():
  line = input('ftp> ')
  return line

#TODO: Implement parse with validation
def parseResponseStatusCode(response) :
  pass
