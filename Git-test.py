#imports
import pygame

#inizitlize pygame
pygame.init()

#screen sizes
width = 800
height = 800

#create screen
screen = pygame.display.set_mode((width, height))

#colors
GREEN  = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 255)

backgroundColor = GREEN

#running bool
isRunning = True

#start of running loop
while isRunning:

    #set color
    screen.fill(backgroundColor)

    #create board
    for i in range(0,4):
        for j in range(0,8):
            if (j % 2 == 0):
                pygame.draw.rect(screen, WHITE, (100 + 150*i, 100 + 75 * j, 75, 75), 0)
                pygame.draw.rect(screen, BLACK, (175 + 150 * i, 100 + 75 * j, 75, 75), 0)
            else:
                pygame.draw.rect(screen, BLACK, (100 + 150 * i, 100 + 75 * j, 75, 75), 0)
                pygame.draw.rect(screen, WHITE, (175 + 150 * i, 100 + 75 * j, 75, 75), 0)

    #event listener
    for event in pygame.event.get():

        #x out of window
        if event.type == pygame.QUIT:

            #quit game
            isRunning = False

    #update screen
    pygame.display.update()

#end pygame
pygame.quit()


