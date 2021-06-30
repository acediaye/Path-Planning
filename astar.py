import pygame
import sys
import pprint

# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# WINDOW_HEIGHT = 400
# WINDOW_WIDTH = 400
# SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# def draw_grid():
#     block_size = 50
#     for x in range(0, WINDOW_WIDTH, block_size):
#         for y in range(0, WINDOW_HEIGHT, block_size):
#             rect = pygame.Rect(x, y, block_size, block_size)
#             pygame.draw.rect(SCREEN, WHITE, rect, 1)

# def draw_num():
#     font = pygame.font.SysFont('arial', 20)
#     text = font.render(str(10), True, WHITE)
#     # pygame.draw.blit(text, pygame.mouse.get_pos())
    
# if __name__ == '__main__':
#     pygame.init()
#     draw_grid()
    
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
                
#         # draw_num()
#         pygame.display.update()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 20
HEIGHT = 20
MARGIN = 5

grid = []
for row in range(10):
    grid.append([])
    for col in range(10):
        grid[row].append(0)
        
grid[1][5] = 1
pygame.init()
WINDOW_SIZE = (255, 255)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('array grid')
running = True
# clock = pygame.time.Clock()
pp = pprint.PrettyPrinter(indent=4)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0] // (WIDTH+MARGIN)
            row = pos[1] // (HEIGHT+MARGIN)
            if grid[row][col] == 0:
                grid[row][col] = 1
            else:
                grid[row][col] = 0
            
            print(f'click {pos}, coor {row} {col}')
            pp.pprint(grid)
            
    SCREEN.fill(BLACK)

    for row in range(10):
        for col in range(10):
            color = WHITE
            if grid[row][col] == 1:
                color = GREEN
            pygame.draw.rect(SCREEN, color, [(WIDTH+MARGIN)*col+MARGIN,
                                             (HEIGHT+MARGIN)*row+MARGIN,
                                             WIDTH,
                                             HEIGHT])
    # clock.tick(60)
    pygame.display.flip()
pygame.quit()
