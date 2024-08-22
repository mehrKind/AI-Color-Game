""""
    Name:   Alireza Mehraban
    Github: https://github.com/mehrKind
    Email:  mr.kind1382@gmail.com
    Uni:    Jahrom University
    Date:   2024-08-20
"""


import sys
import pygame as pg
from pygame import font, draw
import time
import copy

# pg initialization
pg.init()
width = 800
height = 600
ROWS, COLS = 8, 8
tile_size = height // ROWS
limit = 2

screen = pg.display.set_mode((width, height))
pg.display.set_caption("Color Game Mehr")

# Colors
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
dark_green = (0, 164, 92)
Love_pink = (255, 0, 51)

# font
fontt = pg.font.Font(None, 24)  # You can adjust the font size as needed
font_q = pg.font.SysFont("Comic Sans MS", 20)
font_q2 = pg.font.SysFont("Times New Roman (Headings CS)", 25)

# text
code_writer = font_q.render("Alireza Mehraban", True, Love_pink)
player1_text = font_q.render("player Blue : ", True, blue)
player2_text = font_q.render("player Green : ", True, dark_green)
player1_turn_txt = font_q.render("Player Green Turn", True, dark_green)
player2_turn_txt = font_q.render("Player Blue Turn", True, blue)

    
# Initialize the board
original_board = [[{'player': 0, 'score': 0}
                   for _ in range(COLS)] for _ in range(ROWS)]
# default tiles
original_board[0][0] = {'player': 1, 'score': 5}
original_board[ROWS-1][COLS-1] = {'player': 1, 'score': 5}
original_board[0][COLS-1] = {'player': 2, 'score': 5}
original_board[ROWS-1][0] = {'player': 2, 'score': 5}


possible_moves = []
# playser scores
blue_score = 0
green_score = 0


def get_possible_move():
    global board
    return [(i, j) for i in range(ROWS) for j in range(ROWS) if board[i][j] == ' ' ]

# calculate players score from tiles and score list


def is_finish():
    global original_board
    for i in range(len(original_board)):
        for j in range(len(original_board[i])):
            if original_board[i][j]['player'] == 0:
                return False
    return True



def calc_score(board):
    blueScore = 0
    greenScore = 0
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j]["player"] == 1:
                greenScore += int(board[i][j]["score"])
            if board[i][j]["player"] == 2:
                blueScore += int(board[i][j]["score"])

    return greenScore, blueScore

# Define a function to interpolate between two colors
def interpolate_color(color1, color2, factor):
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    return (r, g, b)


# draw the game board for the first time
# Modify the drawBoard function to include a grid
def drawBoard(board):
    global possible_moves, clicked_tile, click_time
    global green_score, blue_score
    # screen.fill((255, 255, 255))
    possible_moves = []
    current_time = time.time()

    # Draw tiles and grid
    for row in range(ROWS):
        for col in range(COLS):
            target_color = black
            if board[row][col]['player'] == 1:
                target_color = green
            elif board[row][col]['player'] == 2:
                target_color = blue

            # Check if this tile was recently clicked
            if clicked_tile == (row, col) and click_time + CLICK_DURATION > current_time:
                # Draw the tile with a lightened color
                current_color = tuple(min(255, c + 100) for c in target_color)
            else:
                # Draw the tile with its original color
                current_color = target_color

            # Draw the tile
            rect_inner = pg.Rect(col * tile_size + 1, row * tile_size + 1, tile_size - 2, tile_size - 2)
            pg.draw.rect(screen, current_color, rect_inner)

            # Draw the grid
            pg.draw.line(screen, black, (col * tile_size, row * tile_size), (col * tile_size, (row + 1) * tile_size), 1)
            pg.draw.line(screen, black, (col * tile_size, row * tile_size), ((col + 1) * tile_size, row * tile_size), 1)

            # Draw the score inside the tile
            green_score, blue_score = calc_score(board)
            score_text = fontt.render(str(board[row][col]["score"]), True, black)
            
            
            text_rect = score_text.get_rect(center=(col * tile_size + tile_size // 2, row * tile_size + tile_size // 2))
            screen.blit(score_text, text_rect)

    pg.display.update()

# reset button
def drawButton():
    # Draw the button
    button_rect = pg.Rect(620, 130, 150, 40)
    pg.draw.rect(screen, Love_pink, button_rect)
    
    # Draw the button text
    button_text = font_q.render("Reset Game", True, black)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    
    return button_rect

def checkButtonClick(pos):
    global original_board
    button_rect = drawButton()
    if button_rect.collidepoint(pos):
        # Initialize the board
        original_board = [[{'player': 0, 'score': 0}
                        for _ in range(COLS)] for _ in range(ROWS)]
        # default tiles
        original_board[0][0] = {'player': 1, 'score': 5}
        original_board[ROWS-1][COLS-1] = {'player': 1, 'score': 5}
        original_board[0][COLS-1] = {'player': 2, 'score': 5}
        original_board[ROWS-1][0] = {'player': 2, 'score': 5}
        drawBoard(original_board)


# find near tile and change them to other color
def changeColorScore(row, column, originalBoard, turn):
    board = copy.deepcopy(originalBoard)
    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            if i < 0 or i >= ROWS:
                continue
            elif j < 0 or j >= ROWS:
                continue
            elif i == row and j == column:
                board[i][j]['player'] = turn
                board[i][j]['score'] = 1
            elif board[i][j]['player'] == 0:
                continue
            else:
                board[i][j]['player'] = turn
                board[i][j]['score'] = int(board[i][j]['score']) + 1
    return board


# Constants for timing
CLICK_DURATION = 0.5  # Duration in seconds for the clicked tile to remain lightened

# Variables to keep track of clicked tiles
clicked_tile = None
click_time = None


def update_board(board):
    global original_board
    original_board = board

# Cutoff test to determine the depth limit for alpha-beta pruning

def cutoffTest(state):
    return state['depth'] >= limit

# Function to generate all possible successors of a state


def successors(state, turn):
    list = []
    board = state['board']
    depth = state['depth']
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]['player'] != 0:
                continue
            list.append({'board': changeColorScore(i, j, board, turn), 'depth': depth + 1})
    return list

# Check if a square is unavailable for a move

def unavaiableSquare(board, row, column):
    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            if i < 0 or i >= ROWS:
                continue
            if j < 0 or j >= ROWS:
                continue
            if board[i][j]['player'] == 0:
                return False
    return True


# Evaluation function to estimate the desirability of a state


def evaluation(state):
    score1 = 0
    score2 = 0
    definite_score1 = 0
    definite_score2 = 0
    board = state['board']
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]['player'] == 0:
                continue
            unavailable = unavaiableSquare(board, i, j)
            score = int(board[i][j]['score'])
            if board[i][j]['player'] == 1:
                score1 += score
                if unavailable:
                    definite_score1 += score
            elif board[i][j]['player'] == 2:
                score2 += score
                if unavailable:
                    definite_score2 += score
    return 1 * (score2 - score1) + 10 * (definite_score2 - definite_score1)

# Main function for the alpha-beta pruning algorithm


def alphaBeta(state):
    state = {'board': state, 'depth': 0}
    maxState = maxChild(state, -float('inf'), float('inf'))
    board = maxState['state']['board']
    update_board(board)
    drawBoard(original_board)

# Function to get the maximum child state


def maxChild(state, a, b):
    if cutoffTest(state):
        return {'state': state, 'value': evaluation(state)}
    maxState = {'state': state, 'value': -float('inf')}
    successorsList = successors(state, 2)
    for s in successorsList:
        newState = minChild(s, a, b)
        if maxState['value'] < newState['value']:
            maxState['state'] = s
            maxState['value'] = newState['value']
            
        if maxState['value'] >= b:
            return maxState
        a = max(a, maxState['value'])
    return maxState

# Function to get the minimum child state


def minChild(state, a, b):
    if cutoffTest(state):
        return {'state': state, 'value': evaluation(state)}
    minState = {'state': state, 'value': float('inf')}
    successorsList = successors(state, 1)
    for s in successorsList:
        newState = maxChild(s, a, b)
        if minState['value'] > newState['value']:
            minState['state'] = s
            minState['value'] = newState['value']
        if minState['value'] <= a:
            return minState
        b = min(b, minState['value'])
    return minState

# Draw the initial state of the game board
screen.fill((255,255,255))
drawButton()
drawBoard(original_board)

# player turn
turn = 1



while True:
    # player turn
    player1_turn_txt = font_q.render("Player Green Turn", True, dark_green)
    player2_turn_txt = font_q.render("Player Blue Turn", True, (255,255,255))
        

    #! show player blue score
    player1_home = font_q2.render(f"{blue_score}", True, blue)
    # show player green score
    player2_home = font_q2.render(f"{green_score}", True, dark_green)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            sys.exit()
        if e.type == pg.MOUSEBUTTONDOWN:
            row = e.pos[1] // tile_size
            col = e.pos[0] // tile_size
            
            if 0 <= row < ROWS and 0 <= col < COLS and original_board[row][col]["player"] == 0:
                board = changeColorScore(row, col, original_board, 1)
                drawBoard(board)
                turn = 2
                player1_turn_txt = font_q.render("Player Green Turn", True, (255,255,255))
                player2_turn_txt = font_q.render("Player Blue Turn", True, blue)
                screen.blit(player1_turn_txt, (615, 200))
                screen.blit(player2_turn_txt, (615, 250))
                pg.display.update()
                alphaBeta(board)
                turn = 1


            # Check if the button is clicked
            checkButtonClick(e.pos)

        # Draw the background for player names
    player1_bg_rect = pg.Rect(610, 27, 180, 40)
    player2_bg_rect = pg.Rect(610, 70, 180, 40)
    pg.draw.rect(screen, (172, 216, 230), player1_bg_rect)
    pg.draw.rect(screen, (173, 230, 216), player2_bg_rect)

    screen.blit(code_writer, (615, 560))
    # player 1 score text
    screen.blit(player1_text, (615, 30))
    # player 2 score text
    screen.blit(player2_text, (615, 70))
    screen.blit(player1_home, (760, 40))
    screen.blit(player2_home, (760, 80))
    screen.blit(player1_turn_txt, (615, 200))
    screen.blit(player2_turn_txt, (615, 250))
    

    # update the game screen
    pg.display.update()