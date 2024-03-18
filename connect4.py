import numpy as np
import pygame
import sys
import math

BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

ROW_COUNT = 6
COL_COUNT = 7

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
            if board[j][i] == 1:
                pygame.draw.circle(screen, RED, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
            elif board[j][i] == 2:
                pygame.draw.circle(screen, YELLOW, (int(i*PLAYAREA+PLAYAREA/2), height-int(j*PLAYAREA+PLAYAREA/2)), RADIUS)
    pygame.display.update()



board = create_board()
print_board(board)
game_over = False
turn = 0
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
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(PLAYAREA/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(PLAYAREA/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, PLAYAREA))
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/PLAYAREA))

                if is_valid(board, col):
                    row = next_row(board, col)
                    add_piece(board, row, col, 1)

                    if win_check(board, 1):
                        label = font.render("Red wins!!", 1, RED)
                        screen.blit(label, (130, 10))
                        game_over = True

            else:
                posx = event.pos[0]
                col = int(math.floor(posx/PLAYAREA))

                if is_valid(board, col):
                    row = next_row(board, col)
                    add_piece(board, row, col, 2)

                    if win_check(board, 2):
                        label = font.render("Yellow wins!!", 1, YELLOW)
                        screen.blit(label, (130, 10))
                        game_over = True
            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(2500)
