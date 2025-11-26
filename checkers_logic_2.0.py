import numpy as np
import pygame
import sys

board = np.full((8,8),None, dtype = object)

# colors
RED = (255, 0, 0); ORANGE = (255, 128, 0); YELLOW = (255, 255, 0); GREEN = (0, 255, 0); BLUE = (0, 0, 255); PURPLE = (255, 0, 255); WHITE = (255, 255, 255); BLACK = (0, 0, 0); BROWN = (201, 155,100)
BACKGROUND_COLOR = (60, 95, 74)

#TODO Needs to be reworked because these combinations are bad
boardSquare1List = [WHITE, BLACK, RED, BROWN, GREEN, YELLOW]
boardSquare2List = [BLACK, WHITE, BROWN, RED, YELLOW, GREEN]
topPieceList = [RED, BLACK, BLUE, YELLOW]
bottomPieceList = [BLACK, RED,YELLOW, GREEN]
potenialColorList = [BLUE, ORANGE, BROWN, PURPLE]

#defult colors
topPieceColor = RED
bottomPieceColor = BLACK
topKingColor = YELLOW
bottomKingColor= GREEN
potenialMovePieceColor = BLUE
boardSquare1Color = boardSquare1List[0]
boardSquare2Color = boardSquare2List[0]

class Piece:
    def __init__(self, location, value):
        self.location = location
        self.x = location[0]
        self.y = location[1]
        self.value = value
        if value == -1:
            self.color = bottomPieceColor
        elif value == 1:
            self.color = topPieceColor
        elif self.value == 99:
            self.color = potenialMovePieceColor
        elif self.value == 5:
            self.color = ORANGE #bottomKingColor
        elif self.value == -5:
            self.color = topKingColor

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

    def king(self):
        # TODO potentially change the image of the piece?
        self.is_king = True
        if self.value == 1:
            self.value = 5
            self.color = bottomKingColor
        elif self.value == -1:
            self.value = -5
            self.color = topKingColor

class Player: #TODO whatever this is
    def __init__(self, color):
        self.color = color

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

def get_possible_moves(piece, jump_piece):  # 1 is red, -1 is black, 5 is red king, -5 is black king
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
                elif board[row + 1][col - 1].value == -1 or board[row + 1][col - 1].value == -5:  # down left is a dark piece
                    if col != 1 and board[row + 2][col - 2] is None:
                        possible_moves.append((row + 2, col - 2))

            if col != 7:  # check down right
                if board[row + 1][col + 1] is None:  # no piece in that loc
                    possible_moves.append((row + 1, col + 1))
                elif board[row + 1][col + 1].value == -1 or board[row + 1][col + 1].value == -5:  # down left is a dark piece
                    if col != 6 and board[row + 2][col + 2] is None:
                        possible_moves.append((row + 2, col + 2))
    # dark pieces move up
    if piece.value == -1:
        if row != 0:
            if col != 0:  # check up left
                if board[row - 1][col - 1] is None:  # no piece in that loc
                    possible_moves.append((row - 1, col - 1))
                elif board[row - 1][col - 1].value == 1 or board[row - 1][col - 1].value == 5:  # up left is a light piece
                    if col != 1 and board[row - 2][col - 2] is None:
                        possible_moves.append((row - 2, col - 2))

            if col != 7:  # check up right
                if board[row - 1][col + 1] is None:  # no piece in that loc
                    possible_moves.append((row - 1, col + 1))
                elif board[row - 1][col + 1].value == 1 or board[row - 1][col + 1].value == 5:  # up right is a dark piece
                    if col != 6 and board[row - 2][col + 2] is None:
                        possible_moves.append((row - 2, col + 2))

    if piece.value == 5: #red king
        if row != 0:
            if col != 0:  # check up left
                if board[row - 1][col - 1] is None:  # no piece in that loc
                    possible_moves.append((row - 1, col - 1))
                elif board[row - 1][col - 1].value == -1 or board[row - 1][col - 1].value == -5:  # up left is a light piece
                    if col != 1 and board[row - 2][col - 2] is None:
                        possible_moves.append((row - 2, col - 2))

            if col != 7:  # check up right
                if board[row - 1][col + 1] is None:  # no piece in that loc
                    possible_moves.append((row - 1, col + 1))
                elif board[row - 1][col + 1].value == -1 or board[row - 1][col + 1].value == -5:  # up right is a dark piece
                    if col != 6 and board[row - 2][col + 2] is None:
                        possible_moves.append((row - 2, col + 2))
        if row != 7:
            if col != 0:  # check down left
                if board[row + 1][col - 1] is None:  # no piece in that loc
                    possible_moves.append((row + 1, col - 1))
                elif board[row + 1][col - 1].value == -1 or board[row + 1][col - 1].value == -5:  # down left is a dark piece
                    if col != 1 and board[row + 2][col - 2] is None:
                        possible_moves.append((row + 2, col - 2))

            if col != 7:  # check down right
                if board[row + 1][col + 1] is None:  # no piece in that loc
                    possible_moves.append((row + 1, col + 1))
                elif board[row + 1][col + 1].value == -1 or board[row + 1][col + 1].value == -5:  # down left is a dark piece
                    if col != 6 and board[row + 2][col + 2] is None:
                        possible_moves.append((row + 2, col + 2))

    if piece.value == -5: # black king
        if row != 0:
            if col != 0:  # check up left
                if board[row - 1][col - 1] is None:  # no piece in that loc
                    possible_moves.append((row - 1, col - 1))
                elif board[row - 1][col - 1].value == 1 or board[row - 1][col - 1].value == 5:  # up left is a light piece
                    if col != 1 and board[row - 2][col - 2] is None:
                        possible_moves.append((row - 2, col - 2))

            if col != 7:  # check up right
                if board[row - 1][col + 1] is None:  # no piece in that loc
                    possible_moves.append((row - 1, col + 1))
                elif board[row - 1][col + 1].value == 1 or board[row - 1][col + 1].value == 5:  # up right is a dark piece
                    if col != 6 and board[row - 2][col + 2] is None:
                        possible_moves.append((row - 2, col + 2))
        if row != 7:
            if col != 0:  # check down left
                if board[row + 1][col - 1] is None:  # no piece in that loc
                    possible_moves.append((row + 1, col - 1))
                elif board[row + 1][col - 1].value == 1 or board[row + 1][col - 1].value == 5:  # down left is a dark piece
                    if col != 1 and board[row + 2][col - 2] is None:
                        possible_moves.append((row + 2, col - 2))

            if col != 7:  # check down right
                if board[row + 1][col + 1] is None:  # no piece in that loc
                    possible_moves.append((row + 1, col + 1))
                elif board[row + 1][col + 1].value == 1 or board[row + 1][col + 1].value == 5:  # down left is a dark piece
                    if col != 6 and board[row + 2][col + 2] is None:
                        possible_moves.append((row + 2, col + 2))

    # if the double jump piece is active, remove any potential moves that are not jumps
    if jump_piece is not None:
        temp_list = []
        for loc in possible_moves:
            if (loc[0] - col % 2 == 0) or (loc[1] - row % 2 == 0):
                temp_list.append(loc)
        possible_moves = temp_list
    print(possible_moves)
    return possible_moves

def move(location, destination):
    # promote to king if necessary
    if board[location[0]][location[1]].value == -1:
        if destination[0] == 0:
            board[location[0]][location[1]].king()

    if board[location[0]][location[1]].value == 1:
        if destination[0] == 7:
            board[location[0]][location[1]].king()

    # warning! this method assumes all inputs are valid and in bounds
    # only moves pieces and removes takes
    diff_row = (destination[0] - location[0])
    diff_col = (destination[1] - location[1])

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
            if j % 2 == 0:
                pygame.draw.rect(screen, boardSquare1Color, (50 + 100 * i, 50 + 50 * j, 50, 50), 0)
                pygame.draw.rect(screen, boardSquare2Color, (100 + 100 * i, 50 + 50 * j, 50, 50), 0)
            else:
                pygame.draw.rect(screen, boardSquare2Color, (50 + 100 * i, 50 + 50 * j, 50, 50), 0)
                pygame.draw.rect(screen, boardSquare1Color, (100 + 100 * i, 50 + 50 * j, 50, 50), 0)
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
    for element in board.flat: #TODO
        global topPieceColor
        global bottomPieceColor
        global potenialMovePieceColor
        global topKingColor
        global bottomKingColor

        if element is not None and element.value == 1:
            pygame.draw.circle(screen, topPieceColor , element.rects.center, 15)
        if element is not None and element.value == -1:
            pygame.draw.circle(screen, bottomPieceColor , element.rects.center, 15)
        if element is not None and element.value == 99:
            pygame.draw.circle(screen, potenialMovePieceColor, element.rects.center, 15)
        if element is not None and element.value == 5:
            pygame.draw.circle(screen, topKingColor , element.rects.center, 15)
        if element is not None and element.value == -5:
            pygame.draw.circle(screen, bottomKingColor , element.rects.center, 15)

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
# create list of possible moves
potential_move_pieces = []
#create possible moves board (to be displayed later)
possible_moves_board = np.full((8,8),None, dtype = object)

selected_piece = None # blue potential piece
turn = 1 # default starts with red
double_jump = None

#TODO win/ stalemate checker
running = True
while running:

    for event in pygame.event.get(): # quit out of the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Test to find out how color change might work
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                boardSquare1Color = boardSquare1List[(boardSquare1List.index(boardSquare1Color) + 1) % 6]
                boardSquare2Color = boardSquare2List[(boardSquare2List.index(boardSquare2Color) + 1) % 6]
                topPieceColor = topPieceList[(topPieceList.index(topPieceColor) + 1) % 4]
                bottomPieceColor = bottomPieceList[(bottomPieceList.index(bottomPieceColor) + 1) % 4]
                potenialMovePieceColor = potenialColorList[(potenialColorList.index(potenialMovePieceColor) + 1) % 4]

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()
            clicked_piece = return_clicked_piece(mouse_pos, board) # returns the selected piece based off of the given location

            if double_jump is None: # if no double jump continue normally
                if clicked_piece is not None:

                    if clicked_piece.value == turn or clicked_piece.value == (turn *5): #checks turn
                        print(get_possible_moves(clicked_piece, double_jump))
                        load_potential_move_pieces(get_possible_moves(clicked_piece,double_jump))

                        if clicked_piece.value != 99: # if the selected piece is not a potential move piece
                            selected_piece = clicked_piece # set the selected piece
                            print(selected_piece.location)
            else: # if double jump is active
                # set the selected piece to only the jump piece
                selected_piece = double_jump
                load_potential_move_pieces(get_possible_moves(double_jump, double_jump))

                # provide a way to get out of the double jump
                possible_moves = get_possible_moves(double_jump, double_jump)
                if mouse_pos[0] > 450 or mouse_pos[1] > 450 or len(possible_moves) == 0: # if there are no possible jumps or the player clicks outside the board
                    turn *= -1 # switch the turn

                    # clear
                    possible_moves_board[:] = None
                    selected_piece = None
                    possible_clicked_piece = None
                    double_jump = None

            # if the selected piece was not assigned to the selected piece, assign it to the potential piece
            possible_clicked_piece = return_clicked_piece(mouse_pos, possible_moves_board)

            if possible_clicked_piece is not None and selected_piece is not None: # if both selected and potential are not None

                if (possible_clicked_piece.location[0] - selected_piece.location[0]) % 2 == 0: # determine if the move was a jump
                    double_jump = selected_piece # select the double jump
                else:
                    double_jump = None # clear the double jump

                move(selected_piece.location, possible_clicked_piece.location) # do the move

                if double_jump is None: # update the turn if not double jump
                    turn *= -1

                # clear possible moves
                possible_moves_board[:] = None
                # deselect piece
                selected_piece = None

    draw_board() # display checkerboard

    display_board_state(board) # display checker pieces based on their location in the board array
    display_board_state(possible_moves_board) # displays any possible pieces

    pygame.display.update()