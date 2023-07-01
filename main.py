import pygame
import random

pygame.init()

WIDTH = 1200
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SNAKE = [pygame.Rect(450, 450, 50, 50)]
FOOD = [[0, pygame.Rect(250, 250, 50, 50)]]

SCORE = 0

CURRENT_DIRECTION = 'l'


# draws the snake every render
def draw_snake():
    for i in range(0, len(SNAKE)):
        pygame.draw.rect(screen, GREEN, SNAKE[i])


def draw_food():
    if FOOD[len(FOOD) - 1][0] != 1:
        pygame.draw.rect(screen, RED, FOOD[len(FOOD)-1][1])


def food_collision():
    if SNAKE[0].colliderect(FOOD[len(FOOD)-1][1]):
        global SCORE
        SCORE += 1
        FOOD[len(FOOD) - 1][0] = 1

        if CURRENT_DIRECTION == 'l':
            SNAKE.append(pygame.Rect(SNAKE[len(SNAKE)-1].x+50, SNAKE[len(SNAKE)-1].y, 50, 50))
        elif CURRENT_DIRECTION == 'r':
            SNAKE.append(pygame.Rect(SNAKE[len(SNAKE)-1].x-50, SNAKE[len(SNAKE)-1].y, 50, 50))
        elif CURRENT_DIRECTION == 'u':
            SNAKE.append(pygame.Rect(SNAKE[len(SNAKE)-1].x, SNAKE[len(SNAKE)-1].y+50, 50, 50))
        elif CURRENT_DIRECTION == 'd':
            SNAKE.append(pygame.Rect(SNAKE[len(SNAKE)-1].x+50, SNAKE[len(SNAKE)-1].y-50, 50, 50))

        grid_blocks_x = list(range(1, 18))
        grid_blocks_y = list(range(1, 18))
        random.shuffle(grid_blocks_x)
        random.shuffle(grid_blocks_y)

        pos_x = grid_blocks_x.pop()*50
        pos_y = grid_blocks_y.pop()*50

        i = 0
        while i < len(SNAKE):
            if grid_blocks_x and grid_blocks_y:
                if SNAKE[i].x == pos_x or SNAKE[i].y == pos_y:
                    pos_x = grid_blocks_x.pop() * 50
                    pos_y = grid_blocks_y.pop() * 50
                    i = 0
            else:
                grid_blocks_x = list(range(1, WIDTH//50))
                grid_blocks_y = list(range(1, (HEIGHT-50)//50))
                random.shuffle(grid_blocks_x)
                random.shuffle(grid_blocks_y)

            i += 1

        FOOD.append([0, pygame.Rect(pos_x, pos_y, 50, 50)])


def snake_collision():
    if SNAKE[0].x < 0 or SNAKE[0].x > WIDTH or SNAKE[0].y < 50 or SNAKE[0].y > HEIGHT:
        return True

    if len(SNAKE) > 4:
        for i in range(1, len(SNAKE)):
            if SNAKE[0].colliderect(SNAKE[i]):
                return True


def move_snake():
    last_pos = []

    for i in range(0, len(SNAKE)):
        if i == 0:
            last_pos = [SNAKE[0].x, SNAKE[0].y]

            if CURRENT_DIRECTION == 'l':
                SNAKE[i].x -= 50
            elif CURRENT_DIRECTION == 'r':
                SNAKE[i].x += 50
            elif CURRENT_DIRECTION == 'u':
                SNAKE[i].y -= 50
            elif CURRENT_DIRECTION == 'd':
                SNAKE[i].y += 50
        else:
            pos = [SNAKE[i].x, SNAKE[i].y]
            SNAKE[i].x = last_pos[0]
            SNAKE[i].y = last_pos[1]

            last_pos = [pos[0], pos[1]]


def menu():
    pygame.draw.rect(screen, WHITE, (WIDTH//3, HEIGHT//4, 400, 300))
    menu_font = pygame.font.Font('freesansbold.ttf', 52)
    screen.blit(menu_font.render('Game over', True, BLACK), (WIDTH//3 + 60, HEIGHT//4 + 50))
    menu_font = pygame.font.Font('freesansbold.ttf', 42)
    screen.blit(menu_font.render('Play again', True, BLACK), (WIDTH//3 + 90, HEIGHT//4 + 175))
    pygame.draw.rect(screen, BLACK, (WIDTH//3 + 75, HEIGHT//4 + 160, 250, 75), 5)


def reset_game():
    global SNAKE, FOOD, CURRENT_DIRECTION, SCORE

    SNAKE.clear()
    FOOD.clear()
    SNAKE = [pygame.Rect(450, 450, 50, 50)]
    FOOD = [[0, pygame.Rect(250, 250, 50, 50)]]
    CURRENT_DIRECTION = 'l'
    SCORE = 0


running = True
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
paused = False

while running:
    screen.fill(BLACK)
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and paused is False:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and CURRENT_DIRECTION != 'r':
                CURRENT_DIRECTION = 'l'
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and CURRENT_DIRECTION != 'l':
                CURRENT_DIRECTION = 'r'
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and CURRENT_DIRECTION != 'd':
                CURRENT_DIRECTION = 'u'
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and CURRENT_DIRECTION != 'u':
                CURRENT_DIRECTION = 'd'
            elif event.key == pygame.K_RETURN:
                reset_game()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = pygame.mouse.get_pressed()

            if mouse_pressed[0]:
                pos_x1 = WIDTH // 3 + 75
                pos_y1 = HEIGHT // 4 + 160

                if pos_x1 < pygame.mouse.get_pos()[0] < pos_x1+250 and pos_y1 < pygame.mouse.get_pos()[1] < pos_y1+75:
                    reset_game()

    draw_snake()
    draw_food()
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 50))
    screen.blit(font.render('Score: ' + str(SCORE), True, BLACK), (500, 10))
    screen.blit(font.render("p - pause", True, BLACK), (50, 10))

    if paused is False:
        state = snake_collision()

        if state is True:
            menu()
        else:
            move_snake()
            food_collision()
    else:
        pygame.draw.rect(screen, BLACK, (WIDTH - 50, 10, 10, 30))
        pygame.draw.rect(screen, BLACK, (WIDTH - 70, 10, 10, 30))

    pygame.display.flip()

pygame.quit()
