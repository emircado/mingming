#!/usr/bin/python

#MERCADO, EMIR R.
#2011-04383
#CS 145 ME1

import socket
import random
import connection
import datetime
import traceback

import threading

def accommodate_client(remote_connection):
	name = 'Server'
	jokes = (
		[	'P1: Ano ang tawag sa anak ng mantika?',
			'P2: Ano?',
			'P1: Edi, baby oil! Wakekeke'],
		[	'Teacher: Juan translate the following. Let\'s help one another',
			'Juan: Tayo\'y magtulungan.',
			'Teacher: Let\'s strive together.',
			'Juan: Tayo\'y magsikap.',
			'Teacher: Because in union there is strength.',
			'Juan: Dahil sa sibuyas may titigas!'],
		[	'Anak: Tay, totoo po bang may multo?',
			'Tatay: Anak walang multo! Bakit mo naitanong?',
			'Anak: Sabi kasi ni yaya merong multo!',
			'Tatay: Anak naman, wala tayong yaya!']
	)

	pickups = (
		[	'Boy: Parol ka ba?',
			'Girl: Bakit?',
			'Boy: Kasi all these years ikaw pa rin ang nakasabit sa puso ko...'],
		[	'Boy: Apoy ka ba?',
			'Girl: Bakit?',
			'Boy: Kasi ALAB u.'],
		[	'Boy: Miss, may banat ako.',
			'Girl: Ano?',
			'Boy: PEDICAB',
			'Girl: Ay, alam ko yan!',
			'Boy: Ha? Sige nga, ano?',
			'Girl: PEDICABang mahalin?']
	)

	months = ('Jan', 'Feb', 'Mar', 'Apr',
		'Sep', 'Oct', 'Nov', 'Dec'
	)

	week = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

	while True:
		message = remote_connection.getMessage()

		if message == 'TIME':
			date = str(datetime.datetime.now())
			day = week[datetime.datetime.today().weekday()]
			response = name+': The time now is '+day+' '+months[int(date[5:7])-1]+' '+date[8:10]+' '+date[11:19]+' PHT '+date[0:4]

			remote_connection.sendMessage(response)
		
		elif message.startswith('MY NAME IS') and len(message[10:].strip()) > 0:
			remote_connection.sendMessage(name+': Hello, '+message[10:].strip())
		
		elif message == 'JOKE TIME':
			response = list(random.choice(jokes))
			for i in range(len(response)):
				response[i] = name+': '+response[i]
			remote_connection.sendMessage("\n".join(response))
		
		elif message == 'PICKUP':
			response = list(random.choice(pickups))
			for i in range(len(response)):
				response[i] = name+': '+response[i]
			remote_connection.sendMessage("\n".join(response))
		
		elif message == 'QUIT':
			remote_connection.sendMessage(name+': Goodbye')
		
		else:
			remote_connection.sendMessage(name+': I can\'t understand what you\'re saying.')
		
		if message == 'QUIT':
			break

	remote_socket.close()


def main():
	try:
		host = ''
		port = int(raw_input('Enter port number: '))
		serversocket = socket.socket()

		serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serversocket.bind((host, port))

		print 'Server ready...'
		serversocket.listen(5)

		while True:
			remote_socket, addr = serversocket.accept()
			remote_connection = connection.connection(remote_socket)
			print(str(addr) + ' connected!')

			remote_thread = threading.Thread(target = accommodate_client, args = (remote_connection,))
			remote_thread.start()

		serversocket.close()
	except Exception as e:
		traceback.print_exc()

if __name__ == '__main__':
	main()