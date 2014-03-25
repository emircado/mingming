#BACKEND IMPORTS
import mingserver
import mingclient
import socket

#FRONTEND IMPORTS
import pygame, sys, os, string
from pygame.locals import *

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
		self.font = pygame.font.Font("resources/ThrowMyHandsUpintheAir.ttf", 35)

		self.__prepare_images()

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
							'page2':		pygame.image.load("resources/howto/howto_page2.png")	}
		}

	def who_you(self):
		self.__on_display = 'whoyou'
		#self.__alias = raw_input('What is your name? (input -1 to skip)').replace(',','').replace(':','')

		self.screen.fill(BLACK)
		self.screen.blit(self.__images['whoyou']['background'], (0,0))
		self.__active_buttons = (
			self.screen.blit(self.__images['arrows']['button_next'], (631,491)),	)

		name = self.font.render(string.join(self.__alias, ""), True, BLACK)
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

		print self.__get_ip()

	def create_game(self):
		self.__on_display = 'host'

		# port = int(raw_input('Enter port number: '))
		port = 8080
		print 'creating game...'
		mingserver.mingserver(self.__get_ip(), port, string.join(self.__alias,""))

	def join_game(self):
		self.__on_display = 'join'

		# host = raw_input('Enter IP Address: ')
		# port = int(raw_input('Enter port number: '))
		host = self.__get_ip()
		port = 8080
		print 'joining game...'
		mingclient.mingclient(host, port, self.__alias)

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
					done = True

				#WHOYOU SCREEN EVENTS
				elif self.__on_display == 'whoyou':
					if event.type == MOUSEBUTTONDOWN:
						for i, b in enumerate(self.__active_buttons):
							if b.collidepoint(pygame.mouse.get_pos()):
								#arrow next
								if i == 0:
									#GET NAME HERE
									self.main_menu()

					#input field
					elif event.type == KEYDOWN:
						if event.key == K_BACKSPACE:
							self.__alias = self.__alias[:-1]
							self.who_you()
						elif event.key == K_RETURN:
							#GET NAME HERE
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
									self.create_game()
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
					print 'IN HOST'

				#JOIN GAME SCREEN EVENTS
				elif self.__on_display == 'join':
					print 'IN JOIN'

			pygame.display.update()
			self.clock.tick(100)
		pygame.quit()
		sys.exit()

def main():
	mingming().start_mingming()

if __name__ == '__main__':
	main()
