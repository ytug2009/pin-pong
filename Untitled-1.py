import pygame
from pygame import *

# Инициализация Pygame
pygame.init()

# Константы
win_width = 700
win_height = 700
speed_x = 3
speed_y = 3

# Настройка окна
window = display.set_mode((win_width, win_height))
display.set_caption('Пинг-понг')
background = transform.scale(image.load("фон.png"), (win_width, win_height))

# Классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# Создание объектов
rocket1 = Player('рокетка.png', 5, 200, 20, 150, 4)
rocket2 = Player('рокетка.png', 600, 200, 20, 150, 4)
ball = GameSprite('мяч.png', 200, 200, 50, 50, 4)

# Настройка шрифта
font.init()
font = font.SysFont('Arial', 70)
win1 = font.render('Player 1 WIN!', True, (255, 215, 0))
win2 = font.render('Player 2 WIN!', True, (255, 215, 0))

# Настройка музыки
mixer.init()
mixer.music.load('звук.ogg')
mixer.music.play()

# Игровые переменные
finish = False
game = True
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_r and finish:  # Перезапуск игры по клавише R
            ball.rect.x = 200
            ball.rect.y = 200
            speed_x = 3
            speed_y = 3
            finish = False

    if not finish:
        window.blit(background, (0, 0))
        
        # Обновление позиций
        rocket1.update_l()
        rocket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # Проверка столкновений с верхом и низом
        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1

        # Проверка столкновений с ракетками
        if sprite.collide_rect(rocket1, ball) or sprite.collide_rect(rocket2, ball):
            speed_x *= -1

        # Проверка выхода мяча за границы
        if ball.rect.x < 0:
            finish = True
            window.blit(win2, (200, 200))  # Победа игрока 2
        elif ball.rect.x > win_width - 50:
            finish = True
            window.blit(win1, (200, 200))  # Победа игрока 1

        # Отрисовка спрайтов
        rocket1.reset()
        rocket2.reset()
        ball.reset()

    display.update()
    clock.tick(60)

pygame.quit()