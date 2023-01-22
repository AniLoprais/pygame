import pygame
import random

# Initializing pygame
pygame.init()

# Creating a screen
width = 1200
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BLOODY UNICORN - HUNTING KIDS")

# Basic settings
fps = 60  # Frame per second
clock = pygame.time.Clock()


# Classes
class Game:
    def __init__(self, our_player, group_of_kids):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.slow_down_cycle = 0

        self.our_player = our_player
        self.group_of_kids= group_of_kids

        # Background music
        pygame.mixer.music.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/media/music.wav") # The path to music
        pygame.mixer.music.play(-1, 0.0)    # The music will play endlessly from the zero second
        pygame.mixer.music.set_volume(0.30)

        # Fonts
        self.scarry_font = pygame.font.Font("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/font/font.ttf", 28)
        self.scarry_font_bigger = pygame.font.Font("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/font/font.ttf", 55)

        # Background image
        self.background_image = pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/dark_forest.jpg")
        self.background_image_rect = self.background_image.get_rect()
        self.background_image_rect.topleft = (0, 0)

        # Images
        zombie_image = pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/zombie.png")
        grim_reaper_image = pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/grim_reaper.png")
        witch_image = pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/witch.png")
        shaman_image = pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/shaman.png")
        # Types of kids: 0 = zombie, 1 = grim_reaper, 2 = witch, 3 = shaman
        self.kids_images = [zombie_image, grim_reaper_image, witch_image, shaman_image]

        # Generating a kid to be caught
        self.kid_catch_type = random.randint(0, 3)
        self.kid_catch_image = self.kids_images[self.kid_catch_type]    # Random selection of all the kid's picture

        self.kid_catch_image_rect = self.kid_catch_image.get_rect()     # objects to store and manipulate rectangular areas
        self.kid_catch_image_rect.centerx = width//2
        self.kid_catch_image_rect.top = 35


    def update(self):
        """ Code called over and over again """
        self.slow_down_cycle += 1
        if self.slow_down_cycle == fps:
            self.round_time += 1    # Raising the time
            self.slow_down_cycle = 0


        # Check collision
        self.check_collision()


    def draw(self):
        """ Drawing everything in the game - texts, frame scree, blitting, collision """
        red = (225, 6, 0)
        green = pygame.Color("#4ADEDE")
        gray = pygame.Color("#999DA0")
        purple = pygame.Color("#9400D3")
        orange = pygame.Color("#ff7400")
        # Types of kids: 0 = zombie, 1 = grim_reaper, 2 = witch, 3 = shaman
        colors = [green, gray, purple, orange]

        # Settings texts
        catch_text = self.scarry_font.render("KILL THIS KID", True, red)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.centerx = width//2
        catch_text_rect.top = 5

        score_text = self.scarry_font.render(f"SCORE: {self.score}", True, red)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (20, 4)

        lives_text = self.scarry_font.render(f"LIVES: {self.our_player.lives}", True, red)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (20, 32)

        round_text = self.scarry_font.render(f"ROUND: {self.round_number}", True, red)
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (20, 60)

        time_text = self.scarry_font.render(f"ROUND TIME: {self.round_time}", True, red)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (width - 20, 5)

        # Count - how many times the unicorn can return to the safe zone
        back_safe_zone_text = self.scarry_font.render(f"SAFE ZONE: {self.our_player.enter_safe_zone}", True, red)
        back_safe_zone_text_rect = back_safe_zone_text.get_rect()
        back_safe_zone_text_rect.topright = (width - 20, 35)

        # Screen rendering (Bliting)
        screen.blit(catch_text ,catch_text_rect)
        screen.blit(score_text ,score_text_rect)
        screen.blit(lives_text, lives_text_rect)
        screen.blit(round_text, round_text_rect)
        screen.blit(time_text, time_text_rect)
        screen.blit(back_safe_zone_text, back_safe_zone_text_rect)
        # Image of hunting kid
        screen.blit(self.kid_catch_image, self.kid_catch_image_rect)

        # Shape
        # The frame game screen - where kids can move around
        pygame.draw.rect(screen, colors[self.kid_catch_type], (0, 100, width, height - 200), 4)


    def check_collision(self):
        """ Checks the collision of a unicorn with a kids """
        # What kid did the player collide with
        collided_kid = pygame.sprite.spritecollideany(self.our_player, self.group_of_kids)

        if collided_kid:
            # Did we collide with the right kid?
            if collided_kid.type == self.kid_catch_type:
                self.our_player.catch_sound.play()      # Play the sound of the right kid being killed
                self.score += 10 * self.round_number    # Score increase
                collided_kid.remove(self.group_of_kids) # Removal of the killed kid
                # Check - if there's any kids left to kill.
                if self.group_of_kids:
                    self.choose_new_target()
                else:
                    # The round is complete, we have killed all the kids
                    self.our_player.reset_game() # The player appears on the starting position
                    self.start_new_round()  # Starting a new round
            else:
                self.our_player.wrong_sound.play()
                self.our_player.lives -= 1
                # Check - the number of lives
                if self.our_player.lives <= 0:
                    self.pause_game(f"FINAL SCORE: {self.score}", "IF YOU WANT TO PLAY AGAIN PRESS ENTER")
                    self.reset_game()
                self.our_player.reset_game()



    def start_new_round(self):
        """ Start a new round - with more kids on the playing surface """
        # The player gets a bonus, according to the speed of the round completed
        self.score += int(100 * (self.round_number / (1 + self.round_time)))

        # Reset values
        self.round_time = 0
        self.slow_down_cycle = 0
        self.round_number += 1
        self.our_player.enter_safe_zone += 1

        # Clean up a group of kids so that the group can be filled with a new number of kids
        for deleted_kid in self.group_of_kids:
            self.group_of_kids.remove(deleted_kid)

        for i in range(self.round_number):
            # Creating the first kid
            self.group_of_kids.add(
            Kids(random.randint(0, width - 64),
            random.randint(100, height - 164),
            self.kids_images[0], 0)
            )

            self.group_of_kids.add(
            Kids(random.randint(0, width - 64),
            random.randint(100, height - 164),
            self.kids_images[1], 1)
            )

            self.group_of_kids.add(
            Kids(random.randint(0, width - 64),
            random.randint(100, height - 164),
            self.kids_images[2], 2)
            )

            self.group_of_kids.add(
            Kids(random.randint(0, width - 64),
            random.randint(100, height - 164),
            self.kids_images[3], 3)
            )

            self.choose_new_target()

    def choose_new_target(self):
        """ Chooses a new kid to catch """
        new_kid_to_catch = random.choice(self.group_of_kids.sprites())
        self.kid_catch_type = new_kid_to_catch.type
        self.kid_catch_image = new_kid_to_catch.image

    def pause_game(self, main_text, sub_heading):
        """ Game pause - pause before starting a new game, at the beginning when starting """

        global lets_continue

        # Color settings
        red = (225, 6, 0)
        black = (0, 0, 0)

        # Main text for pause
        main_text_create = self.scarry_font_bigger.render(main_text, True, red)
        main_text_create_rect = main_text_create.get_rect()
        main_text_create_rect.center = (width//2, height//2 - 35)

        # Subheading for pause
        sub_heading_create = self.scarry_font_bigger.render(sub_heading, True, red)
        sub_heading_create_rect = sub_heading_create.get_rect()
        sub_heading_create_rect.center = (width//2, height//2 + 45)

        # Display main text and subheading text
        screen.fill(black)
        screen.blit(main_text_create, main_text_create_rect)
        screen.blit(sub_heading_create, sub_heading_create_rect)
        pygame.display.update()

        # Stopping the game
        paused = True
        while paused:
            for one_event in pygame.event.get():
                if one_event.type == pygame.KEYDOWN:
                    if one_event.key == pygame.K_RETURN:
                        paused = False
                if one_event.type == pygame.QUIT:
                    paused = False
                    lets_continue = False

    def reset_game(self):
        """ Reset the game to its default state """
        self.score = 0
        self.round_number = 0

        self.our_player.lives = 5
        self.our_player.enter_safe_zone = 3
        self.start_new_round()

        # # Starting music from the beginning
        # pygame.mixer.music.play(-1, 0.0)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Constructor inherits from Sprite
        # Upload a picture of the kid and its location
        self.image = pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/unicorn.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = width//2    # On the x-axis, the centre point of game screen
        self.rect.bottom = height       # Bottom edge of the game screen

        self.lives = 5
        self.enter_safe_zone = 3
        self.speed = 8

        self.catch_sound = pygame.mixer.Sound("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/media/scream.wav")
        self.catch_sound.set_volume(0.3)
        self.wrong_sound = pygame.mixer.Sound("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/media/fail.wav")
        self.wrong_sound.set_volume(0.2)

    def update(self):
        """ Code called over and over again """
        # w - UP, s - DOWN, a - left, d - right
        # Character movement
        keys = pygame.key.get_pressed()     # Pressing the key - save to a variable keys

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:    # Key settings - boundaries for movement
            self.rect.x -= self.speed

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < width:
            self.rect.x += self.speed

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
            self.rect.y -= self.speed

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < height - 100:
            self.rect.y += self.speed

    def back_to_safe_zone(self):
        """ Return to the safe zone at the bottom of the game screen """
        if self.enter_safe_zone > 0:
            self.enter_safe_zone -= 1
            self.rect.bottom = height

    def reset_game(self):
        """ Returns the player to the starting position - the middle of the safe zone """
        self.rect.centerx = width//2
        self.rect.bottom = height


class Kids(pygame.sprite.Sprite):
    def __init__(self, x, y, image, kids_type):
        super().__init__()
        # Upload a picture of the kid and his location
        self.image = image  # Image via a image attribute - more different kids
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

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
        if self.rect.left < 0 or self.rect.right > width:   # Boundary of sides along the x-axis
            self.x = -1 * self.x                            # Turning the kids
        if self.rect.top < 100 or self.rect.bottom > height - 100:
            self.y = -1 * self.y

# Group of kids
kids_group = pygame.sprite.Group()
# # Test kids
# # Types of kids: 0 = zombie, 1 = grim_reaper, 2 = witch, 3 = shaman
# one_kid = Kids(500, 500, pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/zombie.png"), 0)
# kids_group.add(one_kid)
# one_kid = Kids(500, 500, pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/grim_reaper.png"), 1)
# kids_group.add(one_kid)
# one_kid = Kids(500, 500, pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/witch.png"), 2)
# kids_group.add(one_kid)
# one_kid = Kids(500, 500, pygame.image.load("/Users/anicka/Desktop/pyladies/pygame/Scary_Game/img/shaman.png"), 3)
# kids_group.add(one_kid)

# Group of player
player_group = pygame.sprite.Group()
one_player = Player()
player_group.add(one_player)

# Object Game
my_game = Game(one_player, kids_group)
my_game.pause_game("BLOODY UNICORN - HUNTING KIDS", "PRESS ENTER TO START THE GAME")
my_game.start_new_round()

# The main game cycle
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # Stopping the cycle and ending the game
            lets_continue = False
        if event.type == pygame.KEYDOWN:    # If the space bar is pressed, return the player to the safe game
            if event.key == pygame.K_SPACE:
                one_player.back_to_safe_zone()


    # Fill the screen with the background
    # screen.fill((0, 0, 0))
    screen.blit(my_game.background_image, my_game.background_image_rect)

    # Updating group of kids
    kids_group.draw(screen)
    kids_group.update()
    # Updating group of players (one player)
    player_group.update()
    player_group.draw(screen)
    # Update the object create according to the class Game
    my_game.update()
    my_game.draw()

    # Update screens
    pygame.display.update()

    # Slowdown cycle
    clock.tick(fps)


# Ending the pygame
pygame.quit()
