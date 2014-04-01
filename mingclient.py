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

			#THREAD THINGS
			#queue frontend of game proper
			self.cv_game_front = threading.Condition() 
			self.for_game_front = []
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

	def next_game(self):
		self.__status = 'CLIENT_INGAME'

	def send_game_command(self, msg):
		self.__clientconnection.sendMessage('GAME_CMD '+msg)

	def __send_game_update(self, msg):
		self.cv_game_front.acquire()
		self.for_game_front.append(msg)
		self.cv_game_front.notify()
		self.cv_game_front.release()

	#the client either leaves or is kicked out of the room
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

			#in-game status commands
			elif message.startswith('GAME '):
				#game starts
				if message[5:] == 'START':
					self.__status = 'CLIENT_INGAME'
					print 'Game has started'
				elif message[5:] == 'OVER':
					self.__status = 'CLIENT_INROOM'
					print 'Game over'

					#reset game thread things
					self.cv_game_front = threading.Condition() 
					self.for_game_front = []
				elif message[5:] == 'KILL':
					self.exit_room('SERVER_LEFT')
				elif message[5:] == 'NEXT':
					self.__status = 'CLIENT_NEXTGAME'

			elif message.startswith('GAME_UPDATE'):
				self.__send_game_update(message[12:])

		print 'done receiving messages from server'