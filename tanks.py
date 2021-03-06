import pygame
import random
import math
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 640
HEIGHT = 640
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Tank Game")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    if color == 'Red':
        text_surface = font.render(text, False, RED)
    elif color == 'Green':
        text_surface = font.render(text, False, GREEN)
    else:
        text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_health_bar(surf, x, y, pct, tank):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 90) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if tank == 'green':
        pygame.draw.rect(surf, GREEN, fill_rect)
    if tank == 'red':
        pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
# players class
class Player(pygame.sprite.Sprite):
    def __init__(self, tank):
        pygame.sprite.Sprite.__init__(self)
        self.tank = tank
        self.health = 90
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        if tank == 'green':
            self.image_orig = pygame.transform.scale(green_tank, (64, 40))
            self.image_orig.set_colorkey(BLACK)
            self.image = self.image_orig
            self.left = pygame.K_a
            self.right = pygame.K_d
            self.up = pygame.K_w
            self.down = pygame.K_s
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH / 4, HEIGHT / 2)
            self.mask = pygame.mask.from_surface(self.image)
            self.rot = 0
        elif tank == 'red':
            self.image_orig = pygame.transform.scale(red_tank, (64, 40))
            self.image_orig.set_colorkey(BLACK)
            self.image = self.image_orig
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.up = pygame.K_UP
            self.down = pygame.K_DOWN
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH - (WIDTH / 4), HEIGHT / 2)
            self.mask = pygame.mask.from_surface(self.image)
            self.rot = 180
        self.speedx = 0
        self.speedy = 0
        self.rot_speed = 0
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        self.speedx = 0
        self.speedy = 0
        self.rot_speed = 0
        keystate = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if keystate[self.left]:
            self.rot_speed = 2
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        if keystate[self.right]:
            self.rot_speed = -2
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        if keystate[self.up]:
            self.rot = (self.rot + self.rot_speed) % 360
            self.rot_rad = math.radians(self.rot)
            self.speedx = int(math.cos(self.rot_rad) * 4.0)
            self.speedy = int(math.sin(self.rot_rad) * -4.0)
            self.rect.centerx += self.speedx
            self.rect.centery += self.speedy
        if keystate[self.down]:
            self.rot = (self.rot + self.rot_speed) % 360
            self.rot_rad = math.radians(self.rot)
            self.speedx = int(math.cos(self.rot_rad) * -4.0)
            self.speedy = int(math.sin(self.rot_rad) * 4.0)
            self.rect.centerx += self.speedx
            self.rect.centery += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.rot)
            all_sprites.add(bullet)
            if self.tank == 'green':
                bullets_g.add(bullet)
            if self.tank == 'red':
                bullets_r.add(bullet)
# missile class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(missile, (38, 22))
        self.rect = self.image.get_rect()
        self.image_orig = self.image
        self.image.set_colorkey(BLACK)
        self.rot = angle
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.rot_rad = math.radians(self.rot)
        self.speedx = int(math.cos(self.rot_rad) * 5.0)
        self.speedy = int(math.sin(self.rot_rad) * -5.0)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.left > WIDTH:
            self.kill()
        if self.rect.right < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
    
def show_go_screen():
    global play_game
    screen.blit(background, background_rect)
    draw_text(screen, "Tank Game!", 64, WIDTH / 2, HEIGHT / 4, WHITE)
    draw_text(screen, "Arrow keys or WASD to move, Space or Zero to fire", 22, WIDTH / 2, HEIGHT / 2, WHITE)
    draw_text(screen, "Press any key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
    pygame.display.flip()
    play_game = True
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
    

def show_end_screen(tank):
    screen.blit(background, background_rect)
    draw_text(screen, tank + " Tank Wins!", 64, WIDTH / 2, HEIGHT / 2, tank)
    draw_text(screen, "Press any key to restart", 18, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Load all game graphics
green_tank = pygame.image.load(path.join(img_dir, "tank1.png")).convert()
red_tank = pygame.image.load(path.join(img_dir, "tank2.png")).convert()
missile = pygame.image.load(path.join(img_dir, "missile1.png")).convert()
background = pygame.image.load(path.join(img_dir, "grass.png")).convert()
background_rect = background.get_rect()

explosion_anim = {}
explosion_anim['lg'] = []
for i in range(1, 25):
    filename = 'bigger_explosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)

# Game loop
play_game = False
game_over = True
running = True
while running:
    if game_over:
        if not play_game:
            show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        green = Player('green')
        red = Player('red')
        bullets_g = pygame.sprite.Group()
        bullets_r = pygame.sprite.Group()
        all_sprites.add(green, red)
        g = pygame.sprite.Group()
        r = pygame.sprite.Group()
        g.add(green)
        r.add(red)
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(pygame.sprite.Group.sprites(bullets_g)) < 3:
                green.shoot()
            elif event.key == pygame.K_KP0 and len(pygame.sprite.Group.sprites(bullets_r)) < 3:
                red.shoot()
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Update
    all_sprites.update()

    hits_green = pygame.sprite.groupcollide(g, bullets_r, False, True)
    for hit in hits_green:
        green.health -= 10
        if green.health <= 0:
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            game_over = True
            show_end_screen('Red')
    hits_red = pygame.sprite.groupcollide(r, bullets_g, False, True)
    for hit in hits_red:
        red.health -= 10
        if red.health <= 0:
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            game_over = True
            show_end_screen('Green')

    offset_x = green.rect.x - red.rect.x
    offset_y = green.rect.y - red.rect.y

    overlap = red.mask.overlap(green.mask, (offset_x, offset_y))
    if overlap:
        green.rect.x -= green.speedx
        red.rect.x -= red.speedx
        green.rect.y -= green.speedy
        red.rect.y -= red.speedy

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_health_bar(screen, 5, 5, green.health, 'green')
    draw_health_bar(screen, WIDTH - 105, 5, red.health, 'red')
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
