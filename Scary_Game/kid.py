"""Player class"""
import pygame
import random

class Kid(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, kids_type):
        super().__init__()
        # Upload a picture of the kid and his location
        self.image = image  # Image via a image attribute - more different kids
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.width = width
        self.height = height

        # Types of kids: 0 = zombie, 1 = grim_reaper, 2 = witch, 3 = shaman
        self.type = kids_type

        # Setting random direction of kids
        self.x = random.choice([-1, 1])     # Random direction along the x-axis
        self.y = random.choice([-1, 1])     # Random direction along the y-axis
        self.speed = random.randint(1, 5)   # Random speed of kids

    def update(self):
        """ Code called over and over again """
        # Movement of the kids
        self.rect.x += self.x * self.speed  # Increase in direction and speed
        self.rect.y += self.y * self.speed

        # Kids bounce
        if self.rect.left < 0 or self.rect.right > self.width:   # Boundary of sides along the x-axis
            self.x = -1 * self.x                            # Turning the kids
        if self.rect.top < 100 or self.rect.bottom > self.height - 100:
            self.y = -1 * self.y
