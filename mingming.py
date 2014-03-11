import threading
import mingserver
import mingclient
import socket

class mingming:
	def __init__(self):
		self.__name = input('What is your name? ')
		self.__main_menu()

	def __create_game(self):
		port = int(raw_input('Enter port number: '))
		print 'creating game...'
		mingserver.mingserver(self.__name, self.__get_ip(), port)

	def __join_game(self):
		host = raw_input('Enter IP Address: ')
		port = int(raw_input('Enter port number: '))
		print 'joining game...'
		mingclient.mingclient(self.__name, host, port)

	def __get_ip(self):
		return socket.gethostbyname(socket.gethostname())

	def __about(self):
		print 'This is an MP in CS145'
		print 'MAGNO, Grace'
		print 'MERCADO, Emir'
		print 'YAP, Sharmaine'

		print 'Enter 1 to go back'
		cmd = input()

		if cmd == 1:
			self.__main_menu()

	def __main_menu(self):
		print 'Hello '+self.name
		print 'Ming Ming '+self.get_ip()
		print 'Choose a command'
		print '1) Create game'
		print '2) Join game'
		print '3) About game'
		cmd = input()

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
