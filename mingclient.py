import socket
import connection
import traceback
import threading
import string
import Queue

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

			self.__players = [['None','None','None'], ['None','None','None'], ['None','None','None'], ['None','None','None']]

			#thread stoppers
			self.__server = threading.Event()

			#start client
			threading.Thread(target = self.__servermsgs).start()

			#game status
			self.__status = None

		except Exception as e:
			traceback.print_exc()

	def get_players(self):
		return self.__players

	def get_status(self):
		return self.__status

	def toggle_ready(self):
		self.__ready = False if self.__ready == True else True
		self.__clientconnection.sendMessage('READY '+str(self.id)+' '+str(self.__ready))

	def send_game_command(self, msg):
		self.__clientconnection.sendMessage('GAME_CMD '+msg+' '+str(self.id))

	def reset_queue(self):
		self.for_game_front = Queue.Queue()

	def __send_game_update(self, msg, pid):
		self.for_game_front.put((msg, pid))

	def exit_room(self, means = None):
		if means == 'LEAVE':
			print 'Leaving room...'
			self.__clientconnection.sendMessage('LEAVE '+str(self.id))

		elif means == 'KICK':
			print 'You have been kicked out of the room.'

		elif means == 'SERVER_FULL':
			print 'The server is full.'

		elif means == 'SERVER_BUSY':
			print 'A game is currently happening.'

		elif means == 'SERVER_LEFT':
			print 'The server closed the room.'

		elif means == 'SERVER_DEAD':
			print 'Dummy connection closed the server.'

		self.__status = 'CLIENT_IDLE'
		#stop socket and threads
		self.__server.set()
		self.__clientsocket.close()

	def __servermsgs(self):
		while not self.__server.is_set():
			message = self.__clientconnection.getMessage()
		
			#connected to server successfully
			if message.startswith('SETID'):
				try:
					self.id = int(message[6:])
					print 'identifier is '+message[6:]

					#give alias to server
					self.__clientconnection.sendMessage('SET_ALIAS '+self.alias)
					self.__status = 'CLIENT_INROOM'
				except ValueError:
					self.exit_room(message[6:])

			#recieve player list
			elif message.startswith('PLAYERS'):
				self.__players = [x.split(':') for x in message[8:].split(', ')]

			#certain client left room
			elif message.startswith('LEFT'):
				print 'client '+message[5:]+' has left the room'

			#certain client kicked out of room
			elif message.startswith('KICK'):
				#kicked out of room
				if int(message[5:]) == self.id:
					self.exit_room('KICK')
				else:
					print 'client '+message[5:]+' has been kicked out of the room'

			#server left the game
			elif message.startswith('SERVER_LEFT'):
				self.exit_room('SERVER_LEFT')

			#game status
			elif message.startswith('GAME '):
				#game starts
				if message[5:] == 'START':
					self.__status = 'CLIENT_INGAME'
					print 'Game has started'
				#server left immediately
				elif message[5:] == 'KILL':
					self.exit_room('SERVER_LEFT')
			#game updates
			elif message.startswith('GAME_UPDATE'):
				print message
				m = string.split(message, 'GAME_UPDATE ')[1:]

				# print message[12:]
				for n in m:
					msg, pid = string.split(n, ' ')
					self.__send_game_update(msg, pid)
				# msg, pid = string.split(message[12:], ' ')
				# self.__send_game_update(msg, pid)

					if msg == 'GAME_OVER':
						self.__status = 'CLIENT_INROOM'

		print 'done receiving messages from server'