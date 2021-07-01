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
    def __init__(self, row, col, block_size):
        self.row = row
        self.col = col
        self.x = row*block_size
        self.y = col*block_size
        self.block_size = block_size
        self.type = BlockType.DEFAULT
        self.gCost = 0
        self.hCost = 0
        self.fCost = self.gCost + self.hCost
        self.rect = pygame.Rect(self.x, self.y, block_size, block_size)

    def draw(self, window, color):
        pygame.draw.rect(window, color, self.rect)

    def set_type(self, x: BlockType):
        self.type = x

    # def get_rect(self):
    #     return self.rect

# n1 = Node(1, 2, 3)
# print(n1.row, n1.col, n1.width)
# print(n1.type)
# n1.set_type(BlockType.WALL)
# print(n1.type)


class Grid(object):
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.rows = int(width / block_size)
        self.cols = int(height / block_size)
        self.grid = None

    def create_grid(self):
        self.grid = []
        for row in range(self.rows):
            self.grid.append([])
            for col in range(self.cols):
                item = Node(row, col, self.block_size)
                self.grid[row].append(item)
        print(f'shape grid: {np.shape(self.grid)}')

    def draw_grid(self, window):
        for row in range(np.shape(self.grid)[0]):
            for col in range(np.shape(self.grid)[1]):
                # print(self.grid[row][col].type)
                # print(row, col)
                if self.grid[row][col].type == BlockType.WALL:
                    self.grid[row][col].draw(window, BLACK)  # draw blocks
                elif self.grid[row][col].type == BlockType.START:
                    self.grid[row][col].draw(window, GREEN)
                elif self.grid[row][col].type == BlockType.END:
                    self.grid[row][col].draw(window, RED)
                elif self.grid[row][col].type == BlockType.OPEN:
                    self.grid[row][col].draw(window, CYAN)
                elif self.grid[row][col].type == BlockType.CLOSED:
                    self.grid[row][col].draw(window, MAGENTA)
                elif self.grid[row][col].type == BlockType.PATH:
                    self.grid[row][col].draw(window, BLUE)
                else:  # default
                    self.grid[row][col].draw(window, GRAY)
        for x in range(0, self.width, self.block_size):
            pygame.draw.line(window, WHITE,
                             (x, 0), (x, self.height))  # vertical lines
            for y in range(0, self.height, self.block_size):
                pygame.draw.line(window, WHITE,
                                 (0, y), (self.width, y))  # horizontal lines
        pygame.draw.line(window, WHITE,
                         (self.width, 0), (self.width, self.height))  # right
        pygame.draw.line(window, WHITE,
                         (0, self.height), (self.width, self.height))  # bottom
        pygame.display.update()

    def find_start_node(self):
        for row in range(np.shape(self.grid)[0]):
            for col in range(np.shape(self.grid)[1]):
                if self.grid[row][col].type == BlockType.START:
                    node = self.grid[row][col]
                    print(row, col)
                    return node
                else:
                    pass

    def find_end_node(self):
        for row in range(np.shape(self.grid)[0]):
            for col in range(np.shape(self.grid)[1]):
                if self.grid[row][col].type == BlockType.END:
                    node = self.grid[row][col]
                    print(row, col)
                    return node
                else:
                    pass

    def find_neighbors(self, current_block: Node):
        neighbors = []
        temp_r = current_block.row
        temp_c = current_block.col
        print(current_block.row, current_block.col)
        for i in range(current_block.row-1, current_block.row+2, 1):
            for j in range(current_block.col-1, current_block.col+2, 1):
                if i >= 0 and i <= np.shape(self.grid)[0]:
                    if j >= 0 and j <= np.shape(self.grid)[1]:
                        neighbors.append(self.grid[i][j])
                        # print(i, j)
        neighbors.remove(self.grid[temp_r][temp_c])
        print(len(neighbors))

# g = Grid(300, 300, 100)
# g.create_grid()
# print(g.width, g.height, g.block_size, g.rows, g.cols)
# g.draw_grid(SCREEN)


class Astar(object):
    def __init__(self, grid: Grid):
        self.grid = grid.grid

    def distance(self, block1: Node, block2: Node):
        # print(block1.x, block1.y, block2.x, block2.x)
        dist_x = abs(block1.x - block2.x)
        dist_y = abs(block1.y - block2.y)
        # print(dist_x, dist_y)
        dist = np.sqrt(dist_x**2 + dist_y**2)
        # print(dist)
        return int(dist)  # float into int, scaling in pixels

    def find_path(self, start_block: Node, end_block: Node):
        open_list = []
        closed_list = []
        open_list.append(start_block)

        while len(open_list) > 0:
            current_block = open_list[0]
            print(current_block.row, current_block.col)
            for i in range(1, len(open_list)):
                if open_list[i].fCost < current_block.fCost:
                    current_block = open_list[i]
                    print(current_block.row, current_block.col)

            open_list.remove(current_block)
            closed_list.append(current_block)
            current_block.type = BlockType.CLOSED

            if current_block == end_block:
                print('stop')
                print(open_list)
                print(closed_list)
                return


pygame.init()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BLOCK_SIZE = 20

if __name__ == '__main__':
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    grid = Grid(WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)
    grid.create_grid()
    grid.draw_grid(SCREEN)
    cursor = BlockType.DEFAULT
    path = Astar(grid)

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
                # if grid.grid[row][col].type == BlockType.DEFAULT:
                #     grid.grid[row][col].type = BlockType.WALL
                # elif grid.grid[row][col].type == BlockType.WALL:
                #     grid.grid[row][col].type = BlockType.PATH
                # else:
                #     grid.grid[row][col].type = BlockType.DEFAULT
                grid.grid[row][col].type = cursor
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    cursor = BlockType.DEFAULT
                    print(cursor.name)
                elif event.key == pygame.K_2:
                    cursor = BlockType.WALL
                    print(cursor.name)
                elif event.key == pygame.K_3:
                    cursor = BlockType.START
                    print(cursor.name)
                elif event.key == pygame.K_4:
                    cursor = BlockType.END
                    print(cursor.name)
                elif event.key == pygame.K_5:
                    cursor = BlockType.OPEN
                    print(cursor.name)
                elif event.key == pygame.K_6:
                    cursor = BlockType.CLOSED
                    print(cursor.name)
                elif event.key == pygame.K_7:
                    cursor = BlockType.PATH
                    print(cursor.name)
                elif event.key == pygame.K_a:
                    print(path.distance(grid.grid[0][0], grid.grid[10][10]))
                    grid.find_neighbors(grid.grid[10][10])
                elif event.key == pygame.K_b:
                    grid.find_start_node()
                    grid.find_end_node()

        grid.draw_grid(SCREEN)
