import PanelGeneration
import pygame

class Minggame:
    def __init__(self, server, num_clients, stage_num, screen):
        self.server = server
        self.num_clients = num_clients
        self.stage_num = stage_num
        self.screen = screen
    def dispose(self):
        Minggame(self.server, self.num_clients,self.stage_num,self.screen)
    def getlistOfPanels(self):
        panel = PanelGeneration.randomizePanels();
        PanelGeneration.randomizeCommands(panel)
        for i in xrange(0,6):
            PanelGeneration.getListOfSubcommands(panel[i].getSelectedCommand())
    def drawGame(self):
        # Set up for the timer
        timer_width = 16 #width of the timer GUI
        frame_count = 0
        frame_rate = 60
        start_time = 10
        timer = 800
        font = pygame.font.Font(None, 35)
        img = pygame.image.load("chinese.jpg")
        # For the Countdown Timer:
        total_seconds = start_time - (frame_count // frame_rate) #seconds
        pygame.draw.line(screen, GREEN, [0, 171], [timer, 171], 30)
        # TIME'S UP!!!!
        if total_seconds < 0:
            total_seconds = 0
            print "BOOOOM!!!!"

        timer = timer-1.30
        frame_count += 1
    
        # Set the commandline
        output_string = "Command!!!!!!"
     
        # Blit to the screen
        text = font.render(output_string, True, WHITE)

        # Set the panels
        pygame.draw.line(self.screen, LIGHTGRAY, [0, 211], [screen_width, 211], 1)
        pygame.draw.rect(self.screen, GRAY, [0, 212, panel_width, panel_height])
        pygame.draw.line(self.screen, LIGHTGRAY, [panel_width, 212], [panel_width, 211+panel_height], 1)
        pygame.draw.rect(self.screen, GRAY, [panel_width+1, 212, panel_width, panel_height])
        pygame.draw.line(self.screen, LIGHTGRAY, [2*panel_width, 212], [2*panel_width, 211+panel_height], 1)
        pygame.draw.rect(self.screen, GRAY, [2*(panel_width)+1, 212, panel_width, panel_height])
        pygame.draw.line(self.screen, LIGHTGRAY, [0, 212+panel_height], [screen_width, 212+panel_height], 1)
        pygame.draw.rect(self.screen, GRAY, [0, 213+panel_height, panel_width, panel_height])
        pygame.draw.line(self.screen, LIGHTGRAY, [panel_width, 213+panel_height], [panel_width, 211+2*panel_height], 1)
        pygame.draw.rect(self.screen, GRAY, [panel_width+1, 213+panel_height, panel_width, panel_height])
        pygame.draw.line(self.screen, LIGHTGRAY, [2*panel_width, 213+panel_height], [2*panel_width, 211+2*panel_height], 1)
        pygame.draw.rect(self.screen, GRAY, [2*(panel_width)+1, 213+panel_height, panel_width, panel_height])
        pygame.draw.line(self.screen, LIGHTGRAY, [0, 212], [0, 212+2*panel_height], 1)
        pygame.draw.line(self.screen, LIGHTGRAY, [0, 210+2*panel_height], [screen_width, 210+2*panel_height], 1)
        pygame.draw.line(self.screen, LIGHTGRAY, [799, 212], [799, 212+2*panel_height], 1)
        pygame.draw.rect(self.screen, RED, [0, 187, screen_width, 24])
    
 
        # --- Go ahead and update the screen with what we've drawn.
        self.screen.blit(img, (0,0))
        self.screen.blit(text, [0, 188])
        pygame.display.update()
        pygame.display.flip()

game = Minggame(1324,32423,32,424)
game.getlistOfPanels()
