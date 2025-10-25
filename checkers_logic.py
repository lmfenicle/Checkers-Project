import numpy as np
import pygame
import sys
import time

board = np.full((8,8),None, dtype = object)

# colors
RED = (255, 0, 0); ORANGE = (255, 128, 0); YELLOW = (255, 255, 0); GREEN = (0, 255, 0); BLUE = (0, 0, 255); PURPLE = (255, 0, 255); WHITE = (255, 255, 255); BLACK = (0, 0, 0)
BACKGROUND_COLOR = (60, 95, 74)

class Piece:
    def __init__(self, location, value):
        self.location = location
        self.value = value
        if value == -1:
            self.color = BLACK
        elif value == 1:
            self.color = RED
        self.is_king = False

        self.rects = pygame.Rect(self.location[1] * 50 + 50, self.location[0] * 50 + 50, 50, 50)

    def __str__(self):
        return str(self.value)

    #__repr__ = __str__


# fill the board with pieces in the right place
# 1 for light and -1 for dark

def instantiate_board():
    for row in range(8):
        for col in range(8):
            if row == 0 or row == 2:
                if col % 2 == 0:
                    board[row][col] = Piece((row,col),1)
            elif row == 1:
                if col % 2 == 1:
                    board[row][col] = Piece((row,col),1)

            elif row == 5 or row == 7:
                if col % 2 == 1:
                    board[row][col] = Piece((row,col), -1)
            elif row == 6:
                if col % 2 == 0:
                    board[row][col] = Piece((row,col), -1)

def get_possible_moves(location):
    row = location[0]
    col = location[1]
    piece = board[row][col]
    possible_moves = []

    # white (1) pieces can only move down i.e. col + 1
    if piece == 1:
        if row != 7: # prevents OOB error
            #check for down - left
            if col != 0:
                if board[row + 1][col - 1] == 0:
                    possible_moves.append((row + 1, col - 1)) # append the destination to the list of possible moves
                elif board[row + 1][col - 1] == -1: # if down left is taken by a dark piece
                    # check for possible take
                    if col != 1: # prevent OOB
                        if board[row + 2][col - 2] == 0: # open space beyond the dark piece
                            possible_moves.append((row + 2, col - 2))
            # check down Right
            if col != 7: # prevent OOB error
                if board[row + 1][col + 1] == 0:
                    possible_moves.append((row + 1, col + 1))
                #check for possible take
                elif board[row + 1][col + 1] == -1:
                    if col != 6:
                        if board[row + 2][col + 2] == 0:
                            possible_moves.append((row + 2, col + 2))
    # dark pieces move up
    if piece == -1:
        if row != 0: # prevent OOB error
            # ckeck for up left
            if col != 0:
                if board[row - 1][col - 1] == 0:
                    possible_moves.append((row - 1, col - 1))
                #check for takes
                if board[row - 1][col - 1] == -1:
                    if col != 1:
                        if board[row - 2][col - 2] == 0:
                            possible_moves.append((row - 2, col - 2))
            # check for up right
            if col != 7: #prevent OOB error
                if board[row - 1][col + 1] == 0:
                    possible_moves.append((row - 1, col + 1))
                #check for takes
                elif board[row - 1][col + 1] == -1:
                    if col != 6:
                        if board[row - 2][col + 2] == 0:
                            possible_moves.append((row - 2, col + 2))
    return possible_moves

# TODO possible king moves - 3 for white king - 4 for dark king

def move(location, destination):
    # warning! this method assumes all inputs are valid and in bounds
    # only moves pieces and removes takes
    diff_row = (destination[0] - location[0])
    diff_col = (destination[1] - location[1])

    print(diff_row, diff_col)

    #if the move is a take
    if diff_row % 2 == 0:
        remove_row = location[0] + (diff_row // 2)
        remove_col = location[1] + (diff_col // 2)
        print(remove_row, remove_col)
        board[remove_row][remove_col] = 0
    board[destination] = board[location]
    board[location] = 0

def draw_board():
    screen.fill(BACKGROUND_COLOR)
    #create board
    for i in range(0,4):
        for j in range(0,8):
            if (j % 2 == 0):
                pygame.draw.rect(screen, WHITE, (50 + 100 * i, 50 + 50 * j, 50, 50), 0)
                pygame.draw.rect(screen, BLACK, (100 + 100 * i, 50 + 50 * j, 50, 50), 0)
            else:
                pygame.draw.rect(screen, BLACK, (50 + 100 * i, 50 + 50 * j, 50, 50), 0)
                pygame.draw.rect(screen, WHITE, (100 + 100 * i, 50 + 50 * j, 50, 50), 0)
instantiate_board()

### Display piece location based on the board object
pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def display_board_state(board):
    for element in board.flat:
        if element is not None:
            pygame.draw.circle(screen, element.color , element.rects.center, 15)

#print(board)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    draw_board()

    display_board_state(board)

    pygame.display.update()