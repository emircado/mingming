#BACKEND IMPORTS
from __future__ import division
import threading
import mingpanel
import string

#FRONTEND IMPORTS
import pygame
import pyganim
from pygame.locals import *

class level:
	def __init__(self, timer, lose, win, cat):
		self.timer = timer
		self.start = 0
		self.lose = lose
		self.win = win
		self.cat = cat

BLACK     = pygame.Color(   0,   0,   0)
WHITE     = pygame.Color( 255, 255, 255)
GREEN     = pygame.Color(   0, 255,   0)
RED       = pygame.Color( 255,   0,   0)
GRAY      = pygame.Color( 127, 127, 127)
LIGHTGRAY = pygame.Color( 200, 191, 231)
MEDYO_BLUE= pygame.Color(  76,  81,  95)

screen_width = 800
x_pos = screen_width/3
y_pos = 389/2

class minggame:

	def __init__(self, screen, clock, host, lvlnum):
		#frontend things
		self.__screen = screen
		self.__clock = clock
		self.__font = pygame.font.Font(None, 35)

		#backend things
		self.__host = host
		self.__host.reset_queue()

		#initialize resources
		self.__prepare_resources()
		self.__lvlnum = lvlnum
		self.__level = self.__levels[self.__lvlnum]
		self.__current = self.__level.start
		self.__animations[self.__level.cat].play()

		#ming panel
		self.__mypanel = None

		#thread stopper
		self.__done = False
		#game status
		self.__game_over = -1

		#variables for street scrolling
		self.__x1 = 0
		self.__x2 = 800

		#variables for cat scrolling
		self.__catchunk = 800//(self.__level.win-self.__level.lose+3)
		self.__catchunk = self.__catchunk+1 if self.__catchunk%2 == 1 else self.__catchunk
		self.__catx = self.__catchunk*(self.__current - self.__level.lose) - 30
		self.__caty = 50 if self.__level.cat == 'walk' else 30
		self.__catbuffer = 0

		#command to do
		self.__cmd_todo = None
		self.__cmd_word = ''
		self.__cmd_todolist = {}

	def __prepare_resources(self):
		self.__levels = {
			1: level(10, -5, 8, 'walk'),
			2: level(10, -4, 9, 'float'),
			3: level(10, -3, 10, 'walk'),
			4: level(9, -5, 8, 'float'),
			5: level(9, -4, 9, 'walk'),
			6: level(9, -3, 10, 'float'),
			7: level(8, -5, 8, 'walk'),
			8: level(8, -4, 9, 'float'),
			9: level(8, -3, 10, 'walk'),
			10: level(7, -5, 8, 'float'),
			11: level(7, -4, 9, 'walk'),
			12: level(7, -3, 10, 'float'),
			13: level(6, -5, 8, 'walk'),
			14: level(6, -4, 9, 'float'),
			15: level(6, -3, 10, 'walk')
		}

		self.__images = {
			'background':	{	'ming':		pygame.image.load("resources/game/game_background_ming.png"),
								'panel':	pygame.image.load("resources/game/game_background_panel.png")	},
		}

		self.__animations = {
			'walk':	pyganim.PygAnimation(
					[('resources/game/mingming_walk/mingwalk0.png', 0.07), ('resources/game/mingming_walk/mingwalk1.png', 0.07),
					('resources/game/mingming_walk/mingwalk2.png', 0.07), ('resources/game/mingming_walk/mingwalk3.png', 0.07),
					('resources/game/mingming_walk/mingwalk4.png', 0.07), ('resources/game/mingming_walk/mingwalk5.png', 0.07),
					('resources/game/mingming_walk/mingwalk6.png', 0.07), ('resources/game/mingming_walk/mingwalk7.png', 0.07),
					('resources/game/mingming_walk/mingwalk8.png', 0.07), ('resources/game/mingming_walk/mingwalk9.png', 0.07),
					('resources/game/mingming_walk/mingwalk10.png', 0.07), ('resources/game/mingming_walk/mingwalk11.png', 0.07)]),

			'float': pyganim.PygAnimation(
					[('resources/game/mingming_float/mingfloat0.png', 0.1), ('resources/game/mingming_float/mingfloat1.png', 0.1),
					('resources/game/mingming_float/mingfloat2.png', 0.1), ('resources/game/mingming_float/mingfloat3.png', 0.1),
					('resources/game/mingming_float/mingfloat4.png', 0.1), ('resources/game/mingming_float/mingfloat5.png', 0.1),
					('resources/game/mingming_float/mingfloat6.png', 0.1), ('resources/game/mingming_float/mingfloat7.png', 0.1),
					('resources/game/mingming_float/mingfloat8.png', 0.1), ('resources/game/mingming_float/mingfloat9.png', 0.1),
					('resources/game/mingming_float/mingfloat10.png', 0.1), ('resources/game/mingming_float/mingfloat11.png', 0.1),
					('resources/game/mingming_float/mingfloat12.png', 0.1), ('resources/game/mingming_float/mingfloat13.png', 0.1),
					('resources/game/mingming_float/mingfloat14.png', 0.1),	('resources/game/mingming_float/mingfloat15.png', 0.1),
					('resources/game/mingming_float/mingfloat16.png', 0.1), ('resources/game/mingming_float/mingfloat17.png', 0.1),
					('resources/game/mingming_float/mingfloat18.png', 0.1), ('resources/game/mingming_float/mingfloat19.png', 0.1),
					('resources/game/mingming_float/mingfloat20.png', 0.1),	('resources/game/mingming_float/mingfloat21.png', 0.1),
					('resources/game/mingming_float/mingfloat22.png', 0.1), ('resources/game/mingming_float/mingfloat23.png', 0.1),
					('resources/game/mingming_float/mingfloat24.png', 0.1), ('resources/game/mingming_float/mingfloat25.png', 0.1),
					('resources/game/mingming_float/mingfloat26.png', 0.1), ('resources/game/mingming_float/mingfloat27.png', 0.1),
					('resources/game/mingming_float/mingfloat28.png', 0.1), ('resources/game/mingming_float/mingfloat29.png', 0.1),
					('resources/game/mingming_float/mingfloat30.png', 0.1), ('resources/game/mingming_float/mingfloat31.png', 0.1),
					('resources/game/mingming_float/mingfloat32.png', 0.1)])
		}

		self.__panel_coor = (
			((0, 211), (x_pos, 211+y_pos)), ((x_pos, 211), (2*x_pos, 211+y_pos)), ((2*x_pos, 211), (800, 211+y_pos)),
			((0, 211+y_pos), (x_pos, 211+(2*y_pos))), ((x_pos, 211+y_pos), (2*x_pos, 211+(2*y_pos))), ((2*x_pos, 211+y_pos), (800, 600))
		)

	def __draw_things(self):
		self.__screen.fill(MEDYO_BLUE)

		#draw upper panel
		self.__screen.blit(self.__images['background']['ming'], (self.__x1,-30))
		self.__screen.blit(self.__images['background']['ming'], (self.__x2,-30))
		self.__x1-=0.6
		self.__x2-=0.6
		self.__x1 = 800 if self.__x1 <= -800 else self.__x1
		self.__x2 = 800 if self.__x2 <= -800 else self.__x2

		#draw cat 
		if self.__catbuffer != 0:
			self.__catx = self.__catx+2 if self.__catbuffer > 0 else self.__catx-2
			self.__catbuffer = self.__catbuffer-2 if self.__catbuffer > 0 else self.__catbuffer+2
		caty = 50
		self.__animations[self.__level.cat].blit(self.__screen, (self.__catx, self.__caty))

		#draw lower panel
		self.__screen.blit(self.__images['background']['panel'], (0,211))

		#draw panel
		if self.__mypanel != None:
			for i, switch in enumerate(self.__mypanel):
				switch.draw_switch(self.__screen, self.__font, self.__panel_coor[i])

		pygame.draw.line(self.__screen, LIGHTGRAY, [x_pos, 212], [x_pos, 211+y_pos], 1)
		pygame.draw.line(self.__screen, LIGHTGRAY, [2*x_pos, 212], [2*x_pos, 211+y_pos], 1)
		pygame.draw.line(self.__screen, LIGHTGRAY, [0, 212+y_pos], [screen_width, 212+y_pos], 1)
		pygame.draw.line(self.__screen, LIGHTGRAY, [x_pos, 213+y_pos], [x_pos, 211+2*y_pos], 1)
		pygame.draw.line(self.__screen, LIGHTGRAY, [2*x_pos, 213+y_pos], [2*x_pos, 211+2*y_pos], 1)
		pygame.draw.line(self.__screen, LIGHTGRAY, [0, 212], [0, 212+2*y_pos], 1)
		pygame.draw.line(self.__screen, LIGHTGRAY, [0, 210+2*y_pos], [screen_width, 210+2*y_pos], 1)
		pygame.draw.line(self.__screen, LIGHTGRAY, [799, 212], [799, 212+2*y_pos], 1)

		pygame.draw.line(self.__screen, GREEN, [0, 196], [self.__timer_len, 196], 30)
		self.__screen.blit(self.__font.render("STAGE "+str(self.__lvlnum), True, WHITE), (200,200))
		self.__screen.blit(self.__font.render("CURRENT "+str(self.__current), True, WHITE), (250,250))
		self.__screen.blit(self.__font.render("CMD "+str(self.__cmd_word), True, WHITE), (350, 350))

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
				self.__host.send_game_command('TIMEOUT')
				self.__reset_timer()

			self.__clock.tick(self.__frame_rate)

	#process commands sent by players. SERVER ONLY
	def __process_commands(self):
		while not self.__done:
			cmd, pid = self.__host.for_game_front.get()

			#okay command
			if cmd.startswith('COMMAND:'):
				print cmd
				for cid in self.__cmd_todolist:
					print 'match '+self.__cmd_todolist[cid]
					if self.__cmd_todolist[cid] == cmd[8:]:
						print 'found '+str(cid)
						self.__current+=1
						self.__catbuffer+=self.__catchunk
						#win game
						if self.__current == self.__level.win:
							self.__game_over = self.__lvlnum+1 if self.__lvlnum < len(self.__levels) else self.__lvlnum
							self.__host.send_game_update('NEXT_GAME '+str(self.__host.id))
							self.__done = True
						else:
							#generate next command for player
							self.__send_next_command(cid)

			#timeout happened
			elif cmd == 'TIMEOUT':
				self.__current-=1
				self.__catbuffer-=self.__catchunk
				#game over
				if self.__current == self.__level.lose:
					self.__game_over = 0
					self.__host.send_game_update('GAME_OVER '+str(self.__host.id))
					self.__done = True
				else:
					self.__send_next_command(pid)

	#process updates received by client. CLIENT ONLY
	def __process_updates(self):
		while not self.__done:
			update, pid = self.__host.for_game_front.get()
			
			#update with current status
			if update.startswith('CURRENT:'):
				before = self.__current
				self.__current = int(update[8:])
				self.__catbuffer+=self.__catchunk*(self.__current-before)

				#advance to new command
				cid, cmd_num, state_num = string.split(pid, ':')
				# if cmd_num+':'+state_num == self.__cmd_todo:
				if int(cid) == self.__host.id:
					self.__cmd_todo = cmd_num+':'+state_num
					self.__cmd_word = mingpanel.get_cmdword(self.__cmd_todo)
					self.__reset_timer()

			#win game
			elif update == 'NEXT_GAME':
				self.__game_over = self.__lvlnum+1
				self.__done = True

			#lose game
			elif update == 'GAME_OVER':
				self.__game_over = 0
				self.__done = True

			#receive panels
			elif update == 'PANELS':
				self.__mypanel = mingpanel.get_switches([int(i) for i in string.split(pid, ',')])	#get own panel

	# SERVER ONLY
	def __send_next_command(self, cid):
		#ask for a command from mingpanel from list of panels of player
		cmd_num, state_num = mingpanel.get_command(self.__panel_list, cid)
		cmd_str = str(cmd_num)+':'+str(state_num)

		#if server owns the command
		if self.__host.id == cid:
			self.__cmd_todo = cmd_str
			self.__cmd_word = mingpanel.get_cmdword(self.__cmd_todo)
			self.__reset_timer()

		self.__cmd_todolist[cid] = cmd_str		
		self.__host.send_game_update('CURRENT:'+str(self.__current)+' '+str(cid)+':'+cmd_str)

	def start_game_server(self):
		threading.Thread(target = self.__start_timer).start()
		threading.Thread(target = self.__process_commands).start()
		self.__panel_list = self.__host.send_panels(mingpanel.generate_panels()) 	#distribute panels to players
		self.__mypanel = mingpanel.get_switches(self.__panel_list[self.__host.id])	#get own panel

		#send server commands
		cmd_num, state_num = mingpanel.get_command(self.__panel_list, self.__host.id)
		self.__cmd_todo = str(cmd_num)+':'+str(state_num)
		self.__cmd_word = mingpanel.get_cmdword(self.__cmd_todo)
		self.__cmd_todolist[self.__host.id] = self.__cmd_todo

		#send command to players
		for cid in self.__panel_list:
			if cid != self.__host.id:
				self.__send_next_command(cid)

		while not self.__done:
			event = pygame.event.poll()
			self.__draw_things()
			if event.type == QUIT:
				self.__host.stop_game('KILL')
				self.__done = True

			elif event.type == MOUSEBUTTONDOWN:
				for b in self.__mypanel:
					a = b.process_event(pygame.mouse.get_pos())
					if a != None:
						self.__host.send_game_command(a)
						break
				
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

			#game proper
			else:
				self.__draw_things()
				if event.type == QUIT:
					self.__host.exit_room('LEAVE')
					self.__done = True

				elif event.type == MOUSEBUTTONDOWN:
					for b in self.__mypanel:
						a = b.process_event(pygame.mouse.get_pos())
						if a != None:
							self.__host.send_game_command(a)
							break

			pygame.display.update()
		return self.__game_over