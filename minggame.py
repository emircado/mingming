#BACKEND IMPORTS
from __future__ import division
import threading

#FRONTEND IMPORTS
import pygame
from pygame.locals import *

class level:
	def __init__(self, timer, start, lose, win):
		self.timer = timer
		self.start = start
		self.lose = lose
		self.win = win

BLACK     = pygame.Color(   0,   0,   0)
WHITE     = pygame.Color( 255, 255, 255)
GREEN     = pygame.Color(   0, 255,   0)
RED       = pygame.Color( 255,   0,   0)
GRAY      = pygame.Color( 127, 127, 127)
LIGHTGRAY = pygame.Color( 200, 191, 231)

screen_width = 800
x_pos = screen_width/3
y_pos = 389/2

class minggame:

	def __init__(self, screen, clock, host, lvlnum):
		#frontend things
		self.__screen = screen
		self.__clock = clock
		self.__host = host
		self.__font = pygame.font.Font(None, 35)

		#initialize resources
		self.__prepare_resources()
		self.__lvlnum = lvlnum
		self.__level = self.__levels[self.__lvlnum]
		self.__current = self.__level.start

		#thread stopper
		self.__done = False
		#game status
		self.__game_over = -1

	def __prepare_resources(self):
		self.__levels = {
			1: level(10, 0, -5, 10),
			2: level(10, 0, -5, 10),
			3: level(10, 0, -5, 10),
			4: level(10, 0, -5, 10),
			5: level(10, 0, -5, 10),
			6: level(10, 0, -5, 10),
			7: level(10, 0, -5, 10),
			8: level(10, 0, -5, 10),
			9: level(10, 0, -5, 10),
			10: level(10, 0, -5, 10),
			11: level(10, 0, -5, 10),
			12: level(10, 0, -5, 10),
			13: level(10, 0, -5, 10),
			14: level(10, 0, -5, 10),
			15: level(10, 0, -5, 10)
		}

	def __draw_things(self):
		self.__screen.fill(BLACK)

		pygame.draw.line(self.__screen, GREEN, [0, 171], [self.__timer_len, 171], 30)

		pygame.draw.rect(self.__screen, GRAY, [0, 212, x_pos, y_pos])
		pygame.draw.line(self.__screen, LIGHTGRAY, [x_pos, 212], [x_pos, 211+y_pos], 1)
		pygame.draw.rect(self.__screen, GRAY, [x_pos+1, 212, x_pos, y_pos])
		pygame.draw.line(self.__screen, LIGHTGRAY, [2*x_pos, 212], [2*x_pos, 211+y_pos], 1)
		pygame.draw.rect(self.__screen, GRAY, [2*(x_pos)+1, 212, x_pos, y_pos])
		pygame.draw.line(self.__screen, LIGHTGRAY, [0, 212+y_pos], [screen_width, 212+y_pos], 1)
		pygame.draw.rect(self.__screen, GRAY, [0, 213+y_pos, x_pos, y_pos])
		pygame.draw.line(self.__screen, LIGHTGRAY, [x_pos, 213+y_pos], [x_pos, 211+2*y_pos], 1)
		pygame.draw.rect(self.__screen, GRAY, [x_pos+1, 213+y_pos, x_pos, y_pos])
		pygame.draw.line(self.__screen, LIGHTGRAY, [2*x_pos, 213+y_pos], [2*x_pos, 211+2*y_pos], 1)
		pygame.draw.rect(self.__screen, GRAY, [2*(x_pos)+1, 213+y_pos, x_pos, y_pos])
		pygame.draw.line(self.__screen, LIGHTGRAY, [0, 212], [0, 212+2*y_pos], 1)
		pygame.draw.line(self.__screen, LIGHTGRAY, [0, 210+2*y_pos], [screen_width, 210+2*y_pos], 1)
		pygame.draw.line(self.__screen, LIGHTGRAY, [799, 212], [799, 212+2*y_pos], 1)
		pygame.draw.rect(self.__screen, RED, [0, 187, screen_width, 24])

		self.__screen.blit(self.__font.render("STAGE "+str(self.__lvlnum), True, WHITE), (200,200))
		self.__screen.blit(self.__font.render("CURRENT "+str(self.__current), True, WHITE), (250,250))
		self.__screen.blit(self.__font.render("TIME "+str(self.__countdown), True, WHITE), (300,300))

	def __reset_timer(self):
		#timer things
		self.__countdown = self.__level.timer 	#10, 9, 8, ..., 0
		self.__frame_rate = 60					#60 frames per second
		self.__timer_len = screen_width			#800 is the length of the screen
		self.__frame_count = 0					#second counter

	def __start_timer(self):
		self.__reset_timer()

		while not self.__done:
			self.__frame_count = (self.__frame_count+1)%self.__frame_rate
			self.__timer_len-=(screen_width/self.__level.timer)/self.__frame_rate

			#1 second has passed
			if self.__frame_count == 0:
				self.__countdown-=1

			#timer up
			if self.__countdown == 0:
				self.__send_command('TIMEOUT')
				# self.__

			self.__clock.tick(self.__frame_rate)

	def __send_command(self, msg):
		self.__host.send_game_command(msg)

	#process commands sent by players. SERVER ONLY
	def __process_commands(self):
		while not self.__done:
			self.__host.cv_game_front.acquire()
			#wait while queue is empty
			while len(self.__host.for_game_front) == 0:
				self.__host.cv_game_front.wait()
			self.__host.cv_game_front.release()
			
			#process command
			cmd, pid = self.__host.for_game_front.pop()
			valid = None
			if cmd == 'TIMEOUT':
				valid = False
			elif cmd == 'PFFFT':
				valid = True

			#okay command
			if valid == True:
				self.__current+=1
				self.__host.send_game_update('CURRENT++ '+str(pid))
				#win game
				if self.__current == self.__level.win:
					if self.__lvlnum < 15:
						self.__game_over = False
						self.__host.next_game()
					else:
						self.__game_over = True
						self.__host.stop_game('OVER')
					self.__done = True
				#advance to new command
				elif pid == self.__host.id:
					self.__reset_timer()

			#simulate timeout
			elif valid == False:
				self.__current-=1
				self.__host.send_game_update('CURRENT-- '+str(pid))
				#game over
				if self.__current == self.__level.lose:
					self.__game_over = True
					self.__host.stop_game('OVER')
					self.__done = True
				#advance to new command
				elif pid == self.__host.id:
					self.__reset_timer()			


	#process updates received by client. CLIENT ONLY
	def __process_updates(self):
		while not self.__done:
			self.__host.cv_game_front.acquire()
			#wait while queue is empty
			try:
				while len(self.__host.for_game_front) == 0:
					self.__host.cv_game_front.wait()
				self.__host.cv_game_front.release()
			except RuntimeError:
				pass

			try:
				#process update
				update, pid = self.__host.for_game_front.pop()
				valid = None
				if update == 'CURRENT++':
					valid = True
				elif update == 'CURRENT--':
					valid = False

				#okay command
				if valid == True:
					self.__current+=1
					#win game
					if self.__current == self.__level.win:
						self.__game_over = False if self.__lvlnum < 15 else True
						self.__done = True
					elif pid == self.__host.id:
						self.__reset_timer()

				#simulate timeout
				elif valid == False:
					self.__current-=1
					#game over
					if self.__current == self.__level.lose:
						self.__game_over = True
						self.__done = True
					elif pid == self.__host.id:
						self.__reset_timer()
			except IndexError:
				pass


	def start_game_server(self):
		threading.Thread(target = self.__start_timer).start()
		threading.Thread(target = self.__process_commands).start()

		while not self.__done:
			event = pygame.event.poll()
			self.__draw_things()
			if event.type == QUIT:
				self.__host.stop_game('KILL')
				self.__done = True
			elif event.type == KEYDOWN:
				#command message
				if event.key == K_RETURN:
					self.__send_command('PFFFT')
				
			pygame.display.update()
			
		return self.__game_over

	def start_game_client(self):
		threading.Thread(target = self.__start_timer).start()
		threading.Thread(target = self.__process_updates).start()
		
		while not self.__done:
			event = pygame.event.poll()
			#server closed the room
			if self.__host.get_status() == 'CLIENT_IDLE':
				self.__done = True
			elif self.__host.get_status() == 'CLIENT_INROOM':
				self.__game_over = True
				self.__done = True
			#win game
			elif self.__host.get_status() == 'CLIENT_NEXTGAME':
				self.__game_over = False
				self.__host.next_game()
				self.__done = True
			#game proper
			else:
				self.__draw_things()
				if event.type == QUIT:
					self.__host.exit_room('LEAVE')
					self.__done = True
				elif event.type == KEYDOWN:
					#command message
					if event.key == K_RETURN:
						self.__send_command('PFFFT')

			pygame.display.update()
		return self.__game_over