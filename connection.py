import socket

class _myConnection:

	def __init__(self, s):
		self.mySocket = s

	def sendMessage(self, msg):
		try:
			numBytes = self.mySocket.send(msg)
			return numBytes > 0
		except socket.error as serr:
			print "error occured! " + str(serr)

	def getMessage(self):
		return self.mySocket.recv(1024)

def connection(s):
	return _myConnection(s)