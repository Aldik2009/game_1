import pygame as pg
from random import randint

pg.init()

win_width = 900
win_height = 970

window = pg.display.set_mode((win_width, win_height))
background = pg.transform.scale(pg.image.load('background.jpg'), (win_width, win_height))

class GameSprite(pg.sprite.Sprite):
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, image, image_left, speedx, speedy, image_down):
        self.image_normal = pg.image.load(image)
        self.image_left = pg.image.load(image_left)
        self.image_right = pg.transform.flip(self.image_left, True, False)
        self.image_d = pg.image.load(image_down)
        self.image_down = pg.transform.scale(self.image_d, (120, 160))
        self.image = self.image_normal
        self.speedx = speedx
        self.speedy = speedy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if keys[pg.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speedx
        if keys[pg.K_RIGHT] and self.rect.x < win_width - 125:
            self.rect.x += self.speedx

    def jump(self):
        global wait
        global permission
        global permission2
        if permission2 == True:
            if permission == True:
                if keys[pg.K_SPACE] and self.rect.y >= 735:
                    wait = 20
            if wait != 0:
                permission = False
                self.rect.y -= self.speedy
                wait -= 1
            if wait == 0:
                permission = True

    def stay(self):
        global wait
        global permission2
        global permission3
        if self.rect.x < 20 and keys[pg.K_UP] or self.rect.x > win_width - 140 and keys[pg.K_UP]:
            permission2 = False
            permission3 = False
            wait = 0
        else:
            permission2 = True
            permission3 = True
        self.jump()
        self.down()

    def down(self):
        if permission3 == True:
            if self.rect.y < win_height - 225 and wait == 0:
                if self.rect.y != win_height - 225:
                    self.rect.y += self.speedy

    def change_pic(self):
        global z
        global d
        if keys[pg.K_DOWN]:
            self.image = self.image_down
            z = 1
            d = 1
        else:
            self.image = self.image_normal
            if d == 1:
                z = 2
                d = 0
        if z == 1:
            self.rect.y = win_height - 165
            z = 0
        elif z == 2:
            self.rect.y = win_height - 225
            z = 0

    def side_climbing(self):
        if self.rect.x < 20 and keys[pg.K_UP]:
            self.image = self.image_left
        if self.rect.x > win_width - 140 and keys[pg.K_UP]:
            self.image = self.image_right

class Ball(GameSprite):
    def __init__(self, x, y, image, speedx, speedy, boom_time, direction_x, direction_y, spawn_time, a, spawn_wait, boom, boom_wait):
        self.image = pg.image.load(image)
        self.speedx = speedx
        self.speedy = speedy
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.boom_time = boom_time
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.spawn_time = spawn_time
        self.a = a
        self.spawn_wait = spawn_wait
        self.boom = boom
        self.boom_wait = boom_wait

    def direction_f(self):
        if self.rect.y > win_height - 80:
            self.direction_y = -1
        if self.rect.y < 400 or self.rect.y == -100:
            self.direction_y = 1
        if self.rect.x > win_width - 80:
            self.direction_x = -1
        if self.rect.x < 5:
            self.direction_x = 1

    def update(self):
        if self.direction_y == -1:
            self.rect.y -= self.speedy
        else:
            self.rect.y += self.speedy
        if self.direction_x == -1:
            self.rect.x -= self.speedx
        else:
            self.rect.x += self.speedx

    def collided(self, another_sprite):
        if self.rect.y > 400:
            if pg.sprite.collide_rect(self, another_sprite):
                self.direction_x *= -1
                self.direction_y *= -1

    def spawn_f(self):
        if self.a != self.spawn_time:
            self.spawn_wait -= 1
            if self.spawn_wait == 0:
                self.a += 1
                self.spawn_wait = 100
        else:
            self.direction_f()
            self.update()
            self.reset()

    def boom_f(self):
        global count
        global finish_game
        if count > 2:
            self.speedy = 5
            self.speedx = 5
        if count > 4:
            self.speedy = 6
            self.speedx = 6
        if count > 8:
            self.speedy = 7
            self.speedx = 7
        if count > 12:
            finish_game = True
        if self.boom != self.boom_time:
            self.boom_wait -= 1
            if self.boom_wait == 0:
                self.boom += 1
                self.boom_wait = 100
        else:
            self.rect.y = -100
            self.direction_y = 1
            self.boom = 0
            count += 1

player = Player(200, 600, 'stickman.png', 'left.png', 10, 15, 'down.png')
ball = Ball(randint(100, 800), -100, 'ball.png', 4, 3, 4, 1, 1, None, None, None, 0, 100)
ball2 = Ball(randint(100, 800), -100, 'ball.png', 4, 3, 6, -1, 1, 3, 1, 100, 0, 100)
ball3 = Ball(randint(100, 800), -100, 'ball.png', 4, 3, 8, 1, 1, 9, 1, 100, 0, 100)
mark = pg.Surface((100, 5))
mark.fill((66, 102, 245))

game = True
finish_game = False
permission = True
permission2 = True
permission3 = True
count = 0
z = 0
d = 0
clock = pg.time.Clock()
FPS = 60
wait = 0

while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False

    if finish_game != True:
        keys = pg.key.get_pressed()
        window.blit(background, (0, 0))
        window.blit(mark, (10, 400))
        player.update()
        player.stay()
        player.change_pic()
        player.side_climbing()
        ball.direction_f()
        ball.update()
        ball.reset()
        ball2.spawn_f()
        ball3.spawn_f()

        ball.collided(ball2)
        ball.collided(ball3)

        ball2.collided(ball)
        ball2.collided(ball3)

        ball3.collided(ball)
        ball3.collided(ball2)

        ball.boom_f()
        ball2.boom_f()
        ball3.boom_f()

        player.reset()

        if pg.sprite.collide_circle_ratio(0.5)(player, ball):
            finish_game = True
        
        if pg.sprite.collide_circle_ratio(0.5)(player, ball2):
            finish_game = True

        if pg.sprite.collide_circle_ratio(0.5)(player, ball3):
            finish_game = True

    pg.display.update()
    clock.tick(FPS)