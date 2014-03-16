import socket
import connection
import traceback
import threading

import Tkinter
import tkSimpleDialog

class mingserver:
	def __init__(self, host, port, alias):
		try:
			#problem set requirements
			self.id = 0
			self.alias = alias
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
			elif message.startswith('KICK '):
				self.__remove_player(message[5:], 'KICK')
		print 'done getting inputs'

	def __leave_room(self):
		print 'Exiting game...'

		#kick out all players from the room
		for cid in self.__players.keys():
			self.__remove_player(str(cid), 'KICK')

		#connect dummy to kill socket.accept()
		self.__temp.set()
		self.__waiting.set()
		socket.socket().connect((self.host, self.port))
		self.__serversocket.close()

	def __remove_player(self, clientid, means):
		toremove = int(clientid)
		if toremove in self.__players:
			#close connection + stop thread of client to remove
			addr, connection, stopper, alias = self.__players[toremove]
			connection.sendMessage('KICK '+clientid)
			connection.mySocket.close()
			stopper.set()
			self.__playercount-=1
			del self.__players[toremove]

			#inform other clients that player has been removed
			for cid in self.__players:
				addr, connection, stopper, alias = self.__players[cid]
				if means == 'LEFT':
					connection.sendMessage('LEFT '+clientid)
				elif means == 'KICK':
					connection.sendMessage('KICK '+clientid)
		else:
			print 'player to remove not found'

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

			#set alias name
			elif message.startswith('SET_ALIAS'):
				self.__players[cid] = self.__players[cid]+(message[10:],)
				print 'client '+str(cid)+' alias set to '+message[10:]

		print 'done accommodating client '+str(cid)

	def __sendmsg_toall(self, msg):
		for skt, addr, con in self.__players:
			con.sendMessage(msg)

	def __host_room(self):
		self.__serversocket.listen(5)

		#for game events (quit, start, remove, ...)
		threading.Thread(target = self.__tempfunc_roomevt).start()

		#wait for clients to join
		threading.Thread(target = self.__wait_for_players).start()