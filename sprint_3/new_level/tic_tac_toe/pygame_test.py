# pygame_test.py

# Импортировать библиотеку Pygame.
import pygame
from gameparts import Board

# Инициализировать библиотеку Pygame.
pygame.init()

pygame.init()

# Здесь определены разные константы, например 
# размер ячейки и доски, цвет и толщина линий.
# Эти константы используются при отрисовке графики. 
CELL_SIZE = 100
BOARD_SIZE = 3
WIDTH = HEIGHT = CELL_SIZE * BOARD_SIZE
LINE_WIDTH = 15
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)
X_WIDTH = 15
O_WIDTH = 15
SPACE = CELL_SIZE // 4

# Создать окно размером 800x600 точек (или пикселей).
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Установить заголовок окна.
pygame.display.set_caption('Крестики-нолики')
# Заполнить фон окна заданным цветом.
screen.fill(BG_COLOR)


def draw_lines():
    # Горизонтальные линии.
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * CELL_SIZE),
            (WIDTH, i * CELL_SIZE),
            LINE_WIDTH
        )

    # Вертикальные линии.
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, HEIGHT),
            LINE_WIDTH
        )


def draw_figures(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE),
                    (
                        col * CELL_SIZE + CELL_SIZE - SPACE,
                        row * CELL_SIZE + CELL_SIZE - SPACE
                    ),
                    X_WIDTH
                )
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (
                        col * CELL_SIZE + SPACE,
                        row * CELL_SIZE + CELL_SIZE - SPACE
                    ),
                    (
                        col * CELL_SIZE + CELL_SIZE - SPACE,
                        row * CELL_SIZE + SPACE
                    ),
                    X_WIDTH
                )
            elif board[row][col] == 'O':
                pygame.draw.circle(
                    screen,
                    O_COLOR,
                    (
                        col * CELL_SIZE + CELL_SIZE // 2,
                        row * CELL_SIZE + CELL_SIZE // 2
                    ),
                    CELL_SIZE // 2 - SPACE,
                    O_WIDTH
                )


def save_result(message: str):
    filepath = (f'/home/aavdonin/git/yandex_pract/sprint_3/'
                f'new_level/tic_tac_toe/result.txt')
    with open(filepath, 'a') as result:
        result.write(message + '\n')


def main():
    game = Board()
    current_player = 'X'
    running = True
    draw_lines()
    
    # В цикле обрабатываются такие события, как
    # нажатие кнопок мыши и закрытие окна.
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_y = event.pos[0]
                mouse_x = event.pos[1]

                clicked_row = mouse_x // CELL_SIZE
                clicked_col = mouse_y // CELL_SIZE

                # Сюда нужно дописать код:
                # если ячейка свободна,
                    # то сделать ход,
                    # проверить на победу,
                    # проверить на ничью,
                    # сменить игрока. 
                    ...
                    draw_figures(game.board)
        
        # Обновить окно игры.
        pygame.display.update()
    
    # Деинициализирует все модули pygame, которые были инициализированы ранее.
    pygame.quit()


if __name__ == '__main__':
    main() 