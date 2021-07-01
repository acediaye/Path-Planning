from enum import Enum
import pygame
import numpy as np

class BlockType(Enum):
    DEFAULT = 1
    WALL = 2
    START = 3
    END = 4
    OPEN = 5
    CLOSED = 6
    PATH = 7

# print(BlockType.DEFAULT)
# print(BlockType.WALL.value)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

class Node(object):
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.width = width
        self.type = BlockType.DEFAULT
        self.gCost = 0
        self.hCost = 0
        self.fCost = self.gCost + self.hCost
        self.rect = pygame.Rect(self.x, self.y, width, width)
    
    def draw(self, window, color):
        pygame.draw.rect(window, color, self.rect)
    
    def set_type(self, x: BlockType):
        self.type = x
        
    def get_rect(self):
        return self.rect

# n1 = Node(1, 2, 3)
# print(n1.row, n1.col, n1.width)
# print(n1.type)
# n1.set_type(BlockType.WALL)
# print(n1.type)

class Grid(object):
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.block_size = size
        self.rows = int(width / size)
        self.cols = int(height / size)
        self.grid = None
    
    def create_grid(self):
        self.grid = []
        for row in range(self.rows):
            self.grid.append([])
            for col in range(self.cols):
                item = Node(row, col, self.block_size)
                self.grid[row].append(item)
    
    def draw_grid(self, window):
        for row in range(np.shape(self.grid)[0]):
            for col in range(np.shape(self.grid)[1]):
                # print(self.grid[row][col].type)
                if self.grid[row][col].type == BlockType.DEFAULT:
                    self.grid[row][col].draw(window, GRAY)  # draw blocks
                elif self.grid[row][col].type == BlockType.WALL:
                    self.grid[row][col].draw(window, BLACK)  # draw blocks
                elif self.grid[row][col].type == BlockType.PATH:
                    self.grid[row][col].draw(window, MAGENTA)
        for x in range(0, self.width, self.block_size):
            pygame.draw.line(window, WHITE, (x, 0), (x, self.height))  # vertical lines
            for y in range(0, self.height, self.block_size):
                pygame.draw.line(window, WHITE, (0, y), (self.width, y))  # horizontal lines
        pygame.draw.line(window, WHITE, (self.width, 0), (self.width, self.height))  # right line
        pygame.draw.line(window, WHITE, (0, self.height), (self.width, self.height))  # bottom line
        pygame.display.update()
        
        
# g = Grid(300, 300, 100)
# g.create_grid()
# print(g.width, g.height, g.block_size, g.rows, g.cols)
# g.draw_grid(SCREEN)

pygame.init()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BLOCK_SIZE = 20

if __name__ == '__main__':
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    grid = Grid(WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)
    grid.create_grid()
    grid.draw_grid(SCREEN)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = int(pos[0] / BLOCK_SIZE)
                col = int(pos[1] / BLOCK_SIZE)
                print(f'pos: {row}, {col}')
                print(grid.grid[row][col].type)
                if grid.grid[row][col].type == BlockType.DEFAULT:
                    grid.grid[row][col].type = BlockType.WALL
                elif grid.grid[row][col].type == BlockType.WALL:
                    grid.grid[row][col].type = BlockType.PATH
                else:
                    grid.grid[row][col].type = BlockType.DEFAULT
                grid.draw_grid(SCREEN)
