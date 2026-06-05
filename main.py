import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WIDTH / 2, HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print('fire laser')

class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'star.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (randint(0, WIDTH), randint(0, HEIGHT)))

        self.speed = randint(50, 500)
    
    def update(self, dt):
        self.rect.y += self.speed * dt

        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH)


# General Setup
pygame.init() 
WIDTH = 1280
HEIGHT = 720

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# Create plain surface
surf = pygame.Surface(( 100, 200 ))
surf.fill('orange')
x = 100

star_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

for _ in range(40):
    Star([star_sprites, all_sprites])

player = Player(all_sprites)

# Asteroid
asteroid_surf = pygame.image.load(join('sprites', 'asteroid.png')).convert_alpha()
asteroid_rect = asteroid_surf.get_frect(center = (WIDTH / 2, HEIGHT / 2))

# Laser
laser_surf = pygame.image.load(join('sprites', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, HEIGHT - 20))

# Background
background_surf = pygame.image.load(join('sprites', 'background.png'))
background_surf = pygame.transform.scale(background_surf, (WIDTH, HEIGHT))

# Drawing Screen
while running:

    dt = clock.tick() / 1000
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # input
    keys = pygame.key.get_pressed()

    all_sprites.update(dt)

    # draw the game, drawing matters in lines, display background first, then stars, then ship
    # display_surface.fill('darkgray')
    display_surface.blit(background_surf, (0, 0))
    
    star_sprites.draw(display_surface)
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()