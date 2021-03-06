import random
import pygame
import string
from pygame.locals import *

BLACK     = pygame.Color(   0,   0,   0)
WHITE     = pygame.Color( 255, 255, 255)
GREEN     = pygame.Color(   0, 255,   0)
RED       = pygame.Color( 255,   0,   0)
GRAY      = pygame.Color( 127, 127, 127)
LIGHTGRAY = pygame.Color( 200, 191, 231)

BUTTON = 0
TOGGLE = 1
BTN_5 = 2
BTN_3 = 3
BTN_2 = 4
TGL_GRP = 5

_images = {
	BUTTON:	{	'dim0':	(50, 50),
				0: 	pygame.image.load('resources/game/buttons/button_clicked.png')	},

	TOGGLE:	{	'dim1': (50, 50),
				'dim0':	(50, 50),
				0:	pygame.image.load('resources/game/buttons/switch-1.png'),
				1:	pygame.image.load('resources/game/buttons/switch-2.png')	},

	BTN_5:	{	'dim4': (155, 100),
				'dim3': (72, 100),
				'dim2': (195, 35),
				'dim1':	(113, 35),
				'dim0': (30, 35),
				0:	pygame.image.load('resources/game/buttons/b1n.png'),
				1:	pygame.image.load('resources/game/buttons/b2n.png'),
				2:	pygame.image.load('resources/game/buttons/b3n.png'),
				3:	pygame.image.load('resources/game/buttons/b4n.png'),
				4:	pygame.image.load('resources/game/buttons/b5n.png'),
				5:	pygame.image.load('resources/game/buttons/b1y.png'),
				6:	pygame.image.load('resources/game/buttons/b2y.png'),
				7:	pygame.image.load('resources/game/buttons/b3y.png'),
				8:	pygame.image.load('resources/game/buttons/b4y.png'),
				9:	pygame.image.load('resources/game/buttons/b5y.png')		},

	BTN_3:	{	'dim2': (195, 35),
				'dim1':	(113, 35),
				'dim0': (30, 35),
				0:	pygame.image.load('resources/game/buttons/b1n.png'),
				1:	pygame.image.load('resources/game/buttons/b2n.png'),
				2:	pygame.image.load('resources/game/buttons/b3n.png'),
				3:	pygame.image.load('resources/game/buttons/b1y.png'),
				4:	pygame.image.load('resources/game/buttons/b2y.png'),
				5:	pygame.image.load('resources/game/buttons/b3y.png')		},

	BTN_2: {	'dim1': (40, 100),
				'dim0': (40, 35),
				0:	pygame.image.load('resources/game/buttons/btn2.png')	}
}

class mingswitch:
	def __init__(self, sid, name, stype, cmd, extras = None):
		self.sid = sid
		self.name = name
		self.stype = stype
		self.commands = cmd
		self.state = 0
		self.extras = extras
		self.__active_buttons = []

	def draw_switch(self, screen, font, coor):
		(x1, y1), (x2, y2) = coor
		self.__active_buttons = []

		screen.blit(font.render(str(self.name), True, BLACK), (x1, y2-32))

		if self.stype == BUTTON or self.stype == TOGGLE:
			off_x, off_y = _images[self.stype]['dim'+str(self.state)]
			self.__active_buttons.append(screen.blit(_images[self.stype][self.state], (x1+off_x, y1+off_y)))

		elif self.stype == BTN_5:
			for i in range(5):
				off_x, off_y = _images[self.stype]['dim'+str(i)]
				if i == self.state:
					self.__active_buttons.append(screen.blit(_images[self.stype][i+5], (x1+off_x, y1+off_y)))
				else:
					self.__active_buttons.append(screen.blit(_images[self.stype][i], (x1+off_x, y1+off_y)))

		elif self.stype == BTN_3:
			for i in range(3):
				off_x, off_y = _images[self.stype]['dim'+str(i)]
				if i == self.state:
					self.__active_buttons.append(screen.blit(_images[self.stype][i+3], (x1+off_x, y1+off_y)))
				else:
					self.__active_buttons.append(screen.blit(_images[self.stype][i], (x1+off_x, y1+off_y)))

		elif self.stype == BTN_2:
			off_x0, off_y0 = _images[self.stype]['dim0']
			self.__active_buttons.append(screen.blit(_images[self.stype][0], (x1+off_x0, y1+off_y0)))
			screen.blit(font.render(_switches[self.sid].extras[0], True, WHITE), (x1+off_x0+10, y1+off_y0+10))

			off_x1, off_y1 = _images[self.stype]['dim1']
			self.__active_buttons.append(screen.blit(_images[self.stype][0], (x1+off_x1, y1+off_y1)))
			screen.blit(font.render(_switches[self.sid].extras[1], True, WHITE), (x1+off_x1+10, y1+off_y1+10))

	def process_event(self, mouse_evt):
		cmd = None
		for i, b in enumerate(self.__active_buttons):
			if b.collidepoint(mouse_evt):
				cmd = 'COMMAND:'+str(self.sid)+':'+str(self.state)

				if self.stype == TOGGLE:
					cmd = 'COMMAND:'+str(self.sid)+':'+str(self.state)
					if self.state == 0:
						self.state = 1
					elif self.state == 1:
						self.state = 0

				elif self.stype == BTN_5 or self.stype == BTN_3 or self.stype == BTN_2:
					self.state = i
					cmd = 'COMMAND:'+str(self.sid)+':'+str(self.state)
		return cmd

_switches = [
	mingswitch(0, 'Poke', BTN_2, ('Poke Mingming!!!', 'Unpoke Mingming!!!'), ('Poke', 'Unpoke')),
	mingswitch(1, 'Food', BTN_2, ('Feed fish', 'Feed milk'), ('Fish', 'Milk')),
	mingswitch(2, 'Yarn', BTN_3, ('Play with yarn 1', 'Play with yarn 2', 'Play with yarn 3')),
	mingswitch(3, 'Bills', BUTTON , ('Pay Bills',)),			#FINAL
	mingswitch(4, 'Cat Trainer', BTN_5, ('Cat Trainer to 1', 'Cat Tranier to 2', 'Cat Tranier to 3', 'Cat Tranier to 4', 'Cat Tranier to 5')),	#FINAL
	mingswitch(5, 'Compliment', BUTTON, ('Give Compliment',)),	#FINAL
	mingswitch(6, 'Massage', BUTTON, ('Massage Me',)),	#FINAL
	mingswitch(7, 'Meditate', BUTTON, ('Meditate Now',)),	#FINAL
	mingswitch(8, 'Grooming', BTN_3, ('Grooming to Level 1', 'Grooming to Level 2', 'Grooming to Level 3')),
	mingswitch(9, 'Teleport', BUTTON, ('Teleport here',)),
	mingswitch(10, 'Challenger', BUTTON, ('Challenge me',)),
	mingswitch(11, 'Masticate', BUTTON, ('Masticate you',)),
	mingswitch(12, 'Canoodle', BUTTON, ('Canoodle wee',)),
	mingswitch(13, 'Mollycoddle', BUTTON, ('Mollycoddle wee',)),
	mingswitch(14, 'Huckaback', BUTTON, ('Huckaback cloth',)),
	mingswitch(15, 'Panjandrum', BUTTON, ('Panjandrum drum',)),
	mingswitch(16, 'Rats', BUTTON, ('Kill Rats',)),					#FINAL
	mingswitch(17, 'Bell', BUTTON, ('Ring bell',)),					#FINAL
	mingswitch(18, 'Veterinarian', BUTTON, ('Visit Vet',)),			#FINAL
	mingswitch(19, 'Friends', BUTTON, ('Say hi to friends',)),
	mingswitch(20, 'Ping Pong', BUTTON, ('Play Ping Pong',)),
	mingswitch(21, 'Moon Cake', BUTTON, ('Eat Moon Cake',)),
	mingswitch(22, 'Litter Box', BUTTON, ('Clean litter box',)),
	mingswitch(23, 'Schrodinger\'s Cat', BTN_2, ('Schrodinger\'s cat izz dead', 'Schrodinger\'s cat izz alive'), ('Dead', 'Alive')), 
	mingswitch(24, 'Fur', BUTTON, ('Lick Fur',)),
	mingswitch(25, 'Siopao', BTN_2, ('Eat Asado Siopao', 'Eat Bola-bola Siopao'), ('Asado', 'Bola-bola')),	#FINAL
	mingswitch(26, 'Ching', BTN_2, ('Ching Chung', 'Ching Chang'), ('Chung', 'Chang')),
	mingswitch(27, 'Samting10', BUTTON, ('Press Samting10',)),
	mingswitch(28, 'Samting9', BUTTON, ('Press Samting9',)),
	mingswitch(29, 'Bath', BUTTON, ('Take a bath',)),
	mingswitch(30, 'Eyes', BTN_2, ('Make singkit eyes', 'Widen eyes'), ('Singkit', 'Widen')),
	mingswitch(31, 'Meteor Garden', BTN_2, ('Watch Meteor Garden', 'Fangirl Meteor Garden'), ('Watch', 'Fangirl')),
	mingswitch(32, 'Tour', BTN_2, ('Tour China', 'Tour Hong Kong'), ('China', 'Hong Kong')),
	mingswitch(33, 'World War', BTN_3, ('Start World War I', 'Start World War II', 'Start World War III')),
	mingswitch(34, 'Speak Chinese', BTN_2, ('Ni hao', 'Jia you'), ('Ni hao', 'Jia you')),
	mingswitch(35, 'Territory', BTN_2, ('Scratch on territory', 'Pee on territory'), ('Scratch', 'Pee')),
	mingswitch(36, 'Samting11', TOGGLE, ('Engage Samting11', 'Disengage Samting11')),
	mingswitch(37, 'Samting12', TOGGLE, ('Engage Samting12', 'Disengage Samting12')),
	mingswitch(38, 'Samting13', TOGGLE, ('Engage Samting13', 'Disengage Samting13')),
	mingswitch(39, 'Samting14', TOGGLE, ('Engage Samting14', 'Disengage Samting14')),
	mingswitch(40, 'Samting15', TOGGLE, ('Engage Samting15', 'Disengage Samting15')),
	mingswitch(41, 'Samting16', TOGGLE, ('Engage Samting16', 'Disengage Samting16')),
	mingswitch(42, 'Samting17', TOGGLE, ('Engage Samting17', 'Disengage Samting17')),
	mingswitch(43, 'Samting18', TOGGLE, ('Engage Samting18', 'Disengage Samting18')),
	mingswitch(44, 'Samting19', TOGGLE, ('Engage Samting19', 'Disengage Samting19')),
	mingswitch(45, 'Samting20', BTN_5, ('Samting20 to 1', 'Samting20 to 2', 'Samting20 to 3', 'Samting20 to 4', 'Samting20 to 5')),
	mingswitch(46, 'Samting21', BTN_5, ('Samting21 to 1', 'Samting21 to 2', 'Samting21 to 3', 'Samting21 to 4', 'Samting21 to 5')),
	mingswitch(47, 'Samting22', BTN_5, ('Samting22 to 1', 'Samting22 to 2', 'Samting22 to 3', 'Samting22 to 4', 'Samting22 to 5')),
	mingswitch(48, 'Samting23', BTN_5, ('Samting23 to 1', 'Samting23 to 2', 'Samting23 to 3', 'Samting23 to 4', 'Samting23 to 5')),
	mingswitch(49, 'Samting24', BTN_5, ('Samting24 to 1', 'Samting24 to 2', 'Samting24 to 3', 'Samting24 to 4', 'Samting24 to 5'))
]
	
def generate_panels():
	panels = [i for i in range(len(_switches))]
	random.shuffle(panels)
	return [panels[0:6], panels[6:12], panels[12:18], panels[18:24]]

def get_switches(panel):
	return [_switches[i] for i in panel]

def get_command(panel, cid):
	#randomly choose from list
	x = []
	for pid in panel:
		# if pid != cid:
		x+=panel[pid]
	cmd_num = random.choice(x)
	subcom = _switches[cmd_num].commands

	return cmd_num, subcom.index(random.choice(subcom))

def get_cmdword(cmd):
	cmd_num, state_num = string.split(cmd, ':')
	return _switches[int(cmd_num)].commands[int(state_num)]