#!/usr/bin/python

#MERCADO, EMIR R.
#2011-04383
#CS 145 ME2

import socket
import connection
import traceback

import threading
import Tkinter
import tkSimpleDialog

def sender(client_connection):
	while True:
		Tkinter.Tk().withdraw()
		message = tkSimpleDialog.askstring('Input', 'Enter input')
		client_connection.sendMessage(message)

		if message.strip() == 'QUIT':
			break

def main():
	try:
		name = 'Client'
		host = raw_input('Enter IP Address: ')
		port  = int(raw_input('Enter Port Number: '))
		
		clientsocket = socket.socket()
		clientconnection = connection.connection(clientsocket)

		print name+' tries to connect to server...'
		clientsocket.connect((host, port))
		print name+' connected!'

		senderthread = threading.Thread(target = sender, args = (clientconnection,))
		senderthread.start()

		while True:
			responses = clientconnection.getMessage().split("\n")

			# print responses
			for res in responses:
				print res

			if len(responses) == 1 and responses[0] == 'Server: Goodbye':
				break
			# response = clientconnection.getMessage().replace("\\n","\n\t")
			# print "Server: "+response

			# if response == 'Goodbye!':
			# 	break

		clientsocket.close()
	except Exception as e:
		traceback.print_exc()

if __name__ == '__main__':
	main()