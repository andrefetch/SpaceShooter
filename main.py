import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WIDTH / 2, HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # Timer / Cooldown 
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400 # In MS
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            # Debug : print(current_time)
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
    
    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'star.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (randint(0, WIDTH), randint(0, HEIGHT)))

        self.speed = randint(50, 500)
    
    def update(self, dt: float):
        self.rect.y += self.speed * dt

        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH)

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf: str, pos: int, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, surf: str, pos: int, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
    
    def update(self, dt: float):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

def collisions():

    global running

    collision_sprites = pygame.sprite.spritecollide(player, asteroid_sprites, True)
    if collision_sprites:
        running = False

    for laser in laser_sprites:
        collied_sprites = pygame.sprite.spritecollide(laser, asteroid_sprites, True)
        if collied_sprites:
            laser.kill()

# General Setup
pygame.init() 
WIDTH = 1280
HEIGHT = 720

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# Imports
asteroid_surf = pygame.image.load(join('sprites', 'asteroid.png')).convert_alpha()
laser_surf = pygame.image.load(join('sprites', 'laser.png')).convert_alpha()
background_surf = pygame.image.load(join('sprites', 'background.png'))
background_surf = pygame.transform.scale(background_surf, (WIDTH, HEIGHT))

# Sprites
star_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
asteroid_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for _ in range(40):
    Star([star_sprites, all_sprites])

player = Player(all_sprites)

# Custom events -- Meteors / Asteroids
asteroid_event = pygame.event.custom_type()
pygame.time.set_timer(asteroid_event, randint(100, 300))

# Drawing Screen
while running:

    dt = clock.tick() / 1000
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == asteroid_event:
            x, y = randint(0, WIDTH), randint(-200, -100)
            Asteroid(asteroid_surf, (x, y), (all_sprites, asteroid_sprites))
        
    # input
    keys = pygame.key.get_pressed()

    # update
    all_sprites.update(dt)
    collisions()

    # draw the game, drawing matters in lines, display background first, then stars, then ship
    # display_surface.fill('darkgray')
    display_surface.blit(background_surf, (0, 0))

    star_sprites.draw(display_surface)
    all_sprites.draw(display_surface)
    
    pygame.display.update()

pygame.quit()