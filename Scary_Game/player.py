"""Player class"""
import pygame


class Player(pygame.sprite.Sprite):
    """Player class"""
    def __init__(self, width, height):
        super().__init__() # Constructor inherits from Sprite
        # Upload a picture of the kid and its location
        self.image = pygame.image.load("img/unicorn.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2    # On the x-axis, the centre point of game screen
        self.rect.bottom = height       # Bottom edge of the game screen

        self.lives = 5
        self.enter_safe_zone = 3
        self.speed = 8

        self.catch_sound = pygame.mixer.Sound("media/scream.wav")
        self.catch_sound.set_volume(0.3)
        self.wrong_sound = pygame.mixer.Sound("media/fail.wav")
        self.wrong_sound.set_volume(0.2)

        self.width = width
        self.height = height

    def update(self):
        """ Code called over and over again """
        # w - UP, s - DOWN, a - left, d - right
        # Character movement
        keys = pygame.key.get_pressed()     # Pressing the key - save to a variable keys

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:    # Key settings - boundaries for movement
            self.rect.x -= self.speed

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < self.width:
            self.rect.x += self.speed

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
            self.rect.y -= self.speed

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < self.height - 100:
            self.rect.y += self.speed

    def back_to_safe_zone(self):
        """ Return to the safe zone at the bottom of the game screen """
        if self.enter_safe_zone > 0:
            self.enter_safe_zone -= 1
            self.rect.bottom = self.height

    def reset_game(self):
        """ Returns the player to the starting position - the middle of the safe zone """
        self.rect.centerx = self.width//2
        self.rect.bottom = self.height
