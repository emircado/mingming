import socket
import connection
import traceback
import threading

import Tkinter
import tkSimpleDialog

class mingserver:
	def __init__(self, host, port, name = ''):
		try:
			#problem set requirements
			self.id = 0
			self.alias = name
			self.__idctr = 1

			#other fields
			self.host = host
			self.port = port
			self.__serversocket = socket.socket()
			self.__players = {}		#only client connections
			self.__playercount = 1	#self included already

			self.__serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.__serversocket.bind((self.host, self.port))
			print 'Server ready...'

			#threads stoppers
			self.__temp = threading.Event()
			self.__waiting = threading.Event()

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
		self.__waiting.set()

	def __remove_player(self, clientid, means):
		toremove = -1
		for cid in self.__players:
			addr, connection, stopper = self.__players[cid]

			#close connection + stop thread of client to remove
			if cid == int(clientid):
				connection.mySocket.close()
				stopper.set()
				toremove = cid
			#inform other clients that player has been removed
			else:
				if means == 'LEFT':
					connection.sendMessage('LEFT '+clientid)
				elif means == 'KICK':
					connection.sendMessage('KICK '+clientid)

		del self.__players[toremove]

	#handles clients connecting to server
	def __wait_for_players(self):
		while not self.__waiting.is_set():
			remote_socket, addr = self.__serversocket.accept()
			remote_connection = connection.connection(remote_socket)
			
			#add identifier to client
			remote_connection.sendMessage('SETID '+str(self.__idctr))
			self.__players.update({self.__idctr: (addr, remote_connection, threading.Event())})

			#receive client messages
			msg_thread = threading.Thread(target = self.__clientmsgs, args = (self.__idctr,))
			msg_thread.start()

			print(str(addr) + ' connected! '+str(self.__idctr))
			self.__playercount+=1
			self.__idctr+=1

		print 'done waiting for players'

	#handles client requests (leave, ...)
	def __clientmsgs(self, cid):
		addr, remote_connection, stopper = self.__players[cid]
		while not stopper.is_set():
			message = remote_connection.getMessage()
			
			#certain client leaves room
			if message.startswith('LEAVE'):
				self.__remove_player(message[6:], 'LEFT')

		print 'done accommodating client '+str(cid)

	def __sendmsg_toall(self, msg):
		for skt, addr, con in self.__players:
			con.sendMessage(msg)

	def __host_room(self):
		self.__serversocket.listen(5)

		#for game events (quit, start, remove, ...)
		tempthread = threading.Thread(target = self.__tempfunc_roomevt)
		tempthread.start()

		#wait for clients to join
		wait_thread = threading.Thread(target = self.__wait_for_players)
		wait_thread.start()