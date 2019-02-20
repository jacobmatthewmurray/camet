import numpy as np
import pygame

from itertools import combinations


N = 10
M = 10
p = 0.7

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

FPS = 60
BOX_LENGTH = 20
BUTTONHEIGHT = 50
SCREENWIDTH = M*BOX_LENGTH
SCREENHEIGHT = N*BOX_LENGTH + BUTTONHEIGHT

board = np.random.choice(a=[0, 1], size=(N, M), p=[p, 1-p])
nh = [i for i in set(combinations([-1,0,1]*2, 2)) if i != (0,0)]
rule = {True: (2,3), False: (3,3)}
history = [board]

pygame.init()
pygame.font.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('camet')
myfont = pygame.font.SysFont('Arial', 12)
textsurface = myfont.render('Next Generation', False, (0, 0, 0))


def draw_board(board):
    for i in range(N):
        for j in range(M):
            if board[i][j] == 1:
                draw_box(black, j, i)
            else:
                draw_box(white, j, i)


def draw_box(color, x, y):
    pygame.draw.rect(SCREEN, color, pygame.Rect(x * BOX_LENGTH, y * BOX_LENGTH, BOX_LENGTH, BOX_LENGTH))


def get_next_gen(lattice, nh, rule):
    nh_lattice = np.zeros(lattice.shape)
    next_gen = np.zeros(lattice.shape)
    dim_lattice = len(lattice.shape)
    dim_tuple = tuple([i for i in range(dim_lattice)])

    for n in nh:
        nh_lattice += np.roll(lattice, n, dim_tuple)

    for key in rule:
        next_gen[(lattice == key) & (nh_lattice >= rule[key][0]) & (nh_lattice <= rule[key][1])] = 1

    return next_gen


draw_board(board)
pygame.draw.rect(SCREEN, green, pygame.Rect(0, N*BOX_LENGTH, SCREENWIDTH, BUTTONHEIGHT))
SCREEN.blit(textsurface, (10, N*BOX_LENGTH+10))

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if pos[1] > N*BOX_LENGTH:
                board = get_next_gen(board, nh, rule)
                draw_board(board)
                image_data = pygame.surfarray.array3d(pygame.display.get_surface())
                print(image_data.shape)
            else:
                i = int(pos[1] / BOX_LENGTH)
                j = int(pos[0] / BOX_LENGTH)

                if board[i][j] == 1:
                    draw_box(white, j, i)
                    board[i][j] = 0

                else:
                    draw_box(black, j, i)
                    board[i][j] = 1

    FPSCLOCK.tick(FPS)
    pygame.display.flip()
