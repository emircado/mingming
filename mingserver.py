import socket
import connection
import traceback
import threading

import Tkinter
import tkSimpleDialog

class mingserver:
	def __init__(self, name, host, port):
		try:
			self.host = host
			self.port = port
			self.__serversocket = socket.socket()
			self.__players = []		#only client connections
			self.__playercount = 1	#self included already

			self.__serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.__serversocket.bind((self.host, self.port))
			print 'Server ready...'

			#threads stoppers
			self.__temp = threading.Event()
			self.__waiting = threading.Event()
			self.__accom = threading.Event()

			self.__host_room()
		except Exception as e:
			traceback.print_exc()

	def __tempfunc_roomevt(self):
		while not self.__temp.is_set():
			Tkinter.Tk().withdraw()
			message = tkSimpleDialog.askstring('Input', 'Enter input')
			message = message.strip()

			if message == 'QUIT':
				self.__leave_room()
			elif message == 'START':
				print 'Starting game!'
			elif message.startswith('REMOVE '):
				self.__remove_player(int(message[:6:-1]))
		print 'done getting inputs'

	def __leave_room(self):
		print 'Exiting game...'

		#remove all players from the room


		#connect dummy to kill socket.accept()
		socket.socket().connect((self.host, self.port))
		self.__serversocket.close()
		self.__temp.set()
		self.__accom.set()
		self.__waiting.set()

	def __remove_player(self, i):
		print "removed player", i

		#inform all clients that player has been removed

	def __wait_for_players(self):
		while not self.__waiting.is_set():
			remote_socket, addr = self.__serversocket.accept()
			remote_connection = connection.connection(remote_socket)
			print(str(addr) + ' connected!')

			self.__players.append((remote_socket, addr, remote_connection))
			self.__playercount+=1

			#receive client messages
			msg_thread = threading.Thread(target = self.__accommodate_client, args = (remote_connection,))
			msg_thread.start()
		print 'done waiting for players'

	def __accommodate_client(self, remote_connection):
		while not self.__accom.is_set():
			message = remote_connection.getMessage()
			
			if message == 'LEAVE':
				for i in range(len(self.__players))

		print 'done accommodating clients'

	def __host_room(self):
		self.__serversocket.listen(5)

		#for game events (quit, start, remove, ...)
		tempthread = threading.Thread(target = self.__tempfunc_roomevt)
		tempthread.start()

		#wait for clients to join
		wait_thread = threading.Thread(target = self.__wait_for_players)
		wait_thread.start()

		