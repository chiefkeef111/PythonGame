from pygame import * 
from time import time as time_count
from random import randint
mixer.init()
init()
window = display.set_mode((700, 500))
game = True
display.set_caption("SpaceShooter")
background = transform.scale(
    image.load("galaxy.jpg"),
    (700, 500))




class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size, player_speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_image), size)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Enemie(GameSprite):
    def update(self):
        self.rect.y += self.speed
        self.draw_sprite()
class Bullet(GameSprite):

    def update(self):
        self.draw_sprite()
        self.rect.y -= self.speed
bullet = Bullet("bullet.png", 125, 490, (20, 20), 10)
shot_time = time_count()

class Player(GameSprite):
    def update(self, bullets):
        pressed_keys = key.get_pressed()
        if pressed_keys[K_a]:
            self.rect.x -= self.speed
        if pressed_keys[K_d]:
            self.rect.x += self.speed
        if pressed_keys[K_SPACE]:
            global shot_time
            if time_count() - shot_time >= 1:
                new_bullet = Bullet("bullet.png", self.rect.x, self.rect.y, (10, 20), 10)
                bullets.add(new_bullet)
                shot_time = time_count()

def draw_label(score):
    image = font.SysFont("Arial", 20).render("Підбито НЛО:" + str(score), True, (255))
    window.blit(image, (100, 20))
window.blit(background, (0, 0))
clock = time.Clock()
mixer.music.load("space.ogg")
mixer.music.play()

player = Player("rocket.png", 100, 400, (65, 80), 5)
enemy = Enemie("ufo.png", 100, 300, (120, 70), 5)
enemy.draw_sprite()
bullets = sprite.Group()
enemies = sprite.Group()
enemies.add(Enemie("ufo.png", 0, 0, (50, 50), 5))
while game:
    if len(enemies) < 7:
        new_enemy = Enemie('ufo.png', randint(0, 600), -100, (80, 50), 1)
        enemies.add(new_enemy)
    for e in event.get():
        if e.type == QUIT:
            game = False
    window.blit(background, (0, 0))
    enemies.update()
    bullets.update()
    for bullet in bullets:
        bullet.update()
        bullet.draw_sprite()
        sprite.spritecollide(bullet, enemies, True)
    enemies_amount = len(enemies)
    score = 0
    sprite.groupcollide(enemies, bullets, True, True)
    if len(enemies) < enemies_amount:     
        score += enemies_amount - len(enemies)
    draw_label(score)
    player.update(bullets)
    player.draw_sprite()
    display.update()
    clock.tick(60)