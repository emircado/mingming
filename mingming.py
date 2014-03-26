#BACKEND IMPORTS
import mingserver
import mingclient
import socket

#FRONTEND IMPORTS
import pygame, sys, os, string
from pygame.locals import *

#TEMPORARY IMPORTS
import Tkinter
import tkSimpleDialog

BLACK     = pygame.Color(   0,   0,   0)
WHITE     = pygame.Color( 255, 255, 255)
GREEN     = pygame.Color(   0, 255,   0)
RED       = pygame.Color( 255,   0,   0)
GRAY      = pygame.Color( 127, 127, 127)
LIGHTGRAY = pygame.Color( 200, 191, 231)

class mingming:
	def __init__(self):
		self.__alias = []

		pygame.init()
		self.clock = pygame.time.Clock()

		self.screen = pygame.display.set_mode((800, 600)) #width, height
		pygame.display.set_caption("Ming Ming")

		os.environ['SDL_VIDEO_CENTERED'] = '1'
		self.font = pygame.font.Font(None, 35)

		self.__prepare_images()

		self.__room_pcoor = [(400,100), (600,100), (400,400), (600,400)]

		self.__active = None

	#preload all images needed
	def __prepare_images(self):
		self.__images = {	
			'about':	{	'background': 	pygame.image.load("resources/about/about_background.png")	},
			
			'main': 	{	'background':	pygame.image.load("resources/main/main_background.png"),
							'button_about':	pygame.image.load("resources/main/main_button_about.png").convert_alpha(),
							'button_host':	pygame.image.load("resources/main/main_button_host.png").convert_alpha(),
							'button_join':	pygame.image.load("resources/main/main_button_join.png").convert_alpha(),
							'button_howto':	pygame.image.load("resources/main/main_button_howto.png").convert_alpha()	},

			'arrows':	{	'button_next':	pygame.image.load("resources/arrows/arrow_next.png").convert_alpha(),
							'button_dnext':	pygame.image.load("resources/arrows/arrow_next_no.png").convert_alpha(),
							'button_prev':	pygame.image.load("resources/arrows/arrow_prev.png").convert_alpha(),
							'button_dprev':	pygame.image.load("resources/arrows/arrow_prev_no.png").convert_alpha()	},

			'whoyou':	{	'background':	pygame.image.load("resources/whoyou/whoyou_background.png")	},

			'howto':	{	'page1':		pygame.image.load("resources/howto/howto_page1.png"),
							'page2':		pygame.image.load("resources/howto/howto_page2.png")	},
			
			'room':		{	'background':	pygame.image.load("resources/room/room_background.png"),
							'btn_start':	pygame.image.load("resources/room/room_button_start.png").convert_alpha(),
							'btn_nostart':	pygame.image.load("resources/room/room_button_nostart.png").convert_alpha(),
							'btn_leave':	pygame.image.load("resources/room/room_button_leave.png").convert_alpha(),
							'btn_kick':		pygame.image.load("resources/room/room_button_kick.png").convert_alpha(),
							'vacant':		pygame.image.load("resources/room/room_vacant.png").convert_alpha(),
							'user_ready':	pygame.image.load("resources/room/room_occ_ready.png").convert_alpha(),
							'user_nready':	pygame.image.load("resources/room/room_occ_notready.png").convert_alpha()	}
			}

	def who_you(self):
		self.__on_display = 'whoyou'

		self.screen.fill(BLACK)
		self.screen.blit(self.__images['whoyou']['background'], (0,0))
		self.__active_buttons = (
			self.screen.blit(self.__images['arrows']['button_next'], (631,491)),	)

		name = self.font.render(string.join(self.__alias, "").replace(',','').replace(':',''), True, BLACK)
		self.screen.blit(name, (430, 285))

	def main_menu(self):
		self.__on_display = 'main'

		self.screen.fill(BLACK)
		self.screen.blit(self.__images['main']['background'], (0,0))
		self.__active_buttons = (
			self.screen.blit(self.__images['main']['button_host'], (364,364)),
			self.screen.blit(self.__images['main']['button_join'], (575,364)),
			self.screen.blit(self.__images['main']['button_about'], (582,492)),
			self.screen.blit(self.__images['main']['button_howto'], (413,492))	)

		#display user alias
		welcome = self.font.render("NI HAO "+self.__alias, True, WHITE)
		self.screen.blit(welcome, (50,50))
		myip = self.font.render(self.__get_ip(), True, WHITE)
		self.screen.blit(myip, (10, 570))

	def create_game(self, new = False):
		self.__on_display = 'host'

		if new == True:
			Tkinter.Tk().withdraw()
			port = int(tkSimpleDialog.askstring('Input', 'Enter port number').strip())
			self.__server = mingserver.mingserver(self.__get_ip(), port, string.join(self.__alias,""))
			self.__myid = self.__server.id
			self.__active = 'server'

		self.screen.fill(BLACK)
		self.screen.blit(self.__images['room']['background'], (0,0))
		self.__active_buttons = (
			self.screen.blit(self.__images['room']['btn_leave'], (30,491)),)	#BUTTON 0: LEAVE
		
		self.players, self.canstart = self.__server.get_players()
		more_buttons = []

		if self.canstart == False:
			more_buttons.append(self.screen.blit(self.__images['room']['btn_nostart'], (631,491)))	#BUTTON 1: START
		else:
			more_buttons.append(self.screen.blit(self.__images['room']['btn_start'], (631,491)))

		for i, (pid, alias, ready) in enumerate(self.players):
			if alias == None:
				more_buttons.append(self.screen.blit(self.__images['room']['vacant'], self.__room_pcoor[i]))	#BUTTON 3-5: VACANT

			else:
				b = None
				if ready == True:
					b = self.screen.blit(self.__images['room']['user_ready'], self.__room_pcoor[i])
				else:
					b = self.screen.blit(self.__images['room']['user_nready'], self.__room_pcoor[i])
				
				if i == 0:
					more_buttons.append(b) #BUTTON 2: SERVER CAT

				#can kick clients
				x, y = self.__room_pcoor[i]
				x += 100
				y += 100
				if i != 0:
					more_buttons.append(self.screen.blit(self.__images['room']['btn_kick'], self.__room_pcoor[i]))	#BUTTON 3-5: KICK

				#display name
				self.screen.blit(self.font.render(alias, True, BLACK), self.__room_pcoor[i])
		
		self.__active_buttons = self.__active_buttons + tuple(more_buttons)

	def join_game(self):
		self.__on_display = 'join'

		Tkinter.Tk().withdraw()
		host = tkSimpleDialog.askstring('Input', 'Enter IP Address').strip()
		Tkinter.Tk().withdraw()
		port = int(tkSimpleDialog.askstring('Input', 'Enter port number').strip())

		print 'joining game...'
		self.__client = mingclient.mingclient(host, port, self.__alias)
		self.__myid = self.__client.id
		self.__active = 'client'

		self.screen.fill(BLACK)
		self.screen.blit(self.__images['room']['background'], (0,0))
		self.__active_buttons = (
			self.screen.blit(self.__images['room']['btn_leave'], (181,491)),)

	def __get_ip(self):
		return socket.gethostbyname(socket.gethostname())

	def about(self):
		self.__on_display = 'about'

		self.screen.fill(BLACK)
		self.screen.blit(self.__images['about']['background'], (0,0))
		self.__active_buttons = (self.screen.blit(self.__images['arrows']['button_prev'], (631,491)),)

	def howto(self, page):
		self.__on_display = 'howto'+str(page)
		
		self.screen.fill(BLACK)
		self.screen.blit(self.__images['howto']['page'+str(page)], (0,0))

		if page == 1:
			self.__active_buttons = (
				self.screen.blit(self.__images['arrows']['button_prev'], (381,491)),
				self.screen.blit(self.__images['arrows']['button_next'], (631,491)))
		if page == 2:
			self.__active_buttons = (self.screen.blit(self.__images['arrows']['button_prev'], (381,491)),)
			self.screen.blit(self.__images['arrows']['button_dnext'], (631,491))

	def start_mingming(self):
		self.who_you()

		#event handling, repainting
		done = False
		while not done:
			for event in pygame.event.get():
				#QUIT GAME
				if event.type == QUIT:
					#leave room if server
					if self.__active == 'server':
						self.__server.leave_room()
					elif self.__active == 'client':
						self.__client.exit_room('LEAVE')
					done = True

				#WHOYOU SCREEN EVENTS
				elif self.__on_display == 'whoyou':
					if event.type == MOUSEBUTTONDOWN:
						for i, b in enumerate(self.__active_buttons):
							if b.collidepoint(pygame.mouse.get_pos()):
								#arrow next
								if i == 0:
									self.__alias = string.join(self.__alias, "")
									self.main_menu()

					#input field
					elif event.type == KEYDOWN:
						if event.key == K_BACKSPACE:
							self.__alias = self.__alias[:-1]
							self.who_you()
						elif event.key == K_RETURN:
							self.__alias = string.join(self.__alias, "")
							self.main_menu()
						else:
							#20 characters limit
							if len(self.__alias) < 21:
								self.__alias.append(event.unicode)
							self.who_you()

				#MAIN SCREEN EVENTS
				elif self.__on_display == 'main':
					if event.type == MOUSEBUTTONDOWN:
						for i, b in enumerate(self.__active_buttons):
							if b.collidepoint(pygame.mouse.get_pos()):
								if i == 0:
									self.create_game(new = True)
								elif i == 1:
									self.join_game()
								elif i == 2:
									self.about()
								elif i == 3:
									self.howto(1)
				
				#ABOUT SCREEN EVENTS
				elif self.__on_display == 'about':
					if event.type == MOUSEBUTTONDOWN:
						for i, b in enumerate(self.__active_buttons):
							if b.collidepoint(pygame.mouse.get_pos()):
								#return back to main menu
								if i == 0:
									self.main_menu()

				#HOW TO PLAY SCREEN EVENTS, page1
				elif self.__on_display == 'howto1':
					if event.type == MOUSEBUTTONDOWN:
						for i, b in enumerate(self.__active_buttons):
							if b.collidepoint(pygame.mouse.get_pos()):
								#return back to main menu
								if i == 0:
									self.main_menu()
								#proceed to next page
								elif i == 1:
									self.howto(2)

				#HOW TO PLAY SCREEN EVENTS, page 2
				elif self.__on_display == 'howto2':
					if event.type == MOUSEBUTTONDOWN:
						for i, b in enumerate(self.__active_buttons):
							if b.collidepoint(pygame.mouse.get_pos()):
								#return to previous page
								if i == 0:
									self.howto(1)
				
				#HOST GAME SCREEN EVENTS
				elif self.__on_display == 'host':
					self.create_game(new = False)
					if event.type == MOUSEBUTTONDOWN:
						for i, b in enumerate(self.__active_buttons):
							if b.collidepoint(pygame.mouse.get_pos()):
								#leave room
								if i == 0:
									self.__server.leave_room()
									del self.__server
									self.__active = None
									self.main_menu()
								#start game
								elif i == 1:
									if self.canstart == True:
										print "start thing"
									else:
										print "can't start this thing!"								
								#set ready
								elif i == 2:
									self.__server.toggle_ready()
									self.create_game(new = False)

								#kick clients if occupied
								elif i >= 3 and i <= 5:
									#occupied
									if self.players[i-2][0] != None:
										self.__server.remove_player(str(self.players[i-2][0]), 'KICK')
										self.create_game(new = False)

				#JOIN GAME SCREEN EVENTS
				elif self.__on_display == 'join':
					if event.type == MOUSEBUTTONDOWN:
						for i, b in enumerate(self.__active_buttons):
							if b.collidepoint(pygame.mouse.get_pos()):
								#leave room
								if i == 0:
									self.__client.exit_room('LEAVE')
									del self.__client
									self.__active = None
									self.main_menu()

			pygame.display.update()
			self.clock.tick(100)
		pygame.quit()
		sys.exit()

def main():
	mingming().start_mingming()

if __name__ == '__main__':
	main()
