import pygame
from os.path import join
from random import randint, uniform

from settings import WIDTH, HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, laser_surf, laser_groups, laser_sound):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WIDTH / 2, HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # Dependencies the player needs in order to fire a laser.
        # Passed in instead of grabbed from globals.
        self.laser_surf = laser_surf
        self.laser_groups = laser_groups
        self.laser_sound = laser_sound

        # Timer / Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400  # In MS

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
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
            Laser(self.laser_surf, self.rect.midtop, self.laser_groups)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            self.laser_sound.play()

        self.laser_timer()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'star.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(randint(0, WIDTH), randint(0, HEIGHT)))
        self.speed = randint(50, 500)

    def update(self, dt: float):
        self.rect.y += self.speed * dt
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH)


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.orig_surf = surf
        self.image = self.orig_surf
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation = 0
        self.rotation_speed = randint(10, 30)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt: float):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        # Rotations
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.orig_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()