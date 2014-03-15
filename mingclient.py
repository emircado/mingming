import socket
import connection
import traceback
import threading

import Tkinter
import tkSimpleDialog

class mingclient:
	def __init__(self, host, port, name = ''):
		try:
			#problem set requirements
			self.alias = name
			self.id = -1

			#other fields
			self.__clientsocket = socket.socket()
			self.__clientconnection = connection.connection(self.__clientsocket)

			print 'trying to connect to server '+host+':'+str(port)
			self.__clientsocket.connect((host, port))
			print 'connected!!'

			#thread stoppers
			self.__temp = threading.Event()
			self.__waiting = threading.Event()
			self.__server = threading.Event()

			self.__join_game()
		except Exception as e:
			traceback.print_exc()

	def __tempfunc_playerevt(self):
		while not self.__temp.is_set():
			Tkinter.Tk().withdraw()
			message = tkSimpleDialog.askstring('Input', 'Enter input')
			message = message.strip()

			if message == 'LEAVE':
				self.__leave_room()
		print 'done getting client inputs'

	def __leave_room(self):
		print 'Leaving room...'
		self.__clientconnection.sendMessage("LEAVE "+str(self.id))

		#stop socket and threads
		self.__clientsocket.close()
		self.__temp.set()
		self.__waiting.set()
		self.__server.set()

	def __servermsgs(self):
		while not self.__server.is_set():
			message = self.__clientconnection.getMessage()
		
			#connected to server successfully (like an ACK)
			if message.startswith('SETID'):
				clientid = int(message[6:])
				if clientid == -1:
					print 'server is full!'
				else:
					self.id = clientid
					print 'identifier is '+str(clientid)

			#certain client left room
			elif message.startswith('LEFT'):
				print 'client '+message[5:]+'has left the room'

			#others
			else:
				print message

		print 'done receiving messages from server'

	def __join_game(self):
		#for game events (leave server, ...)
		tempthread = threading.Thread(target = self.__tempfunc_playerevt)
		tempthread.start()

		#get server messages
		fromserver = threading.Thread(target = self.__servermsgs)
		fromserver.start()
		