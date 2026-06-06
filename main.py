import pygame
from os.path import join
from random import randint

from settings import WIDTH, HEIGHT
from entities import Player, Star, Asteroid, AnimatedExplosion


def collisions():
    global running

    if pygame.sprite.spritecollide(player, asteroid_sprites, True, pygame.sprite.collide_mask):
        running = False

    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, asteroid_sprites, True, pygame.sprite.collide_mask):
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()


def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), False, "#d4d4d4")
    text_rect = text_surf.get_frect(midbottom=(WIDTH / 2, HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, "#d4d4d4", text_rect.inflate(20, 30), 5, 10)


# General setup
pygame.init()
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# Asset loading
asteroid_surf = pygame.image.load(join('sprites', 'asteroid.png')).convert_alpha()
laser_surf = pygame.image.load(join('sprites', 'laser.png')).convert_alpha()
background_surf = pygame.image.load(join('sprites', 'background.png'))
background_surf = pygame.transform.scale(background_surf, (WIDTH, HEIGHT))
explosion_frames = [pygame.image.load(join('sprites', 'explosion', f'{i}.png')).convert_alpha() for i in range(12)]

# Font rendering
font = pygame.font.Font(join('sprites', 'HomeVideo.ttf'), 40)

# Sounds
laser_sound = pygame.mixer.Sound(join('sprites', 'audio', 'laser.wav'))
explosion_sound = pygame.mixer.Sound(join('sprites', 'audio', 'explosion.wav'))
game_music_sound = pygame.mixer.Sound(join('sprites', 'audio', 'game_music.wav'))

laser_sound.set_volume(0.2)
explosion_sound.set_volume(0.2)
game_music_sound.set_volume(0.1)
game_music_sound.play(loops=-1)

# Sprite groups
all_sprites = pygame.sprite.Group()
star_sprites = pygame.sprite.Group()
asteroid_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for _ in range(40):
    Star([star_sprites, all_sprites])

# Player gets handed the things it needs to spawn lasers
player = Player(all_sprites, laser_surf, (all_sprites, laser_sprites), laser_sound)

# Custom event -- Meteors / Asteroids
asteroid_event = pygame.event.custom_type()
pygame.time.set_timer(asteroid_event, randint(150, 300))

# Game loop
while running:
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == asteroid_event:
            x, y = randint(0, WIDTH), randint(-200, -100)
            Asteroid(asteroid_surf, (x, y), (all_sprites, asteroid_sprites))

    # update
    all_sprites.update(dt)
    collisions()

    # draw (order matters: background, stars, score, then everything else)
    display_surface.blit(background_surf, (0, 0))
    star_sprites.draw(display_surface)
    display_score()
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()