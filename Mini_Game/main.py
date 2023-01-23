import pygame
import random

# Initializing pygame
pygame.init()

# Creating a screen
width = 700
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("CRAZY UNICORN GAME")

# Basic settings
distance = 5
fps = 60  # Frame per second
clock = pygame.time.Clock()
score = 0

# Definition of colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (173, 216, 230)
pink = (255, 204, 255)
hot_pink = (255, 105, 180)

# Font settings
unicorn_font = pygame.font.Font("font/unifont.ttf", 30)
# Text
unicorn_text = unicorn_font.render(" Crazy Unicorn Game ", True, hot_pink)
unicorn_text_rect = unicorn_text.get_rect()
unicorn_text_rect.midtop = (width//2, 10)
# Score text
score_text = unicorn_font.render(f"Score: {score}", True, hot_pink)
score_text_rect = score_text.get_rect()
score_text_rect.x = 10
score_text_rect.y = 10


media_dir = "media/"
# Background music settings
pygame.mixer.music.load(media_dir + "background.wav")
# Play background music
pygame.mixer.music.play(-1, 0.0)

# Upload sounds
sound_pick = pygame.mixer.Sound(media_dir + "pick.wav")
sound_pick.set_volume(1.5)

# Pictures
unicorn_image = pygame.image.load("img/crazy.png")
unicorn_image_rect = unicorn_image.get_rect()
unicorn_image_rect.center = (width//2, height//2)

kid_image = pygame.image.load("img/kid.png")
kid_image_rect = kid_image.get_rect()
kid_image_rect.center = (100, height//2)

# The main game cycle
lets_continue = True

while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

    # w - UP, s - DOWN, a - left, d - right
    # Character movement
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and unicorn_image_rect.top > 60:
        unicorn_image_rect.y -= distance
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and unicorn_image_rect.bottom < height:
        unicorn_image_rect.y += distance
    elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and unicorn_image_rect.left > 0:
        unicorn_image_rect.x -= distance
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and unicorn_image_rect.right < width:
        unicorn_image_rect.x += distance

    # Collision check
    if unicorn_image_rect.colliderect(kid_image_rect):
        kid_image_rect.centerx = random.randint(0 + 32, width - 32)
        kid_image_rect.centery = random.randint(50 + 32, height - 32)
        score += 1
        sound_pick.play()

    # Background image
    background_image = pygame.image.load("img/BG.jpg")
    screen.blit(background_image, (0, 0))

    # Shape
    pygame.draw.line(screen, hot_pink, (0, 50), (width, 50), 2)

    # Texts
    screen.blit(unicorn_text, unicorn_text_rect)
    screen.blit(score_text, score_text_rect)
    score_text = unicorn_font.render(f"Score: {score}", True, hot_pink)
    score_text_rect = score_text.get_rect()
    score_text_rect.x = 10
    score_text_rect.y = 10

    # Adding a picture
    screen.blit(unicorn_image, unicorn_image_rect)
    screen.blit(kid_image, kid_image_rect)

    # Text
    screen.blit(unicorn_text, unicorn_text_rect)
    screen.blit(score_text, score_text_rect)

    # Update screens
    pygame.display.update()

    # The clock is ticking
    clock.tick(fps)

# Ending the pygame
pygame.quit()
