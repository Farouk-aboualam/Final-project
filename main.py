import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from AI.agent import Agent

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()

    game = Game(WIN)
    turn = RED
    player = RED
    AI = WHITE

    while run:
        clock.tick(FPS)
        if game.winner() is not None:
            print(game.winner())
            run = False
        if turn == player:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)
                    turn = game.turn
        else:
            if run == True:
                # Agent = State(game, AI)
                Agents = Agent(AI, game.encode(), False, [])
                move = Agents.iterativeMiniMax(Agents)
                print(move[0], move[1])
                game.agent_move(move[0], move[1])
                turn = player
        game.update()
    pygame.quit()

main()