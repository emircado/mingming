import socket
import connection
import traceback
import threading

import Tkinter
import tkSimpleDialog

class mingclient:
	def __init__(self, host, port, alias):
		try:
			#problem set requirements
			self.alias = alias
			self.id = -1

			self.__ready = False

			#other fields
			self.__clientsocket = socket.socket()
			self.__clientconnection = connection.connection(self.__clientsocket)

			print 'trying to connect to server '+host+':'+str(port)
			self.__clientsocket.connect((host, port))
			print 'connected!!'

			#thread stoppers
			self.__temp = threading.Event()
			self.__server = threading.Event()

			#start client
			self.__start_client()

			#give alias to server
			self.__clientconnection.sendMessage('SET_ALIAS '+alias)

		except Exception as e:
			traceback.print_exc()

	def __tempfunc_playerevt(self):
		while not self.__temp.is_set():
			Tkinter.Tk().withdraw()
			message = tkSimpleDialog.askstring('Input', 'Enter input')
			message = message.strip()

			#leave room
			if message == 'LEAVE':
				self.__exit_room('LEAVE')

			#toggle ready status
			elif message == 'READY':
				self.__ready = False if self.__ready == True else True
				self.__clientconnection.sendMessage('READY '+str(self.id)+' '+str(self.__ready))

		print 'done getting client inputs'

	#the client either leaves or is kicked out of the room
	def __exit_room(self, means = None):
		if means == 'LEAVE':
			print 'Leaving room...'
			self.__clientconnection.sendMessage('LEAVE '+str(self.id))

		elif means == 'KICK':
			print 'You have been kicked out of the room.'

		#stop socket and threads
		self.__temp.set()
		self.__server.set()
		self.__clientsocket.close()

	def __servermsgs(self):
		while not self.__server.is_set():
			message = self.__clientconnection.getMessage()
		
			#connected to server successfully (like an ACK)
			if message.startswith('SETID'):
				clientid = int(message[6:])
				#waiting area is full
				if clientid == -1:
					print 'server is full!'
					self.__exit_room()
				#players are currently playing
				elif clientid == -2:
					print 'A game is currently happening.'
					self.__exit_room()
				#successful entry
				else:
					self.id = clientid
					print 'identifier is '+str(clientid)

			#recieve player list
			elif message.startswith('PLAYERS'):
				print message
				for ready, pid, palias in [x.split(':') for x in message[8:].split(', ')]:
					print ready, pid, palias
				#UPDATE FRONTEND DISPLAYS HERE

			#certain client left room
			elif message.startswith('LEFT'):
				print 'client '+message[5:]+' has left the room'

			#certain client kicked out of room
			elif message.startswith('KICK'):
				#kicked out of room
				if int(message[5:]) == self.id:
					self.__exit_room('KICK')
				else:
					print 'client '+message[5:]+' has been kicked out of the room'

		print 'done receiving messages from server'

	def __start_client(self):
		#for game events (leave server, ...)
		threading.Thread(target = self.__tempfunc_playerevt).start()
		
		#get server messages
		threading.Thread(target = self.__servermsgs).start()