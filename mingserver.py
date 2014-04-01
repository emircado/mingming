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

			#THREAD THINGS
			#queue frontend of game proper
			self.cv_game_front = threading.Condition() 
			self.for_game_front = []

			#threads stoppers
			self.__waiting = threading.Event()

			#start server
			self.__serversocket.listen(5)
			threading.Thread(target = self.__wait_for_players).start()
			
		except Exception as e:
			traceback.print_exc()

	def leave_room(self):
		print 'Exiting game...'

		#kick out all players from the room
		for cid in self.__players.keys():
			self.remove_player(str(cid), 'SERVER_LEFT')

		#connect dummy to kill socket.accept()
		self.__waiting.set()
		socket.socket().connect((self.host, self.port))
		self.__serversocket.close()

	def toggle_ready(self):
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
			self.__sendmsg_toall("GAME START")

	def stop_game(self, means):
		#means could either be
		# OVER - game over for the players
		# KILL - server left the game unexpectedly
		print 'Ending game...'
		self.__playing = False
		self.__sendmsg_toall("GAME "+means)

		if means == 'KILL':
			self.leave_room()

	def next_game(self):
		self.__sendmsg_toall("GAME NEXT")

	def remove_player(self, clientid, means):
		toremove = int(clientid)
		if toremove in self.__players:
			#close connection + stop thread of client to remove
			addr, connection, stopper, alias = self.__players[toremove]
			if means == 'KICK' or means == 'SERVER_LEFT':
				connection.sendMessage(means+' '+clientid)
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
			
	def get_players(self):
		p = [(self.id, self.alias, self.__pready[0])]
		for i in range(1, len(self.__plist)):
			if self.__plist[i] == None:
				p.append((None, None, None))
			else:
				try:
					p.append((self.__plist[i], self.__players[self.__plist[i]][3], self.__pready[i]))
				except Exception:
					p.append((self.__plist[i], '', self.__pready[i]))

		b = True
		if len(self.__players) == 0:
			b = False
		elif False in self.__pready:
			b = False

		return p, b

	#add command to game queue
	def send_game_command(self, msg):
		self.cv_game_front.acquire()
		self.for_game_front.append(msg)
		self.cv_game_front.notify()
		self.cv_game_front.release()

	#send game update to clients
	def send_game_update(self, msg):
		self.__sendmsg_toall('GAME_UPDATE '+msg)

	#send player status to clients
	def __update_players(self):
		message = 'PLAYERS '+str(self.id)+':'+str(self.alias)+':'+str(self.__pready[0])+', '
		for i in range(1, len(self.__plist)):
			message+=str(self.__plist[i])

			if self.__plist[i] == None:
				message+=':None:None'
			else:
				message+=':'+str(self.__players[self.__plist[i]][3])+':'+str(self.__pready[i])
			
			if i+1 != len(self.__plist):
				message+=', '

		self.__sendmsg_toall(message)

	#handles clients connecting to server
	def __wait_for_players(self):
		while not self.__waiting.is_set():
			remote_socket, addr = self.__serversocket.accept()
			remote_connection = connection.connection(remote_socket)
			
			#if server leaves
			if self.__waiting.is_set():
				#to be recieved by the dummy client that closed this thread
				remote_connection.sendMessage('SETID SERVER_DEAD')
				remote_socket.close()
				break

			#room is busy
			if self.__playing == True:
				remote_connection.sendMessage('SETID SERVER_BUSY')
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
					remote_connection.sendMessage('SETID SERVER_FULL')
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

	#send message to all connected clients
	def __sendmsg_toall(self, msg):
		for cid in self.__players:
			addr, connection, stopper, alias = self.__players[cid]

			connection.sendMessage(msg)

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

			#receive game command
			elif message.startswith('GAME_CMD'):
				self.send_game_command(message[9:])

		print 'done accommodating client '+str(cid)

