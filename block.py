from enum import Enum
import pygame
import numpy as np
# import pprint


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
        # node variables
        self.row = row
        self.col = col
        # x, y in pixels count
        self.x = row*block_size
        self.y = col*block_size
        self.block_size = block_size
        self.type = BlockType.DEFAULT
        self.gCost = 0  # distance from starting node
        self.hCost = 0  # distance from end node
        self.fCost = self.gCost + self.hCost  # total cost
        self.parent = None
        self.rect = pygame.Rect(self.x, self.y, block_size, block_size)

    def draw(self, window, color):
        pygame.draw.rect(window, color, self.rect)

    def set_type(self, x: BlockType):
        self.type = x
        
    def set_gCost(self, x: int):
        self.gCost = x
    
    def set_hCost(self, x: int):
        self.hCost = x
    
    def set_fCost(self, x: int):
        self.fCost = x


# n1 = Node(1, 2, 3)
# print(n1.row, n1.col, n1.width)
# print(n1.type)
# n1.set_type(BlockType.WALL)
# print(n1.type)


class Grid(object):
    def __init__(self, width, height, block_size):
        # window variables
        self.width = width
        self.height = height
        self.block_size = block_size
        # grid variables
        self.rows = int(width / block_size)
        self.cols = int(height / block_size)
        self.grid = None
        # self.pp = pprint.PrettyPrinter(indent=4)

    def create_grid(self):
        self.grid = []
        for row in range(self.rows):
            self.grid.append([])
            for col in range(self.cols):
                item = Node(row, col, self.block_size)
                self.grid[row].append(item)
        print(f'shape grid: {np.shape(self.grid)}')

    def draw_grid(self, window):
        rows, cols = np.shape(self.grid)
        for r in range(rows):
            for c in range(cols):
                # print(self.grid[row][col].type)
                # print(row, col)
                if self.grid[r][c].type == BlockType.WALL:
                    self.grid[r][c].draw(window, BLACK)  # draw blocks
                elif self.grid[r][c].type == BlockType.START:
                    self.grid[r][c].draw(window, GREEN)
                elif self.grid[r][c].type == BlockType.END:
                    self.grid[r][c].draw(window, RED)
                elif self.grid[r][c].type == BlockType.OPEN:
                    self.grid[r][c].draw(window, CYAN)
                elif self.grid[r][c].type == BlockType.CLOSED:
                    self.grid[r][c].draw(window, MAGENTA)
                elif self.grid[r][c].type == BlockType.PATH:
                    self.grid[r][c].draw(window, BLUE)
                else:  # default
                    self.grid[r][c].draw(window, GRAY)
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
        """
        find the first start node
        """
        rows, cols = np.shape(self.grid)
        for r in range(rows):
            for c in range(cols):
                if self.grid[r][c].type == BlockType.START:
                    node = self.grid[r][c]
                    print(f'start node: {r}, {c}')
                    return node
                else:
                    pass
        return None

    def find_end_node(self):
        """
        find the first end node
        """
        rows, cols = np.shape(self.grid)
        for r in range(rows):
            for c in range(cols):
                if self.grid[r][c].type == BlockType.END:
                    node = self.grid[r][c]
                    print(f'end node: {r}, {c}')
                    return node
                else:
                    pass
        return None

    def find_neighbors(self, current_block: Node):
        """
        given block, find the 8 neighbor blocks
        return: list
            list of neighbors
        """
        neighbors = []
        temp_r = current_block.row
        temp_c = current_block.col
        rows, cols = np.shape(self.grid)
        for i in range(current_block.row-1, current_block.row+2, 1):
            for j in range(current_block.col-1, current_block.col+2, 1):
                if i >= 0 and i <= rows:
                    if j >= 0 and j <= cols:
                        neighbors.append(self.grid[i][j])
                        # print(i, j)
        neighbors.remove(self.grid[temp_r][temp_c])
        # print(len(neighbors))
        return neighbors

    def print_fcost(self):
        rows, cols = np.shape(self.grid)
        arr = np.zeros(shape=(rows, cols), dtype=int)
        for r in range(rows):
            for c in range(cols):
                arr[r][c] = self.grid[r][c].fCost
        arr = arr.T  # pygame is in col x row instead
        print('f cost')
        print(arr)
    
    def print_gcost(self):
        rows, cols = np.shape(self.grid)
        arr = np.zeros(shape=(rows, cols), dtype=int)
        for r in range(rows):
            for c in range(cols):
                arr[r][c] = self.grid[r][c].gCost
        arr = arr.T  # pygame is in col x row instead
        print('g cost')
        print(arr)
    
    def print_hcost(self):
        rows, cols = np.shape(self.grid)
        arr = np.zeros(shape=(rows, cols), dtype=int)
        for r in range(rows):
            for c in range(cols):
                arr[r][c] = self.grid[r][c].hCost
        arr = arr.T  # pygame is in col x row instead
        print('h cost')
        print(arr)

# g = Grid(300, 300, 100)
# g.create_grid()
# print(g.width, g.height, g.block_size, g.rows, g.cols)
# g.draw_grid(SCREEN)


class Astar(object):
    def __init__(self, gridOb: Grid):
        # grid object
        self.gridOb = gridOb
        # actual grid
        self.grid = gridOb.grid

    def distance(self, block1: Node, block2: Node):
        """
        block 1, block 2: nodes
        return
            cartesian distance
        """
        dist_x = abs(block1.x - block2.x)
        dist_y = abs(block1.y - block2.y)
        dist = np.sqrt(dist_x**2 + dist_y**2)
        return int(dist)  # float into int, scaling in pixels

    def find_path(self, start_block: Node, end_block: Node):
        open_list = []
        closed_list = []
        open_list.append(start_block)

        while len(open_list) > 0:
            current_block = open_list[0]  # take first node in list
            for i in range(1, len(open_list)):  # find lowest f cost
                if (open_list[i].fCost < current_block.fCost  # cost smaller
                   or open_list[i].fCost == current_block.fCost
                   and open_list[i].hCost < current_block.hCost):  # closer to end
                    current_block = open_list[i]

            open_list.remove(current_block)
            current_block.type = BlockType.CLOSED
            closed_list.append(current_block)

            if current_block == end_block:
                print('stop')
                return

            for neighbor in self.gridOb.find_neighbors(current_block):
                if neighbor.type == BlockType.WALL or neighbor in closed_list:
                    continue
                else:
                    shorter_cost = (current_block.gCost
                                + self.distance(current_block, neighbor))
                    # print(shorter_cost)
                    if shorter_cost < neighbor.gCost or neighbor not in open_list:
                        neighbor.gCost = shorter_cost  # cost from start
                        neighbor.hCost = self.distance(neighbor, end_block)  # cost to end
                        neighbor.fCost = int(neighbor.gCost + neighbor.hCost)
                        neighbor.parent = current_block

                        if neighbor not in open_list:
                            neighbor.type = BlockType.OPEN
                            open_list.append(neighbor)

    def show_path(self, start_block: Node, end_block: Node):
        """
        color path
        """
        path = []
        current_block = end_block
        while current_block != start_block:
            path.append(current_block)
            current_block = current_block.parent
        path.append(start_block)
        path.reverse()

        for block in path:
            block.type = BlockType.PATH


pygame.init()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
BLOCK_SIZE = 20

if __name__ == '__main__':
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    gridOb = Grid(WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE)
    gridOb.create_grid()
    gridOb.draw_grid(SCREEN)
    cursor = BlockType.DEFAULT
    path = Astar(gridOb)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = int(pos[0] / BLOCK_SIZE)
                col = int(pos[1] / BLOCK_SIZE)
                print(f'mouse pos: {row}, {col}')
                print(gridOb.grid[row][col].type)
                # if grid.grid[row][col].type == BlockType.DEFAULT:
                #     grid.grid[row][col].type = BlockType.WALL
                # elif grid.grid[row][col].type == BlockType.WALL:
                #     grid.grid[row][col].type = BlockType.PATH
                # else:
                #     grid.grid[row][col].type = BlockType.DEFAULT
                gridOb.grid[row][col].type = cursor
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
                    print(path.distance(gridOb.grid[0][0],
                                        gridOb.grid[10][10]))
                    gridOb.find_neighbors(gridOb.grid[10][10])
                elif event.key == pygame.K_b:
                    gridOb.find_start_node()
                    gridOb.find_end_node()
                elif event.key == pygame.K_c:
                    start = gridOb.find_start_node()
                    end = gridOb.find_end_node()
                    path.find_path(start, end)
                    path.show_path(start, end)
                elif event.key == pygame.K_f:
                    gridOb.print_fcost()
                elif event.key == pygame.K_g:
                    gridOb.print_gcost()
                elif event.key == pygame.K_h:
                    gridOb.print_hcost()

        gridOb.draw_grid(SCREEN)
