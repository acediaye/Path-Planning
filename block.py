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

print(BlockType.DEFAULT)
print(BlockType.WALL.value)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

n1 = Node(1, 2, 3)
print(n1.row, n1.col, n1.width)
print(n1.type)
n1.set_type(BlockType.WALL)
print(n1.type)

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
        for r in range(self.rows):
            self.grid.append([])
            for c in range(self.cols):
                item = Node(r, c, self.block_size)
                self.grid[r].append(item)
        # print(self.grid)
    
    def draw_grid(self, window):
        for row in range(np.shape(self.grid)[0]):
            for col in range(np.shape(self.grid)[1]):
                self.grid[row][col].draw(window, BLUE)  # draw blocks
        for x in range(0, self.width, self.block_size):
            pygame.draw.line(window, WHITE, (x, 0), (x, self.height))  # vertical lines
            for y in range(0, self.height, self.block_size):
                pygame.draw.line(window, WHITE, (0, y), (self.width, y))  # horizontal lines
        pygame.draw.line(window, WHITE, (self.width, 0), (self.width, self.height))  # right line
        pygame.draw.line(window, WHITE, (0, self.height), (self.width, self.height))  # bottom line
        pygame.display.update()
        
        
g = Grid(300, 300, 100)
g.create_grid()
print(g.width, g.height, g.block_size, g.rows, g.cols)
SCREEN = pygame.display.set_mode((300, 300))
g.draw_grid(SCREEN)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    