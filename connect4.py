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
RED_WINNER_IMG = pygame.image.load('red_winner2.png')
YELLOW_WINNER_IMG = pygame.image.load('yellow_winner2.png')
BACKGROUND = pygame.image.load('mainMenu.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (800, 800))

# Scale images to match your cell size (minus a small margin if you like)
cell_margin = 10  # Adjust as needed for aesthetics
RED_IMG = pygame.transform.scale(RED_IMG, (PLAYAREA - cell_margin, PLAYAREA - cell_margin))
YELLOW_IMG = pygame.transform.scale(YELLOW_IMG, (PLAYAREA - cell_margin, PLAYAREA - cell_margin))
YELLOW_WINNER_IMG = pygame.transform.scale(YELLOW_WINNER_IMG, (PLAYAREA - cell_margin, PLAYAREA - cell_margin))
RED_WINNER_IMG = pygame.transform.scale(RED_WINNER_IMG, (PLAYAREA - cell_margin, PLAYAREA - cell_margin))

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
#Window to check fo spaces and check for win or next move
WINDOW_LENGTH = 4

DIM = 800

def main_menu(screen):
    difficulty = "Medium"  # Default difficulty
    board_size = "Default"  # Default board size
    ai1_difficulty = "Medium"
    ai2_difficulty = "Medium"
    ai_vs_ai = False
    menu = True
    color = GREEN
    # Get the size of the image

    screen = pygame.display.set_mode((DIM, DIM))
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
        ai_vs_ai_button = font.render(f"AI vs AI: {'On' if ai_vs_ai else 'Off'}", True, color)
        ai_vs_ai_button_rect = ai_vs_ai_button.get_rect(center=(DIM // 2, 450))
        ai1_difficulty_text = font.render(f"AI 1 Difficulty: {ai1_difficulty}", True, color)
        ai1_difficulty_text_rect = ai1_difficulty_text.get_rect(center=(DIM // 2, 500))

        # Render AI 2 difficulty button and get its rectangle
        ai2_difficulty_text = font.render(f"AI 2 Difficulty: {ai2_difficulty}", True, color)
        ai2_difficulty_text_rect = ai2_difficulty_text.get_rect(center=(DIM // 2, 550))
        exit_button = font.render("Exit", True, RED)

        # Positioning the text
        screen.blit(title, (DIM // 2 - title.get_width() // 2, 130))
        screen.blit(play_button, (DIM // 2 - play_button.get_width() // 2, 230))
        screen.blit(difficulty_text, (DIM // 2 - difficulty_text.get_width() // 2, 300))
        screen.blit(board_size_text, (DIM // 2 - board_size_text.get_width() // 2, 350))
        screen.blit(exit_button, (DIM // 2 - exit_button.get_width() // 2, 600))
        screen.blit(ai_vs_ai_button, ai_vs_ai_button_rect)
        screen.blit(ai1_difficulty_text, ai1_difficulty_text_rect)
        screen.blit(ai2_difficulty_text, ai2_difficulty_text_rect)

        # Handle events and selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if ai_vs_ai_button_rect.collidepoint(mouse):
                    ai_vs_ai = not ai_vs_ai
                    ai_vs_ai_button = font.render(f"AI vs AI: {'On' if ai_vs_ai else 'Off'}", True, color)
                elif ai1_difficulty_text_rect.collidepoint(mouse):
                    # Change AI 1 difficulty and re-render the button
                    ai1_difficulty = "Easy" if ai1_difficulty == "Medium" else "Medium" if ai1_difficulty == "Hard" else "Hard"

                elif ai2_difficulty_text_rect.collidepoint(mouse):
                    # Change AI 2 difficulty and re-render the button
                    ai2_difficulty = "Easy" if ai2_difficulty == "Medium" else "Medium" if ai2_difficulty == "Hard" else "Hard"
                # Play button
                if DIM // 2 - play_button.get_width() // 2 < mouse[0] < DIM // 2 + play_button.get_width() // 2 and 230 < mouse[1] < 280:
                    menu = False
                # Difficulty selection
                elif DIM // 2 - difficulty_text.get_width() // 2 < mouse[0] < DIM // 2 + difficulty_text.get_width() // 2 and 300 < mouse[1] < 350:
                    difficulty = "Easy" if difficulty == "Medium" else "Medium" if difficulty == "Hard" else "Hard"
                # Board size selection
                elif DIM // 2 - board_size_text.get_width() // 2 < mouse[0] < DIM // 2 + board_size_text.get_width() // 2 and 350 < mouse[1] < 400:
                    board_size = "Small" if board_size == "Default" else "Default" if board_size == "Large" else "Large"
                # Exit button
                elif DIM // 2 - exit_button.get_width() // 2 < mouse[0] < DIM // 2 + exit_button.get_width() // 2 and 600 < mouse[1] < 650:
                    pygame.quit()
                    quit()
        pygame.display.update()
    return difficulty, board_size, ai_vs_ai, ai1_difficulty, ai2_difficulty

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
        for j in range(3, ROW_COUNT):
            if board[j][i] == piece and board[j-1][i+1] == piece and board[j-2][i+2] == piece and board[j-3][i+3] == piece:
                return True
    return False

        
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
                
            elif board[j][i] == 3: # RED WINNER
                #pygame.draw.circle(screen, YELLOW, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
                 
                # Calculate the position for the piece image
                pos_x = int(i * PLAYAREA + PLAYAREA / 2 - RED_WINNER_IMG.get_width() / 2)
                pos_y = height - int(j * PLAYAREA + PLAYAREA / 2 + RED_WINNER_IMG.get_height() / 2)
                screen.blit(RED_WINNER_IMG, (pos_x, pos_y))
                
            elif board[j][i] == 4: # YELLOW WINNER
                #pygame.draw.circle(screen, YELLOW, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
                 
                # Calculate the position for the piece image
                pos_x = int(i * PLAYAREA + PLAYAREA / 2 - YELLOW_WINNER_IMG.get_width() / 2)
                pos_y = height - int(j * PLAYAREA + PLAYAREA / 2 + YELLOW_WINNER_IMG.get_height() / 2)
                screen.blit(YELLOW_WINNER_IMG, (pos_x, pos_y))

    pygame.display.update()

#Looks at the current window and evaluates what the best options are
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    if window.count(piece) == 4:
        score += 500
        
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 3
    
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 8
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
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
	for r in range(3, ROW_COUNT-3):
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
                board[j][i] = piece + 2
                board[j][i+1] = piece + 2
                board[j][i+2] = piece + 2
                board[j][i+3] = piece + 2
                draw_board(board)
                return
            
    #Vertical Wim
    for i in range(COL_COUNT):
        for j in range(ROW_COUNT-3):
            if board[j][i] == piece and board[j+1][i] == piece and board[j+2][i] == piece and board[j+3][i] == piece:
                board[j][i] = piece + 2
                board[j+1][i] = piece + 2
                board[j+2][i] = piece + 2
                board[j+3][i] = piece + 2
                draw_board(board)
                return
            
    #+ Slope
    for i in range(COL_COUNT-3):
        for j in range(ROW_COUNT-3):
            if board[j][i] == piece and board[j+1][i+1] == piece and board[j+2][i+2] == piece and board[j+3][i+3] == piece:
                board[j][i] = piece + 2
                board[j+1][i+1] = piece + 2
                board[j+2][i+2] = piece + 2
                board[j+3][i+3] = piece + 2
                draw_board(board)
                return
            
    #- Slope
    for i in range(COL_COUNT-3):
        for j in range(3, ROW_COUNT):
            if board[j][i] == piece and board[j-1][i+1] == piece and board[j-2][i+2] == piece and board[j-3][i+3] == piece:
                board[j][i] = piece + 2
                board[j-1][i+1] = piece + 2
                board[j-2][i+2] = piece + 2
                board[j-3][i+3] = piece + 2
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

def get_depth(difficulty):
    if difficulty == "Easy":
        return 1
    elif difficulty == "Medium":
        return 3
    else:
        return 6
    
def ai_move(ai_piece, depth):
    col, minimax_score = minimax(board, depth, -math.inf, math.inf, True)

    if is_valid(board, col):
        row = next_row(board, col)
        add_piece(board, row, col, ai_piece)
        if win_check(board, ai_piece):
            color_winning_pieces(board, ai_piece)
            global game_over
            game_over = True

        draw_board(board)


game_over = False
turn = random.randint(PLAYER, AI)
pygame.init()
width = 7 * PLAYAREA
screen = pygame.display.set_mode((800, 600))
difficulty, board_size, ai_vs_ai, ai1_difficulty, ai2_difficulty = main_menu(screen)

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
        
        if ai_vs_ai and not game_over:
            pygame.time.wait(1000)
            current_depth = get_depth(ai1_difficulty) if turn == PLAYER else get_depth(ai2_difficulty)
            current_piece = PLAYER_PIECE if turn == PLAYER else AI_PIECE
            ai_move(current_piece, current_depth)
            turn = AI if turn == PLAYER else PLAYER
            draw_board(board)
            pygame.display.update()
        else:           
            if event.type == pygame.MOUSEMOTION and turn == PLAYER:
                # Clear the top area where the piece is displayed
                pygame.draw.rect(screen, BLACK, (0, 0, width, PLAYAREA))
                posx = event.pos[0]
                # Center the RED_IMG around the mouse cursor
                piece_center_x = posx - RED_IMG.get_width() // 2
                # Assuming the height of RED_IMG is not more than PLAYAREA
                screen.blit(RED_IMG, (piece_center_x, (PLAYAREA - RED_IMG.get_height()) // 2))
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER: #Player Turn
                pygame.draw.rect(screen, BLACK, (0, 0, width, PLAYAREA))
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
            depth = get_depth(difficulty)
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
                turn = PLAYER

                print_board(board)
                draw_board(board)
                #Changes the turn from AI to player or vise versa

    if game_over:
        pygame.display.update()
        pygame.time.wait(5000)
