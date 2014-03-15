import threading
import mingserver
import mingclient
import socket

class mingming:
	def __init__(self):
		name = raw_input('What is your name? (input -1 to skip)')
		if name != '-1':
			self.__name = name
	
		self.__main_menu()

	def __create_game(self):
		port = int(raw_input('Enter port number: '))
		print 'creating game...'
		mingserver.mingserver(self.__get_ip(), port, self.__name)

	def __join_game(self):
		host = raw_input('Enter IP Address: ')
		port = int(raw_input('Enter port number: '))
		print 'joining game...'
		mingclient.mingclient(host, port, self.__name)

	def __get_ip(self):
		return socket.gethostbyname(socket.gethostname())

	def __about(self):
		print 'This is an MP in CS145'
		print 'MAGNO, Grace'
		print 'MERCADO, Emir'
		print 'YAP, Sharmaine'

		print 'Enter 1 to go back'
		cmd = int(raw_input())

		if cmd == 1:
			self.__main_menu()

	def __main_menu(self):
		print 'Hello '+self.__name
		print 'Ming Ming '+self.__get_ip()
		print 'Choose a command'
		print '1) Create game'
		print '2) Join game'
		print '3) About game'
		cmd = int(raw_input())

		if cmd == 1:
			self.__create_game()
		elif cmd == 2:
			self.__join_game()
		elif cmd == 3:
			self.__about()

def main():
	mingming()

if __name__ == '__main__':
	main()
