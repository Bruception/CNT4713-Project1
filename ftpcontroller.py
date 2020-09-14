#FTP Client Controller
import socket
import ftputils

class FTPController:
  def __init__(self, host, port=ftputils.FTP_PORT):
    self.commandHost = host
    self.commandPort = port
    self.commandSocket = ftputils.getTCPSocket()
    print(self.commandHost, self.commandPort, self.commandSocket)

# def dec(data) :
#   return data.decode(encoding='utf8')

# def parseStatusCode(data) :
#   pass

# controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# controlSocket.connect((TEST_HOST, FTP_PORT))

# controlSocket.sendall(b'USER demo\r\n')
# d = controlSocket.recv(4096)
# print(dec(d))

# controlSocket.sendall(b'PASS demopass\r\n')
# d = controlSocket.recv(4096)
# print(dec(d))

# controlSocket.sendall(b'PASV\r\n')
# d = controlSocket.recv(4096)
# print(dec(d))

# dataHost, dataPort = ftputils.parseHostAddressAndPort(d)
# dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# dataSocket.connect((dataHost, dataPort))

# controlSocket.sendall(b'MKD testdir\r\n')
# d = controlSocket.recv(4096)
# print(dec(d))

# controlSocket.sendall(b'LIST\r\n')
# d = controlSocket.recv(4096)
# print(dec(d))
# d = dataSocket.recv(4096)
# print(dec(d))
# dataSocket.close()

# controlSocket.sendall(b'RMD testdir\r\n')
# d = controlSocket.recv(4096)
# d = controlSocket.recv(4096)
# print(dec(d))

# controlSocket.close()
