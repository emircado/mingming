import random

class Panels:
    """ Panel class contains the information regarding the ff. : list of commands, image, panel_width, panel_height,panel_number """
    def __init__(self):
        self.panel_number         = 0
        self.commands             = []
        self.selected_command     = ''
        self.panel_width          = 800/3
        self.panel_height         = 389/2
    
    def setPanelNumber(self, number):
        self.panel_number = number
    def getPanelNumber(self):
    	return self.panel_number;

    def setCommands(self,com):
        self.commands=com
    def getCommands(self):
        return self.commands

    def setSelectedCommand(self, selected):
    	self.selected_command = selected
    def getSelectedCommand(self):
    	return self.selected_command

class Commands:
    """ Command class contains the information regarding the ff. : command_name and list of subcommands, command message to be displayed """
    def __init__(self,commandname):
		self.commandname = commandname
		self.subcommands = []
		self.image = ''
		self.message = ''

    def getCommandname(self):
	    return self.commandname 

    def setSubcommands(self,subcommands):
	    self.subcommands = subcommands
    def getSubcommands(self):
	    return self.subcommands

    def setMessage(self, msg):
	    self.message = msg
    def getMessage(self):
        return self.message

    def setImage(self,image):
    	self.image = image
    def getImage(self):
    	return self.image

class Subcommands:
    """ Subcommand class contains the information regarding the ff. : subcommand_name, coordinates, mingming_reaction """
    def __init__(self,subcommandname):
		self.subcommandname = subcommandname
		self.xcoordinate = 0
		self.ycoordinate = 0
		self.image = ''
		self.reaction = ''

    def getSubcommandname(self):
	    return self.subcommandname 

    def setxcoordinate(self,xcoordinate):
	    self.xcoordinate = xcoordinate
    def getxcoordinate(self):
	    return self.xcoordinate

    def setycoordinate(self,xcoordinate):
	    self.ycoordinate = ycoordinate
    def getycoordinate(self):
	    return self.ycoordinate

    def setReaction(self, reaction):
	    self.reaction = reaction
    def getReaction(self):
        return self.reaction

    def setImage(self,image):
    	self.image = image
    def getImage(self):
    	return self.image

#Possible panel values
def CommandsList():
    panel_commands    = [[],[],[],[],[],[]]
    panel_commands[0] = ['prepare', 'train','rock','huckaback']
    panel_commands[1] = ['groom','pay','teleport','panjandrum']
    panel_commands[2] = ['play', 'earthquake','challenge', 'rats']
    panel_commands[3] = ['poke', 'compliment','masticate','bell']
    panel_commands[4] = ['purr','message','canoodle', 'vet']
    panel_commands[5] = ['tickle', 'meditate','molly', 'visit']
    return panel_commands

def randomizePanels():
    panel_list = []
    panel_commands = CommandsList()
    for i in xrange(0,6):
        panel = Panels()
        panel.setPanelNumber(i)
        selectedPanel = random.choice(list(panel_commands))
        panel.setCommands(selectedPanel)
        panel_list.append(panel)
        panel_commands.remove(selectedPanel)
    return panel_list

def randomizeCommands(panel_list):
    for i in xrange(0,6):
        chosen_command = Commands(random.choice(list(panel_list[i].getCommands())))
        panel_list[i].setSelectedCommand(chosen_command)
    return panel_list

def callCommand(listOfSelectedCommands):
	for i in xrange(0,6):
		command = random.choice(list(listOfSelectedCommands))
	for i in xrange(0,len(command.getSubcommands())):
		subcommand = random.choice(list(command.getSubcommands()))
	return (command,subcommand)

def getListOfSubcommands(command):
    commandname = command.getCommandname()
    if(commandname == 'prepare'):
        #choices = ['fish' , 'milk']
        choice1 = Subcommands('fish')
        choice2 = Subcommands('milk')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'train'):
        #choices = ['1','2','3','4']
        choice1 = Subcommands('1')
        choice2 = Subcommands('2')
        choice3 = Subcommands('3')
        choice4 = Subcommands('4')
        choices = [choice1,choice2,choice3,choice4]
        command.setSubcommands(choices)
    elif(commandname == 'panjandrum'):
        #choices = ['0','1','2','3','4']
        choice0 = Subcommands('0')
        choice1 = Subcommands('1')
        choice2 = Subcommands('2')
        choice3 = Subcommands('3')
        choice4 = Subcommands('4')
        choices = [choice0,choice1,choice2,choice3,choice4]
        command.setSubcommands(choices)
    elif(commandname == 'rock'):
        #choices = ['activate','deactivate']
        command.setImage('switch-1.png')
        choice1 = Subcommands('activate')
        choice1.setImage('swithc-2.png')
        choice2 = Subcommands('deactivate')
        choice1.setImage('switch-1.png')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'poke'):
        #choices = ['activate','deactivate']
        command.setImage('buttons_unclicked.png')
        choice1 = Subcommands('activate')
        choice1.setImage('buttons_clicked.png')
        choice2 = Subcommands('deactivate')
        choice1.setImage('buttons_unclicked.png')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname =='purr'):
        #choices = ['activate','deactivate']
        command.setImage('buttons_unclicked.png')
        choice1 = Subcommands('activate')
        choice1.setImage('buttons_clicked.png')
        choice2 = Subcommands('deactivate')
        choice1.setImage('buttons_unclicked.png')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'meditate'):
        #choices = ['activate','deactivate']
        command.setImage('switch-1.png')
        choice1 = Subcommands('activate')
        choice1.setImage('swithc-2.png')
        choice2 = Subcommands('deactivate')
        choice1.setImage('switch-1.png')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname =='bell'):
        #choices = ['activate','deactivate']
        command.setImage('buttons_unclicked.png')
        choice1 = Subcommands('activate')
        choice1.setImage('buttons_clicked.png')
        choice2 = Subcommands('deactivate')
        choice1.setImage('buttons_unclicked.png')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'huckaback'):
        #choices = ['clean','throw','burn']
        choice1 = Subcommands('clean')
        choice2 = Subcommands('throw')
        choice3 = Subcommands('burn')
        choices = [choice1,choice2,choice3]
        command.setSubcommands(choices)
    elif(commandname == 'groom'):
        #choices = ['1','2','3']
        choice1 = Subcommands('1')
        choice2 = Subcommands('2')
        choice3 = Subcommands('3')
        choices = [choice1,choice2,choice3]
        command.setSubcommands(choices)
    elif(commandname == 'pay'):
        #choices = ['yaman me','kuripot me']
        choice1 = Subcommands('yaman me')
        choice2 = Subcommands('kuripot me')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'teleport'):
        #choices = ['try', 'lol no']
        choice1 = Subcommands('try')
        choice2 = Subcommands('lol no')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'play'):
        #choices = ['red', 'blue', 'green']
        choice1 = Subcommands('red')
        choice2 = Subcommands('blue')
        choice3 = Subcommands('green')
        choices = [choice1,choice2,choice3]
        command.setSubcommands(choices)
    elif(commandname == 'earthquake'):
        #choices = ['left','right']
        choice1 = Subcommands('left')
        choice2 = Subcommands('right')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'challenge'):
        #choices = ['1','2','3','4','5']
        choice1 = Subcommands('1')
        choice2 = Subcommands('2')
        choice3 = Subcommands('3')
        choice4 = Subcommands('4')
        choice5 = Subcommands('5')
        choices = [choice1,choice2,choice3,choice4,choice5]
        command.setSubcommands(choices)
    elif(commandname == 'rats'):
        #choices = ['kill']
        choice1 = Subcommands('kill')
        choices = [choice1]
        command.setSubcommands(choices)
    elif(commandname == 'compliment'):
        #choices = ['bola', 'sincere']
        choice1 = Subcommands('bola')
        choice2 = Subcommands('sincere')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'masticate'):
        #choices = ['food', 'toy']
        choice1 = Subcommands('food')
        choice2 = Subcommands('toy')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname =='message'):
        #choices = ['swedish','shiatsu']
        choice1 = Subcommands('swedish')
        choice2 = Subcommands('shiatsu')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'canoodle'):
        #choices = ['caress','fondle','pet']
        choice1 = Subcommands('caress')
        choice2 = Subcommands('fondle')
        choice3 = Subcommands('pet')
        choices = [choice1,choice2,choice3]
        command.setSubcommands(choices)
    elif(commandname == 'vet'):
        #choices = ['checkup', 'confine']
        choice1 = Subcommands('checkup')
        choice2 = Subcommands('confine')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    elif(commandname == 'tickle'):
        #choices = ['click']
        choice1 = Subcommands('click')
        choices = [choice1]
        command.setSubcommands(choices)
    elif(commandname == 'molly'):
        #choices = ['0','1','2','3','4','5']
        choice0 = Subcommands('0')
        choice1 = Subcommands('1')
        choice2 = Subcommands('2')
        choice3 = Subcommands('3')
        choice4 = Subcommands('4')
        choice5 = Subcommands('5')
        choices = [choice0,choice1,choice2,choice3,choice4,choice5]
        command.setSubcommands(choices)
    elif(commandname == 'visit'):
        #choices = ['friend1', 'friend2']
        choice1 = Subcommands('friend1')
        choice2 = Subcommands('friend2')
        choices = [choice1,choice2]
        command.setSubcommands(choices)
    return command
