import pygame
import random

# Initializing pygame
pygame.init()

# Creating a screen
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("WHITE-EYED KIDS - SCARY GAME")

# Basic settings
fps = 60  # Frame per second
clock = pygame.time.Clock()


# Classes
class Kids(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/grim_reaper.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = random.randint(1, 6)

    def update(self):
        self.rect.y += self.speed


class Player(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, x, y, group_of_kids):
        super().__init__()
        self.image = pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/unicorn.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.group_of_kids = group_of_kids

        self.speed = 8

    def update(self):
        self.move()
        self.collison_checker()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def collison_checker(self):
        if pygame.sprite.spritecollide(self, self.group_of_kids, True):
            print("Collison")


# Creating a group of kids
kids_group = pygame.sprite.Group()
for i in range(10):
    one_kid = Kids(i * 70, 50)
    kids_group.add(one_kid)

# Creating a group of players
player_group = pygame.sprite.Group()
one_player = Player(width//2, 520, kids_group)
player_group.add(one_player)


# The main game cycle
lets_continue = True

while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False


    # Fill the screen with the background
    screen.fill((0, 0, 0))


    # Updating group of kids
    kids_group.update()
    kids_group.draw(screen)
    # Updating group of players
    player_group.update()
    player_group.draw(screen)


    # Update screens
    pygame.display.update()


    # The clock is ticking
    clock.tick(fps)


# Ending the pygame
pygame.quit()
