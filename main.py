import pygame
from os.path import join
from random import randint

from settings import WIDTH, HEIGHT
from entities import Player, Star, Asteroid, AnimatedExplosion


def start_game():
    """Set up (or reset) a fresh playthrough."""
    global player, game_start_time, game_state

    # Clear anything left over from a previous run
    all_sprites.empty()
    star_sprites.empty()
    asteroid_sprites.empty()
    laser_sprites.empty()

    # Rebuild the scene
    for _ in range(40):
        Star([star_sprites, all_sprites])
    player = Player(all_sprites, laser_surf, (all_sprites, laser_sprites), laser_sound)

    # Start spawning asteroids and reset the score clock
    pygame.time.set_timer(asteroid_event, randint(150, 300))
    game_start_time = pygame.time.get_ticks()
    game_state = "playing"


def collisions():
    global game_state

    if pygame.sprite.spritecollide(player, asteroid_sprites, True, pygame.sprite.collide_mask):
        game_state = "title"
        pygame.time.set_timer(asteroid_event, 0)  # stop spawning asteroids

    for laser in laser_sprites:
        if pygame.sprite.spritecollide(laser, asteroid_sprites, True, pygame.sprite.collide_mask):
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()


def display_score():
    # Score is now time since THIS game started, not since the program launched
    elapsed = (pygame.time.get_ticks() - game_start_time) // 100
    text_surf = font.render(str(elapsed), False, "#d4d4d4")
    text_rect = text_surf.get_frect(midbottom=(WIDTH / 2, HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, "#d4d4d4", text_rect.inflate(20, 30), 5, 10)


def display_title():
    title_surf = title_font.render("SPACE SHOOTER", False, "#d4d4d4")
    title_rect = title_surf.get_frect(center=(WIDTH / 2, HEIGHT / 2 - 60))
    display_surface.blit(title_surf, title_rect)

    if (pygame.time.get_ticks() // 500) % 2 == 0:
        prompt_surf = font.render("Press SPACE to start", False, "#d4d4d4")
        prompt_rect = prompt_surf.get_frect(center=(WIDTH / 2, HEIGHT / 2 + 40))
        display_surface.blit(prompt_surf, prompt_rect)

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

# Fonts
font = pygame.font.Font(join('sprites', 'HomeVideo.ttf'), 40)
title_font = pygame.font.Font(join('sprites', 'HomeVideo.ttf'), 80)

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

# Custom event -- Meteors / Asteroids
asteroid_event = pygame.event.custom_type()

# State that start_game() will fill in. Stars exist now so the title has a backdrop.
game_state = "title"
game_start_time = 0
player = None
for _ in range(40):
    Star([star_sprites, all_sprites])

# Game loop
while running:
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "title":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_game()

        elif game_state == "playing":
            if event.type == asteroid_event:
                x, y = randint(0, WIDTH), randint(-200, -100)
                Asteroid(asteroid_surf, (x, y), (all_sprites, asteroid_sprites))

    # update + draw, branching on which state we're in
    display_surface.blit(background_surf, (0, 0))

    if game_state == "title":
        star_sprites.update(dt)     
        star_sprites.draw(display_surface)
        display_title()

    elif game_state == "playing":
        all_sprites.update(dt)
        collisions()
        star_sprites.draw(display_surface)
        display_score()
        all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()