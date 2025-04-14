import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Шрифт для счетчика очков
font = pygame.font.Font(None, 74)

# Класс ракетки
class Paddle:
    def __init__(self, x, y):
        self.width = 10
        self.height = 100
        self.x = x
        self.y = y
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        if keys[up] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

# Класс мяча
class Ball:
    def __init__(self, x, y):
        self.size = 15
        self.x = x
        self.y = y
        self.speed_x = 4
        self.speed_y = 4

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size // 2)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Отскок от верхней и нижней границы
        if self.y - self.size // 2 <= 0 or self.y + self.size // 2 >= SCREEN_HEIGHT:
            self.speed_y *= -1

        # Проверка выхода за левую или правую границу
        if self.x - self.size // 2 <= 0:
            return "player2"
        if self.x + self.size // 2 >= SCREEN_WIDTH:
            return "player1"
        return None

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x *= -1

    def check_collision(self, paddle):
        ball_rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
        if ball_rect.colliderect(paddle.rect):
            self.speed_x *= -1

# Создание объектов
paddle1 = Paddle(50, SCREEN_HEIGHT // 2 - 50)
paddle2 = Paddle(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 - 50)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Счетчики очков
score_player1 = 0
score_player2 = 0

# Основной цикл игры
clock = pygame.time.Clock()

while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Движение мяча
    result = ball.move()

    # Обработка результатов
    if result == "player1":
        score_player1 += 1
        ball.reset()
    elif result == "player2":
        score_player2 += 1
        ball.reset()

    # Проверка столкновений мяча с ракетками
    ball.check_collision(paddle1)
    ball.check_collision(paddle2)

    # Управление ракетками
    paddle1.move(pygame.K_w, pygame.K_s)
    paddle2.move(pygame.K_UP, pygame.K_DOWN)

    # Отрисовка объектов
    paddle1.draw()
    paddle2.draw()
    ball.draw()

    # Отрисовка счетчиков очков
    score_text1 = font.render(str(score_player1), True, RED)
    score_text2 = font.render(str(score_player2), True, BLUE)
    screen.blit(score_text1, (SCREEN_WIDTH // 4, 20))
    screen.blit(score_text2, (3 * SCREEN_WIDTH // 4, 20))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)



