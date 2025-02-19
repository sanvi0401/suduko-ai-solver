import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 540, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku AI Solver")

# Define colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (211, 211, 211)
DARK_GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

# Define font
font = pygame.font.SysFont('Arial', 30)

# Sudoku Grid (9x9)
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Function to draw the Sudoku grid
def draw_grid():
    block_size = 60
    for i in range(10):
        # Draw grid lines
        thickness = 2 if i % 3 != 0 else 4
        pygame.draw.line(screen, BLACK, (i * block_size, 0), (i * block_size, HEIGHT), thickness)
        pygame.draw.line(screen, BLACK, (0, i * block_size), (WIDTH, i * block_size), thickness)

    # Draw numbers in cells
    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            if num != 0:
                text = font.render(str(num), True, BLACK)
                screen.blit(text, (col * block_size + 20, row * block_size + 15))

# Function to check if a number is valid in a given position
def is_valid(board, row, col, num):
    # Check the row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check 3x3 sub-grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

# Backtracking algorithm to solve the Sudoku
def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# Function to handle user input
def handle_input(pos):
    block_size = 60
    x, y = pos
    row, col = y // block_size, x // block_size

    if grid[row][col] == 0:
        # Get the input from the player (number 1-9)
        value = input("Enter a number (1-9): ")
        try:
            value = int(value)
            if 1 <= value <= 9:
                grid[row][col] = value
        except ValueError:
            pass

# Main game loop
def main():
    running = True
    selected_cell = None
    start_time = time.time()

    while running:
        screen.fill(WHITE)
        draw_grid()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    handle_input(pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key to solve
                    solve(grid)
                    print("Solved Sudoku:")
                    print(grid)
                    elapsed_time = time.time() - start_time
                    print(f"Time taken: {elapsed_time:.2f} seconds")
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
