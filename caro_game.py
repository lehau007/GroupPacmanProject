import pygame
import sys
import random
import math

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 15, 15
CELL_SIZE = WIDTH // COLS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_COLOR = (100, 100, 100) 

# Initialize the board
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro Game")

# Draw the board
def draw_board():
    screen.fill(WHITE)
    for row in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), 2)
    for col in range(1, COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT), 2)

# Draw X and O on the board
def draw_symbols():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE),
                                 ((col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK, ((col + 1) * CELL_SIZE, row * CELL_SIZE),
                                 (col * CELL_SIZE, (row + 1) * CELL_SIZE), 2)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 5, 2)

# Check for a win
def check_win(row, col, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 5):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - i * dr, col - i * dc
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

# Main game loop
def caro_game():
    turn = 'X'
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board()
        draw_symbols()
        pygame.display.flip()

        if turn == 'X':
            row, col = get_user_move()
        else:
            row, col = get_user_move()
        
        if board[row][col] == ' ':
            board[row][col] = turn
            if check_win(row, col, turn):
                print(f"Player {turn} wins!")
                game_over = True
            elif all(cell != ' ' for row in board for cell in row):
                print("It's a tie!")
                game_over = True
            turn = 'O' if turn == 'X' else 'X'

# Get user move
def get_user_move():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // CELL_SIZE
                row = event.pos[1] // CELL_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == ' ':
                    return row, col

# Get bot move using Minimax with Alpha-Beta Pruning
def get_bot_move():
    _, best_move = minimax(board, 3, float('-inf'), float('inf'), True)
    return best_move

# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or check_win(0, 0, 'X') or check_win(0, 0, 'O') or all(cell != ' ' for row in board for cell in row):
        return evaluate(board), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_possible_moves(board):
            new_board = make_move(board, move, 'O')
            eval, _ = minimax(new_board, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_possible_moves(board):
            new_board = make_move(board, move, 'X')
            eval, _ = minimax(new_board, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# Evaluate the game state for the bot
def evaluate(board):
    score = 0
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 'O':
                score += evaluate_direction(board, row, col, 0, 1)  # Horizontal
                score += evaluate_direction(board, row, col, 1, 0)  # Vertical
                score += evaluate_direction(board, row, col, 1, 1)  # Diagonal \
                score += evaluate_direction(board, row, col, 1, -1)  # Diagonal /
    return score

# Evaluate a specific direction for the bot
def evaluate_direction(board, row, col, dr, dc):
    opponent = 'X'
    score = 0

    for i in range(1, 5):
        r, c = row + i * dr, col + i * dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == 'O':
               
                score += 10
            elif board[r][c] == 'X':
                break
        else:
            return score

    for i in range(1, 5):
        r, c = row - i * dr, col - i * dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if board[r][c] == 'O':
                score += 10
            elif board[r][c] == 'X':
                break
        else:
            return score

    return score

# Get possible moves on the board
def get_possible_moves(board):
    return [(row, col) for row in range(ROWS) for col in range(COLS) if board[row][col] == ' ']

# Make a move on the board
def make_move(board, move, player):
    row, col = move
    new_board = [row[:] for row in board]
    new_board[row][col] = player
    return new_board

if __name__ == "__main__":
    caro_game()
