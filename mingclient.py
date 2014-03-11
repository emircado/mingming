import socket
import connection
import traceback
import threading

import Tkinter
import tkSimpleDialog

class mingclient:
	def __init__(self, name, host, port):
		try:
			self.__clientsocket = socket.socket()
			self.__clientconnection = connection.connection(self.__clientsocket)

			print 'trying to connect to server '+host+':'+str(port)
			self.__clientsocket.connect((host, port))
			print 'connected!!'

			#thread stoppers
			self.__temp = threading.Event()
			self.__waiting = threading.Event()

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
		self.__clientconnection.sendMessage("LEAVE")


		#stop socket and threads
		self.__clientsocket.close()
		self.__temp.set()

	def __join_game(self):
		#for game events (leave server, ...)
		tempthread = threading.Thread(target = self.__tempfunc_playerevt)
		tempthread.start()

		#get server messages

		