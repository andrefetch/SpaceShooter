import pygame
from os.path import join
from random import randint, uniform

from settings import WIDTH, HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, laser_surf, laser_groups, laser_sound, damage_sound):
        super().__init__(groups)
        self.image = pygame.image.load(join('sprites', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WIDTH / 2, HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        # Sound & Laser Attributes
        self.laser_surf = laser_surf
        self.laser_groups = laser_groups
        self.laser_sound = laser_sound
        self.damage_sound = damage_sound

        # Timer / Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400  # In MS

        # Lives / damage
        self.lives = 3
        self.invincible = False
        self.hit_time = 0
        self.invincible_duration = 1500  # ms of i-frames after a hit

        # Two prebuilt versions of the sprite. set_alpha is unreliable on
        # convert_alpha() surfaces, so we make a faded copy with BLEND_RGBA_MULT
        # and just swap self.image between them to flash.
        self.original_image = self.image
        self.faded_image = self.image.copy()
        self.faded_image.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def invincibility_timer(self):
        if self.invincible:
            if pygame.time.get_ticks() - self.hit_time >= self.invincible_duration:
                self.invincible = False
                self.image = self.original_image

    def take_damage(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.hit_time = pygame.time.get_ticks()
            self.damage_sound.play()

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        
        # WASD Movement Support
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a]) or int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) # Added: Arrow Key Support
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w]) or int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        
        # Set direction and normalize so players can't speed boost.
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        # Bounding detection, so players can't move off the screen !
        self.rect.clamp_ip(pygame.FRect(0, 0, WIDTH, HEIGHT))

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(self.laser_surf, self.rect.midtop, self.laser_groups)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            self.laser_sound.play()

        self.laser_timer()
        self.invincibility_timer()

        # Flashes from white to orig to notify that a player is currently invincible
        if self.invincible:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                self.image = self.faded_image
            else:
                self.image = self.original_image


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