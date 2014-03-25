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
			self.__plist = [0, None, None, None]
			self.__pready = [False, None, None, None]
			self.__playing = False

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

			#start server
			self.__start_server()
			
		except Exception as e:
			traceback.print_exc()

	def leave_room(self):
		print 'Exiting game...'

		#kick out all players from the room
		for cid in self.__players.keys():
			self.remove_player(str(cid), 'KICK')

		#connect dummy to kill socket.accept()
		self.__temp.set()
		self.__waiting.set()
		socket.socket().connect((self.host, self.port))
		self.__serversocket.close()

	def set_ready(self):
		self.__pready[0] = False if self.__pready[0] else True
		self.__update_players()
		
	def start_game(self):
		print 'Attempting to start game...'
		if len(self.__players) == 0:
			print 'Can\'t play with only one player'
		elif False in self.__pready:
			print 'Not all players are ready' 
		else:
			self.__playing = True
			print 'Starting game!'

	def remove_player(self, clientid, means):
		toremove = int(clientid)
		if toremove in self.__players:
			#close connection + stop thread of client to remove
			addr, connection, stopper, alias = self.__players[toremove]
			if means == 'KICK':
				connection.sendMessage('KICK '+clientid)
			connection.mySocket.close()
			stopper.set()
			self.__playercount-=1

			del self.__players[toremove]
			for i in range(len(self.__plist)):
				if self.__plist[i] == toremove:
					self.__plist[i] = None
					self.__pready[i] = None
					break

			#inform other clients that player has been removed
			if means == 'LEFT':
				self.__sendmsg_toall('LEFT '+clientid)
			elif means == 'KICK':
				self.__sendmsg_toall('KICK '+clientid)
			self.__update_players()
		else:
			print 'player to remove not found'

	#UI events
	def __tempfunc_roomevt(self):
		while not self.__temp.is_set():
			Tkinter.Tk().withdraw()
			message = tkSimpleDialog.askstring('Input', 'Enter input')
			message = message.strip()

			#quit game (leave room)
			if message == 'QUIT':
				self.leave_room()

			#ready to play
			elif message == 'READY':
				self.set_ready()

			#start game
			elif message == 'START':
				self.start_game()
			
			#kick client out of game
			elif message.startswith('KICK '):
				self.remove_player(message[5:], 'KICK')
		print 'done getting inputs'

	#send player status to clients
	def __update_players(self):
		message = 'PLAYERS '+str(self.__pready[0])+':'+str(self.id)+':'+str(self.alias)+', '
		for i in range(1, len(self.__plist)):
			message+=str(self.__pready[i])

			if self.__plist[i] == None:
				message+=':None:None'
			else:
				message+=':'+str(self.__plist[i])+':'+str(self.__players[self.__plist[i]][3])
			
			if i+1 != len(self.__plist):
				message+=', '

		self.__sendmsg_toall(message)

	#handles clients connecting to server
	def __wait_for_players(self):
		while not self.__waiting.is_set():
			remote_socket, addr = self.__serversocket.accept()
			remote_connection = connection.connection(remote_socket)
			
			#room is busy
			if self.__playing:
				remote_connection.sendMessage('SETID -2')
				remote_socket.close()

			else:
				#determine if room is full
				ind = -1
				for i in range(len(self.__plist)):
					if self.__plist[i] == None:
						ind = i
						break

				#room is full
				if ind == -1:
					remote_connection.sendMessage('SETID -1')
					remote_socket.close()

				#room can accommodate
				else:
					#add identifier to client
					remote_connection.sendMessage('SETID '+str(self.__idctr))
					self.__players.update({self.__idctr: (addr, remote_connection, threading.Event())})

					#add to list of players
					self.__plist[ind] = self.__idctr
					self.__pready[ind] = False	

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
				self.remove_player(message[6:], 'LEFT')

			#set alias name
			elif message.startswith('SET_ALIAS'):
				self.__players[cid] = self.__players[cid]+(message[10:],)
				print 'client '+str(cid)+' alias set to '+message[10:]

				self.__update_players()

			#set to ready
			elif message.startswith('READY'):
				print message
				a, pid, pready = message.split(' ')
				print pid, pready
				for i in range(len(self.__plist)):
					if self.__plist[i] == int(pid):
						self.__pready[i] = True if pready == 'True' else False
						break

				print self.__pready
				self.__update_players()
				#UPDATE GRAHPICS HERE

		print 'done accommodating client '+str(cid)

	def __sendmsg_toall(self, msg):
		for cid in self.__players:
			addr, connection, stopper, alias = self.__players[cid]

			connection.sendMessage(msg)

	def __start_server(self):
		self.__serversocket.listen(5)
		
		#for game events (quit, start, remove, ...)
		threading.Thread(target = self.__tempfunc_roomevt).start()
		
		#wait for clients to join
		threading.Thread(target = self.__wait_for_players).start()