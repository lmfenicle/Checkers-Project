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
        self.x = location[0]
        self.y = location[1]
        self.value = value
        if value == -1:
            self.color = BLACK
        elif value == 1:
            self.color = RED
        elif self.value == 99:
            self.color = BLUE

        self.rects = pygame.Rect(self.location[1] * 50 + 50, self.location[0] * 50 + 50, 50, 50)
        self.is_king = False
    def __str__(self):
        return str(self.value)

    __repr__ = __str__

    def update_loc(self, new_loc):
        self.location = new_loc
        self.x = new_loc[0]
        self.y = new_loc[1]
        self.rects = pygame.Rect(self.location[1] * 50 + 50, self.location[0] * 50 + 50, 50, 50)

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

def get_possible_moves(piece):  # TODO refactor for king pieces
    # input piece output: list of location tuples
    row = piece.x
    col = piece.y
    possible_moves = []

    # white (1) pieces can only move down i.e. col + 1
    if piece.value == 1:
        if row != 7:
            if col != 0:  # check down left
                if board[row + 1][col - 1] is None:  # no piece in that loc
                    possible_moves.append((row + 1, col - 1))
                elif board[row + 1][col - 1].value == -1:  # down left is a dark piece
                    if col != 1 and board[row + 2][col - 2] is None:
                        possible_moves.append((row + 2, col - 2))

            if col != 7:  # check down right
                if board[row + 1][col + 1] is None:  # no piece in that loc
                    possible_moves.append((row + 1, col + 1))
                elif board[row + 1][col + 1].value == -1:  # down left is a dark piece
                    if col != 6 and board[row + 2][col + 2] is None:
                        possible_moves.append((row + 2, col + 2))
    # dark pieces move up
    if piece.value == -1:
        if row != 0:
            if col != 0:  # check up left
                if board[row - 1][col - 1] is None:  # no piece in that loc
                    possible_moves.append((row - 1, col - 1))
                elif board[row - 1][col - 1].value == 1:  # up left is a light piece
                    if col != 1 and board[row - 2][col - 2] is None:
                        possible_moves.append((row - 2, col - 2))

            if col != 7:  # check up right
                if board[row - 1][col + 1] is None:  # no piece in that loc
                    possible_moves.append((row - 1, col + 1))
                elif board[row - 1][col + 1].value == 1:  # up right is a dark piece
                    if col != 6 and board[row - 2][col + 2] is None:
                        possible_moves.append((row - 2, col + 2))

    return possible_moves

# TODO possible king moves - 3 for white king - 4 for dark king

def move(location, destination):
    #TODO refactor the move method for object handeling

    # warning! this method assumes all inputs are valid and in bounds
    # only moves pieces and removes takes
    diff_row = (destination[0] - location[0])
    diff_col = (destination[1] - location[1])

    print("diff row/ col:",diff_row, diff_col)

    #if the move is a take
    if diff_row % 2 == 0:
        remove_row = location[0] + (diff_row // 2)
        remove_col = location[1] + (diff_col // 2)
        print(remove_row, remove_col)
        board[remove_row][remove_col] = None

    # reassigns the location attribute to the moved piece
    board[location].update_loc(destination)
    # moves the element within the board array
    board[destination] = board[location]
    # removes the original piece in the board
    board[location] = None

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

def return_clicked_piece(pos, board):
    x, y = pos
    if (50 <= x <= 450) & (50 <= y <= 450): #clicked on the board
        i = (x - 50) // 50
        j = (y - 50) // 50
        return board[j][i] # WARNING - can return None

def display_board_state(board):
    for element in board.flat:
        if element is not None:
            pygame.draw.circle(screen, element.color , element.rects.center, 15)

####################################################### just messin around

potential_move_pieces = []
def load_potential_move_pieces(loc_list):
    # loads and updates the board with the current list of potential moves
    # TODO First remove all potential moves beforehand
    for i in range(8):
        for j in range(8):
            if possible_moves_board[i][j] is not None:
                if possible_moves_board[i][j].value == 99:
                    possible_moves_board[i][j] = None
    for loc in loc_list:
        x, y = loc
        piece = Piece(loc,99)
        possible_moves_board[x][y]=piece

possible_moves_board = np.full((8,8),None, dtype = object)

selected_piece = None
##################################################### Just messin around


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()
            clicked_piece = return_clicked_piece(mouse_pos, board)
            ###########<
            if clicked_piece is not None:
                if clicked_piece.value != 99:
                    selected_piece = clicked_piece
                    print(selected_piece.location)


            if clicked_piece is not None:
                print(get_possible_moves(clicked_piece))
                load_potential_move_pieces(get_possible_moves(clicked_piece))
            #############>
            possible_clicked_piece = return_clicked_piece(mouse_pos, possible_moves_board)
            if possible_clicked_piece is not None and selected_piece is not None:
                move(selected_piece.location, possible_clicked_piece.location)
                # clear possible moves
                possible_moves_board[:] = None
                # deselect piece
                selected_piece = None

    draw_board()

    display_board_state(board)
    ################################################# Testing
    display_board_state(possible_moves_board)
    #################################################

    pygame.display.update()