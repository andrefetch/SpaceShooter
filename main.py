import pygame
from os.path import join
from random import randint

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

# Player
player_surf = pygame.image.load(join('sprites', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center = (WIDTH / 2, HEIGHT / 2))
player_direction = pygame.math.Vector2(1, 1)
player_speed = 200

# Stars
star_surf = pygame.image.load(join('sprites', 'star.png')).convert_alpha()
star_positions = [[randint(0, WIDTH), randint(0, HEIGHT)] for i in range(20)]
star_speed = 300

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


    # draw the game, drawing matters in lines, display background first, then stars, then ship
    # display_surface.fill('darkgray')
    display_surface.blit(background_surf, (0, 0))

    for pos in star_positions:
        pos[1] += star_speed * dt
        if pos[1] > HEIGHT:
            pos[1] = 0
            pos[0] = randint(0, WIDTH)
        display_surface.blit(star_surf, pos)

    display_surface.blit(asteroid_surf, asteroid_rect)
    display_surface.blit(laser_surf, laser_rect)

    # Player Movement
    if player_rect.bottom >= HEIGHT or player_rect.top <= 0:
        player_direction.y *= -1
    if player_rect.right >= WIDTH or player_rect.left <= 0:
        player_direction.x *= -1
    player_rect.center += player_direction * player_speed * dt
    display_surface.blit(player_surf, player_rect)

    pygame.display.update()

pygame.quit()