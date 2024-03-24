import numpy as np
import pygame
import sys
import math
import random

BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

ROW_COUNT = 6
COL_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board

def add_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid(board, col):
    return board[ROW_COUNT-1][col] == 0

def next_row(board, col):
    for i in range(ROW_COUNT):
        if board[i][col] == 0:
            return i
        
def print_board(board):
    print(np.flip(board, 0))

def win_check(board, piece):
    #Horizontal wim
    for i in range(COL_COUNT-3):
        for j in range(ROW_COUNT):
            if board[j][i] == piece and board[j][i+1] == piece and board[j][i+2] == piece and board[j][i+3] == piece:
                return True
            
    #Vertical Wim
    for i in range(COL_COUNT):
        for j in range(ROW_COUNT-3):
            if board[j][i] == piece and board[j+1][i] == piece and board[j+2][i] == piece and board[j+3][i] == piece:
                return True
            
    #+ Slope
    for i in range(COL_COUNT-3):
        for j in range(ROW_COUNT-3):
            if board[j][i] == piece and board[j+1][i+1] == piece and board[j+2][i+2] == piece and board[j+3][i+3] == piece:
                return True
            
    #- Slope
    for i in range(COL_COUNT-3):
        for j in range(ROW_COUNT):
            if board[j][i] == piece and board[j-1][i+1] == piece and board[j-2][i+2] == piece and board[j-3][i+3] == piece:
                return True
            
def draw_board(board):
    for i in range(COL_COUNT):
        for j in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (i*PLAYAREA, j*PLAYAREA+PLAYAREA, PLAYAREA, PLAYAREA))
                pygame.draw.circle(screen, BLACK, (int(i*PLAYAREA+PLAYAREA/2), int(j*PLAYAREA+PLAYAREA+PLAYAREA/2)), RADIUS)

    for i in range(COL_COUNT):
        for j in range(ROW_COUNT):
            if board[j][i] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
            elif board[j][i] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
    pygame.display.update()

def evaluate_window(window, piece):
    score = 0
    
    if window.count(EMPTY) == 4:
        return 0
    
    if piece == PLAYER_PIECE:
        opponent_piece = PLAYER_PIECE
    else:
        opponent_piece = AI_PIECE
        
    if window.count(piece) == 4:
        score += 500
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 3
    
    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 8
    elif window.count(opponent_piece) == 2 and window.count(EMPTY) == 2:
        score -= 4
        
    return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COL_COUNT//2])]
	score += center_array.count(piece) * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COL_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COL_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COL_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

    ## Score negative sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COL_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score




board = create_board()
print_board(board)
game_over = False
turn = random.randint(PLAYER, AI)
pygame.init()

PLAYAREA = 100

width = COL_COUNT * PLAYAREA
height = (ROW_COUNT+1) * PLAYAREA
size = (width, height)

RADIUS = int(PLAYAREA/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("monospace", 75, bold = True)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, PLAYAREA))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(PLAYAREA/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(PLAYAREA/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, PLAYAREA))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/PLAYAREA))

                if is_valid(board, col):
                    row = next_row(board, col)
                    add_piece(board, row, col, PLAYER_PIECE)

                    if win_check(board, PLAYER_PIECE):
                        label = font.render("Red wins!!", 1, RED)
                        screen.blit(label, (130, 10))
                        game_over = True

            ## AI turn
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/PLAYAREA))

                if is_valid(board, col):
                    row = next_row(board, col)
                    add_piece(board, row, col, AI_PIECE)

                    if win_check(board, AI_PIECE):
                        label = font.render("Yellow wins!!", 1, YELLOW)
                        screen.blit(label, (70, 10))
                        game_over = True
                        
            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(2500)
