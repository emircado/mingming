#FRONTEND IMPORTS
import pygame
from pygame.locals import *

BLACK     = pygame.Color(   0,   0,   0)
WHITE     = pygame.Color( 255, 255, 255)
GREEN     = pygame.Color(   0, 255,   0)
RED       = pygame.Color( 255,   0,   0)
GRAY      = pygame.Color( 127, 127, 127)
LIGHTGRAY = pygame.Color( 200, 191, 231)

class minggame:

	def __init__(self, screen, host, level):
		self.screen = screen
		self.host = host
		self.level = level

		self.__prepare_resources()

		self.__start_level()

	def __prepare_resources(self):
		self.__images = {
			'arrows':	{	'button_next':	pygame.image.load("resources/arrows/arrow_next.png").convert_alpha(),
							'button_prev':	pygame.image.load("resources/arrows/arrow_prev.png").convert_alpha()	},

		}

	def __start_level(self):
		self.screen.fill(BLACK)

		screen_width = 800
		screen_height = 600
		panel_width = screen_width/3
		panel_height = 389/2

		pygame.draw.line(self.screen, LIGHTGRAY, [0, 211], [screen_width, 211], 1)
        pygame.draw.rect(self.screen, GRAY, [0, 212, panel_width, panel_height])
        # pygame.draw.line(self.screen, LIGHTGRAY, [panel_width, 212], [panel_width, 211+panel_height], 1)
        # pygame.draw.rect(self.screen, GRAY, [panel_width+1, 212, panel_width, panel_height])
        # pygame.draw.line(self.screen, LIGHTGRAY, [2*panel_width, 212], [2*panel_width, 211+panel_height], 1)
        # pygame.draw.rect(self.screen, GRAY, [2*(panel_width)+1, 212, panel_width, panel_height])
        # pygame.draw.line(self.screen, LIGHTGRAY, [0, 212+panel_height], [screen_width, 212+panel_height], 1)
        # pygame.draw.rect(self.screen, GRAY, [0, 213+panel_height, panel_width, panel_height])
        # pygame.draw.line(self.screen, LIGHTGRAY, [panel_width, 213+panel_height], [panel_width, 211+2*panel_height], 1)
        # pygame.draw.rect(self.screen, GRAY, [panel_width+1, 213+panel_height, panel_width, panel_height])
        # pygame.draw.line(self.screen, LIGHTGRAY, [2*panel_width, 213+panel_height], [2*panel_width, 211+2*panel_height], 1)
        # pygame.draw.rect(self.screen, GRAY, [2*(panel_width)+1, 213+panel_height, panel_width, panel_height])
        # pygame.draw.line(self.screen, LIGHTGRAY, [0, 212], [0, 212+2*panel_height], 1)
        # pygame.draw.line(self.screen, LIGHTGRAY, [0, 210+2*panel_height], [screen_width, 210+2*panel_height], 1)
        # pygame.draw.line(self.screen, LIGHTGRAY, [799, 212], [799, 212+2*panel_height], 1)
        # pygame.draw.rect(self.screen, RED, [0, 187, screen_width, 24])

        # pygame.display.update()