import pygame
import random
import time
from pygame.constants import HIDDEN

WIDTH = 500
HEIGHT = 600
ROCK_COUNT = 8
FPS = 60

#game initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter") #title of game
clock = pygame.time.Clock()

#sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,40)) #setting the image of the sprite
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()  #put a rectangle around the sprite
        #self.rect.x, self.rect.y = 200, 200 #top left corner position is 200,200
        #self.rect.center = (WIDTH/2, HEIGHT/2) #center of the screen
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 20
        self.speed = 8
    def update(self):
        key_pressed = pygame.key.get_pressed()
        if(key_pressed[pygame.K_RIGHT]):
            self.rect.x += self.speed
        if(key_pressed[pygame.K_LEFT]):
            self.rect.x -= self.speed
        if(self.rect.right >= WIDTH):
            self.rect.right = WIDTH
        if(self.rect.left <= 0):
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        all_bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40)) #setting the image of the sprite
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()  #put a rectangle around the sprite
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = 0
        self.speedx = random.randint(-2,2)
        self.speedy = random.randint(3,7)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if(self.rect.bottom >= HEIGHT or self.rect.right >= WIDTH or self.rect.left <= 0):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = 0
            self.speedx = random.randint(-2,2)
            self.speedy = random.randint(3,7)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship_x, ship_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = ship_x
        self.rect.centery = ship_y
        self.speed = -10
    
    def update(self):
        self.rect.y += self.speed
        if(self.rect.bottom <= 0):
            self.kill()
        


all_sprites = pygame.sprite.Group() #group all sprites together
all_rocks = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
for i in range(ROCK_COUNT):
    rock = Rock()
    all_sprites.add(rock)
    all_rocks.add(rock)

running = True
#game loop
while running:
    clock.tick(FPS)

    #getting user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #update
    all_sprites.update() #calls update function on all sprites in the group
    #check if bullets and rocks collided, returns a list
    bullet_hit_rock = pygame.sprite.groupcollide(all_rocks, all_bullets, True, True)
    #for all rocks hit, make a new one to replace it
    for i in bullet_hit_rock:
        rock = Rock()
        all_sprites.add(rock)
        all_rocks.add(rock)

    #check if rocks hit player, returns a list of all rocks that collided with player
    rock_hit_player = pygame.sprite.spritecollide(player, all_rocks, False)
    if rock_hit_player:
        running = False

    #display
    screen.fill((150,200,200))
    all_sprites.draw(screen) #draw the all_sprite group onto screen
    pygame.display.update()
