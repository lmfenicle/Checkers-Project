#imports
import pygame

#inizitlize pygame
pygame.init()

#screen sizes
width = 800
height = 600

#create screen
screen = pygame.display.set_mode((width, height))

isRunning = True

#start of running loop
while isRunning:

    #event listener
    for event in pygame.event.get():

        #x out of window
        if event.type == pygame.QUIT:

            #quit game
            isRunning = False

#end pygame
pygame.quit()