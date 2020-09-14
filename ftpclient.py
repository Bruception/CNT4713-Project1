import socket
import re

FTP_PORT = 21
TEST_HOST = 'inet.cs.fiu.edu'

def dec(data) :
  return data.decode(encoding='utf8')

def parseStatusCode(data) :
  pass

def parseHostAddressAndPort(data) :
  print('Parsing ... ', dec(data))
  decodedData = data.decode(encoding='utf8')
  stringHostAddress = re.findall(r'\(([0-9^,]+)', decodedData)[0].split(',')
  hostAddress = list(map(int, stringHostAddress))
  hostPort = (hostAddress[-2] * 256) + hostAddress[-1]
  return ('.'.join(stringHostAddress[0:-2]), hostPort)

controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controlSocket.connect((TEST_HOST, FTP_PORT))

controlSocket.sendall(b'USER demo\r\n')
d = controlSocket.recv(4096)
print(dec(d))

controlSocket.sendall(b'PASS demopass\r\n')
d = controlSocket.recv(4096)
print(dec(d))

controlSocket.sendall(b'PASV\r\n')
d = controlSocket.recv(4096)
print(dec(d))

dataHost, dataPort = parseHostAddressAndPort(d)
dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dataSocket.connect((dataHost, dataPort))

controlSocket.sendall(b'MKD testdir\r\n')
d = controlSocket.recv(4096)
print(dec(d))

controlSocket.sendall(b'LIST\r\n')
d = controlSocket.recv(4096)
print(dec(d))
d = dataSocket.recv(4096)
print(dec(d))
dataSocket.close()

controlSocket.sendall(b'RMD testdir\r\n')
d = controlSocket.recv(4096)
d = controlSocket.recv(4096)
print(dec(d))

controlSocket.close()
