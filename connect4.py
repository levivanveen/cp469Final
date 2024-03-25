import numpy as np
import pygame
import sys
import math
import random

#Colours for board and pieces
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

#Board Sizing
ROW_COUNT = 6
COL_COUNT = 7

#Represent whos turn it is
PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
#Window to check fo spaces and check for win or next move
WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board
#Drops piece into given board either 1 for player or 2 for AI
def add_piece(board, row, col, piece):
    board[row][col] = piece
#Checks if the decided spot is a valid location
def is_valid(board, col):
    return board[ROW_COUNT-1][col] == 0
#Assures we are looking at the next open space in a colum
def next_row(board, col):
    for i in range(ROW_COUNT):
        if board[i][col] == 0:
            return i
        
def print_board(board):
    print(np.flip(board, 0))

#Checks for all possible combos for a connect 4
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
            if board[j][i] == 1:
                pygame.draw.circle(screen, RED, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
            elif board[j][i] == 2:
                pygame.draw.circle(screen, YELLOW, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
    pygame.display.update()

#Looks at the current window and evaluates what the best options are
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

#When a game is won
def terminal_node(board):
     return win_check(board, PLAYER_PIECE) or win_check(board, AI_PIECE) or len(get_valid_locations(board)) == 0

#Recursivly checks for best possible moves in a tree of a given depth and ignores loss cases using alpha beta pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if win_check(board, AI_PIECE):
				return (None, 100000000000000)
			elif win_check(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = next_row(board, col)
			b_copy = board.copy()
			add_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = next_row(board, col)
			b_copy = board.copy()
			add_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value
        
def get_valid_locations(board):
    valid_loc = []
    for col in range(COL_COUNT):
        if is_valid(board, col):
            valid_loc.append(col)
    return valid_loc


board = create_board()
print_board(board)
game_over = False
turn = random.randint(PLAYER, AI)
pygame.init()

PLAYAREA = 100 #Size of a given slot in the board

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
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN: #Player Turn
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
                    
                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)
            #AI Turn
    if turn == AI and not game_over:
        col, minimax_score = minimax(board, 2, -math.inf, math.inf, True)

        if is_valid(board, col):
            row = next_row(board, col)
            add_piece(board, row, col, AI_PIECE)

            if win_check(board, AI_PIECE):
                label = font.render("Yellow wins!!", 1, YELLOW)
                screen.blit(label, (130, 10))
                game_over = True
            print_board(board)
            draw_board(board)
            #Changes the turn from AI to player or vise versa
            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(2500)
