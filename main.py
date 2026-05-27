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

# Create plain surface
surf = pygame.Surface(( 100, 200 ))
surf.fill('orange')
x = 100

# Importing Images
player_surf = pygame.image.load(join('sprites', 'player.png')).convert_alpha()
star_surf = pygame.image.load(join('sprites', 'star.png')).convert_alpha()
star_positions = [(randint(0, WIDTH), randint(0, HEIGHT)) for i in range(20)]

# Drawing Screen
while running:
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # draw the game, drawing matters in lines, display background first, then stars, then ship
    display_surface.fill('darkgray')

    for pos in star_positions:
        display_surface.blit(star_surf, pos)
    x += 1
    display_surface.blit(player_surf, ( x, 150 ))
    pygame.display.update()

pygame.quit()