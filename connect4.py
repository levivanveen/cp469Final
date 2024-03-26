import numpy as np
import pygame
import sys
import math
import random

PLAYAREA = 100 #Size of a given slot in the board

pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init() #turn all of pygame on.

# Load images
RED_IMG = pygame.image.load('red.png')
YELLOW_IMG = pygame.image.load('yellow.png')
GREEN_IMG = pygame.image.load('green.png')
BACKGROUND = pygame.image.load('mainMenu.png')


# Scale images to match your cell size (minus a small margin if you like)
cell_margin = 10  # Adjust as needed for aesthetics
RED_IMG = pygame.transform.scale(RED_IMG, (PLAYAREA - cell_margin, PLAYAREA - cell_margin))
YELLOW_IMG = pygame.transform.scale(YELLOW_IMG, (PLAYAREA - cell_margin, PLAYAREA - cell_margin))
GREEN_IMG = pygame.transform.scale(GREEN_IMG, (PLAYAREA - cell_margin, PLAYAREA - cell_margin))

#Colours for board and pieces
BLUE = (0, 0, 255)
BLUE2 = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (7, 240, 111)
GREEN2 = (7, 145, 69)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Board Sizing
ROW_COUNT = 6
COL_COUNT = 7

#Represent whos turn it is
PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINNING_PIECE = 3
#Window to check fo spaces and check for win or next move
WINDOW_LENGTH = 4

def main_menu(screen):
    difficulty = "Medium"  # Default difficulty
    board_size = "Default"  # Default board size
    menu = True
    color = GREEN
    # Get the size of the image

    screen = pygame.display.set_mode((680, 680))
    while menu:
        screen.blit(BACKGROUND, (0, 0))
         
        #font = pygame.font.SysFont("monospace", 50)
        font = pygame.font.Font("JungleAdventurer.ttf", 50)

        # Render the menu options
        title = font.render("Connect Four!", True, (176, 16, 157))
        play_button = font.render("Play", True, BLACK)

        if (difficulty == "Medium"):
            color = YELLOW
        elif(difficulty == "Hard"):
            color = RED
        else:
             color = GREEN

        difficulty_text = font.render(f"Difficulty: {difficulty}", True, color)
        board_size_text = font.render(f"Board Size: {board_size}", True, BLACK)
        exit_button = font.render("Exit", True, RED)

        # Positioning the text
        screen.blit(title, (width // 2 - title.get_width() // 2, 130))
        screen.blit(play_button, (width // 2 - play_button.get_width() // 2, 230))
        screen.blit(difficulty_text, (width // 2 - difficulty_text.get_width() // 2, 300))
        screen.blit(board_size_text, (width // 2 - board_size_text.get_width() // 2, 400))
        screen.blit(exit_button, (width // 2 - exit_button.get_width() // 2, 500))

        # Handle events and selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # Play button
                if width // 2 - play_button.get_width() // 2 < mouse[0] < width // 2 + play_button.get_width() // 2 and 230 < mouse[1] < 250:
                    menu = False
                # Difficulty selection
                elif width // 2 - difficulty_text.get_width() // 2 < mouse[0] < width // 2 + difficulty_text.get_width() // 2 and 300 < mouse[1] < 350:
                    difficulty = "Easy" if difficulty == "Medium" else "Medium" if difficulty == "Hard" else "Hard"
                # Board size selection
                elif width // 2 - board_size_text.get_width() // 2 < mouse[0] < width // 2 + board_size_text.get_width() // 2 and 400 < mouse[1] < 450:
                    board_size = "Small" if board_size == "Default" else "Default" if board_size == "Large" else "Large"
                # Exit button
                elif width // 2 - exit_button.get_width() // 2 < mouse[0] < width // 2 + exit_button.get_width() // 2 and 500 < mouse[1] < 550:
                    pygame.quit()
                    quit()
        pygame.display.update()
    return difficulty, board_size

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
    screen.blit(BOARD_IMG, (0, PLAYAREA))
    for i in range(COL_COUNT):
        for j in range(ROW_COUNT):
                
                 
                #pygame.draw.rect(screen, BLUE, (i*PLAYAREA, j*PLAYAREA+PLAYAREA, PLAYAREA, PLAYAREA))
                pygame.draw.circle(screen, BLACK, (int(i*PLAYAREA+PLAYAREA/2), int(j*PLAYAREA+PLAYAREA+PLAYAREA/2)), RADIUS)


    for i in range(COL_COUNT):
        for j in range(ROW_COUNT):
            if board[j][i] == 1:
                #pygame.draw.circle(screen, RED, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)

                # Calculate the position for the piece image
                pos_x = int(i * PLAYAREA + PLAYAREA / 2 - RED_IMG.get_width() / 2)
                pos_y = height - int(j * PLAYAREA + PLAYAREA / 2 + RED_IMG.get_height() / 2)
                screen.blit(RED_IMG, (pos_x, pos_y))

            elif board[j][i] == 2:
                #pygame.draw.circle(screen, YELLOW, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
                 
                # Calculate the position for the piece image
                pos_x = int(i * PLAYAREA + PLAYAREA / 2 - YELLOW_IMG.get_width() / 2)
                pos_y = height - int(j * PLAYAREA + PLAYAREA / 2 + YELLOW_IMG.get_height() / 2)
                screen.blit(YELLOW_IMG, (pos_x, pos_y))
                
            elif board[j][i] == 3:
                #pygame.draw.circle(screen, YELLOW, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
                 
                # Calculate the position for the piece image
                pos_x = int(i * PLAYAREA + PLAYAREA / 2 - GREEN_IMG.get_width() / 2)
                pos_y = height - int(j * PLAYAREA + PLAYAREA / 2 + GREEN_IMG.get_height() / 2)
                screen.blit(GREEN_IMG, (pos_x, pos_y))

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
 
def color_winning_pieces(board, piece):
    #Horizontal wim
    for i in range(COL_COUNT-3):
        for j in range(ROW_COUNT):
            if board[j][i] == piece and board[j][i+1] == piece and board[j][i+2] == piece and board[j][i+3] == piece:
                board[j][i] = WINNING_PIECE
                board[j][i+1] = WINNING_PIECE
                board[j][i+2] = WINNING_PIECE
                board[j][i+3] = WINNING_PIECE
                draw_board(board)
                return
            
    #Vertical Wim
    for i in range(COL_COUNT):
        for j in range(ROW_COUNT-3):
            if board[j][i] == piece and board[j+1][i] == piece and board[j+2][i] == piece and board[j+3][i] == piece:
                board[j][i] = WINNING_PIECE
                board[j+1][i] = WINNING_PIECE
                board[j+2][i] = WINNING_PIECE
                board[j+3][i] = WINNING_PIECE
                draw_board(board)
                return
            
    #+ Slope
    for i in range(COL_COUNT-3):
        for j in range(ROW_COUNT-3):
            if board[j][i] == piece and board[j+1][i+1] == piece and board[j+2][i+2] == piece and board[j+3][i+3] == piece:
                board[j][i] = WINNING_PIECE
                board[j+1][i+1] = WINNING_PIECE
                board[j+2][i+2] = WINNING_PIECE
                board[j+3][i+3] = WINNING_PIECE
                draw_board(board)
                return
            
    #- Slope
    for i in range(COL_COUNT-3):
        for j in range(ROW_COUNT):
            if board[j][i] == piece and board[j-1][i+1] == piece and board[j-2][i+2] == piece and board[j-3][i+3] == piece:
                board[j][i] = WINNING_PIECE
                board[j-1][i+1] = WINNING_PIECE
                board[j-2][i+2] = WINNING_PIECE
                board[j-3][i+3] = WINNING_PIECE
                draw_board(board)
                return

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


game_over = False
turn = random.randint(PLAYER, AI)
pygame.init()

width = 7 * PLAYAREA
screen = pygame.display.set_mode((800, 600))
difficulty, board_size = main_menu(screen)

if difficulty == "Easy":
    depth = 1
elif difficulty == "Medium":
    depth = 3
else:
    depth = 6

if board_size == "Small":
    ROW_COUNT, COL_COUNT = 5, 6
elif board_size == "Default":
    ROW_COUNT, COL_COUNT = 6, 7
else:
    ROW_COUNT, COL_COUNT = 7, 8

BOARD_IMG = pygame.image.load('board3.png')
BOARD_IMG = pygame.transform.scale(BOARD_IMG, (COL_COUNT * PLAYAREA, ROW_COUNT * PLAYAREA))

width = COL_COUNT * PLAYAREA
height = (ROW_COUNT+1) * PLAYAREA
size = (width, height)
screen = pygame.display.set_mode(size)

RADIUS = int(PLAYAREA/2 - 5)
board = create_board()
print_board(board)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("JungleAdventurer.ttf", 75)
pygame.display.set_caption("Connect Four")

addSFX = pygame.mixer.Sound('addSFX.mp3')
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)  # Play the music indefinitely


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            # Clear the top area where the piece is displayed
            pygame.draw.rect(screen, BLACK, (0, 0, width, PLAYAREA))
            posx = event.pos[0]
            if turn == PLAYER:
                # Center the RED_IMG around the mouse cursor
                piece_center_x = posx - RED_IMG.get_width() // 2
                # Assuming the height of RED_IMG is not more than PLAYAREA
                screen.blit(RED_IMG, (piece_center_x, (PLAYAREA - RED_IMG.get_height()) // 2))
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN: #Player Turn
            pygame.draw.rect(screen, BLACK, (0, 0, width, PLAYAREA))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/PLAYAREA))

                if is_valid(board, col):
                    row = next_row(board, col)
                    add_piece(board, row, col, PLAYER_PIECE)
                    addSFX.play()

                    if win_check(board, PLAYER_PIECE):
                        color_winning_pieces(board, PLAYER_PIECE)
                        pygame.mixer.music.load('winSFX.mp3')
                        pygame.mixer.music.play(-1)  # Play the music indefinitely
                        label = font.render("You Win!!", True, RED)
                        label_rect = label.get_rect()

                        # Set the center of the rectangle to the center of the screen
                        label_rect.center = (width // 2, PLAYAREA // 2)

                        # Blit the label at the center
                        screen.blit(label, label_rect)
                        game_over = True
                    
                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)
            #AI Turn
    if turn == AI and not game_over:
        col, minimax_score = minimax(board, depth, -math.inf, math.inf, True)

        if is_valid(board, col):
            row = next_row(board, col)
            add_piece(board, row, col, AI_PIECE)

            if win_check(board, AI_PIECE):
                color_winning_pieces(board, AI_PIECE)
                pygame.mixer.music.load('loseSFX.mp3')
                pygame.mixer.music.play(-1)  # Play the music indefinitely
                label = font.render("You Lose!!", True, YELLOW)
                label_rect = label.get_rect()

                # Set the center of the rectangle to the center of the screen
                label_rect.center = (width // 2, PLAYAREA // 2)

                # Blit the label at the center
                screen.blit(label, label_rect)
                game_over = True
            print_board(board)
            draw_board(board)
            #Changes the turn from AI to player or vise versa
            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(5000)
