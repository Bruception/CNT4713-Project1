# FTP Utility functions
import re
import socket

FTP_PORT = 21
TEST_HOST = 'inet.cs.fiu.edu'
BYTES_PER_LINE = 8192

DATA_COMMANDS = ['LIST', 'RETR', 'STOR']
FILTER_CODES = ['331', '227']

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
  'mkdir': {
    'command': 'MKD',
    'argument': True,
  },
  'rmdir': {
    'command': 'RMD',
    'argument': True,
  },
}

def parseHostAddressAndPort(response):
  if (parseResponseStatusCode(response) != '227'):
    return ('', 0)
  hostAddressGroups = re.findall(r'\(([0-9^,]+)\)', response)
  stringHostAddress = hostAddressGroups[0].split(',')
  hostAddress = list(map(int, stringHostAddress))
  hostPort = (hostAddress[4] * 256) + hostAddress[5]
  return ('.'.join(stringHostAddress[:4]), hostPort)

def joinDataLines(dataBuffer):
  buffer = []
  for line in dataBuffer:
    decodedLine = formatResponse(line.decode())
    buffer.append(decodedLine)
  return ''.join(buffer)

def writeToFile(fileName, dataBuffer):
  with open(fileName, 'wb') as file:
    for line in dataBuffer:
      file.write(line)
    file.close()

def formatResponse(response):
  if (response and response[-1] == '\n'):
    response = response[0:-1]
  return response

def parseLine(line):
  splitLine = line.split(' ')
  return getCommandAndArgument(splitLine)

def getCommandAndArgument(line):
  userCommand = line[0]
  if (userCommand not in COMMAND_MAP):
    return ('', '')
  commandData = COMMAND_MAP[userCommand]
  command = commandData['command']
  expectingArgument = commandData['argument']
  return (command, line[1] if expectingArgument and 1 < len(line) else '')

def formatCommand(command, argument=''):
  return f'{command} {argument}\r\n'.encode()

def getTCPSocket():
  return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def getFTPLine():
  line = input('ftp> ')
  return line

def parseResponseStatusCode(response):
  splitLine = response[:3]
  return splitLine if splitLine.isdigit() else '500'
