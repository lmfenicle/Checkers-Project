#imports
import pygame


#inizitlize pygame
pygame.init()
pygame.font.init()


#screenfunctions

#draw the welcome screen
def welcomeScreen():
    screen.fill(BLUE)
    font = pygame.font.SysFont('Arial', 90)
    textToDispaly = "Welcome to Checkers!"
    textColor = BLACK
    textSurface = font.render(textToDispaly, True, textColor)

    # Position the text
    textRect = textSurface.get_rect()
    textRect.center = (800 // 2, 200)

    # Blit the text to the screen
    screen.blit(textSurface, textRect)

    font = pygame.font.SysFont('Arial', 50)
    textToDispaly = "Press Enter to continue"
    textSurface = font.render(textToDispaly, True, textColor)
    textRect = textSurface.get_rect()
    textRect.center = (800 // 2, 600)
    screen.blit(textSurface, textRect)


#draw the board
def board():
    screen.fill(GREEN)
    #create board
    for i in range(0,4):
        for j in range(0,8):
            if (j % 2 == 0):
                pygame.draw.rect(screen, WHITE, (100 + 150*i, 100 + 75 * j, 75, 75), 0)
                pygame.draw.rect(screen, BLACK, (175 + 150 * i, 100 + 75 * j, 75, 75), 0)
            else:
                pygame.draw.rect(screen, BLACK, (100 + 150 * i, 100 + 75 * j, 75, 75), 0)
                pygame.draw.rect(screen, WHITE, (175 + 150 * i, 100 + 75 * j, 75, 75), 0)

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

screenState = "Welcome"

#running bool
isRunning = True

#start of running loop
while isRunning:

    #event listener
    for event in pygame.event.get():

        #x out of window
        if event.type == pygame.QUIT:

            #quit game
            isRunning = False

        #switch for screen state
        match screenState:
            case "Welcome":
                welcomeScreen()

            case Board:
                board()

        #chnage the screen and draw the board
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and screenState == "Welcome":
                screenState = "board"
    #update screen
    pygame.display.update()

#end pygame
pygame.quit()


