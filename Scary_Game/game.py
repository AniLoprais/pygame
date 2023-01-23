"""Game class"""
import pygame
import random
from kid import Kid

class Game:
    """Main class of the game"""
    def __init__(self, our_player, group_of_kids, screen, fps):
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.slow_down_cycle = 0

        self.our_player = our_player
        self.group_of_kids= group_of_kids

        self.width = screen.get_width()
        self.height = screen.get_height()
        self.fps = fps
        self.screen = screen

        # Background music
        pygame.mixer.music.load("media/music.wav") # The path to music
        pygame.mixer.music.play(-1, 0.0)    # The music will play endlessly from the zero second
        pygame.mixer.music.set_volume(0.30)

        # Fonts
        self.scarry_font = pygame.font.Font("font/font.ttf", 28)
        self.scarry_font_bigger = pygame.font.Font("font/font.ttf", 55)

        # Background image
        self.background_image = pygame.image.load("img/dark_forest.jpg")
        self.background_image_rect = self.background_image.get_rect()
        self.background_image_rect.topleft = (0, 0)

        # Images
        zombie_image = pygame.image.load("img/zombie.png")
        grim_reaper_image = pygame.image.load("img/grim_reaper.png")
        witch_image = pygame.image.load("img/witch.png")
        shaman_image = pygame.image.load("img/shaman.png")
        # Types of kids: 0 = zombie, 1 = grim_reaper, 2 = witch, 3 = shaman
        self.kids_images = [zombie_image, grim_reaper_image, witch_image, shaman_image]

        # Generating a kid to be caught
        self.kid_catch_type = random.randint(0, 3)
        self.kid_catch_image = self.kids_images[self.kid_catch_type]    # Random selection of all the kid's picture

        self.kid_catch_image_rect = self.kid_catch_image.get_rect()     # objects to store and manipulate rectangular areas
        self.kid_catch_image_rect.centerx = self.width//2
        self.kid_catch_image_rect.top = 35


    def update(self):
        """ Code called over and over again """
        self.slow_down_cycle += 1
        if self.slow_down_cycle == self.fps:
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
        catch_text_rect.centerx = self.width//2
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
        time_text_rect.topright = (self.width - 20, 5)

        # Count - how many times the unicorn can return to the safe zone
        back_safe_zone_text = self.scarry_font.render(f"SAFE ZONE: {self.our_player.enter_safe_zone}", True, red)
        back_safe_zone_text_rect = back_safe_zone_text.get_rect()
        back_safe_zone_text_rect.topright = (self.width - 20, 35)

        # self.screen rendering (Bliting)
        self.screen.blit(catch_text ,catch_text_rect)
        self.screen.blit(score_text ,score_text_rect)
        self.screen.blit(lives_text, lives_text_rect)
        self.screen.blit(round_text, round_text_rect)
        self.screen.blit(time_text, time_text_rect)
        self.screen.blit(back_safe_zone_text, back_safe_zone_text_rect)
        # Image of hunting kid
        self.screen.blit(self.kid_catch_image, self.kid_catch_image_rect)

        # Shape
        # The frame game self.screen - where kids can move around
        pygame.draw.rect(self.screen, colors[self.kid_catch_type], (0, 100, self.width, self.height - 200), 4)


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
                    # self.reset_game()
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
            for j in range(4):
                self.group_of_kids.add(
                    Kid(
                        random.randint(0, self.width - 64),
                        random.randint(100, self.height - 164),
                        self.width,
                        self.height,
                        self.kids_images[j],
                        j
                    )
                )

            self.choose_new_target()

    def choose_new_target(self):
        """ Chooses a new kid to catch """
        new_kid_to_catch = random.choice(self.group_of_kids.sprites())
        self.kid_catch_type = new_kid_to_catch.type
        self.kid_catch_image = new_kid_to_catch.image

    def pause_game(self, main_text, sub_heading):
        """ Game pause - pause before starting a new game, at the beginning when starting """

        # Color settings
        red = (225, 6, 0)
        black = (0, 0, 0)

        # Main text for pause
        main_text_create = self.scarry_font_bigger.render(main_text, True, red)
        main_text_create_rect = main_text_create.get_rect()
        main_text_create_rect.center = (self.width//2, self.height//2 - 35)

        # Subheading for pause
        sub_heading_create = self.scarry_font_bigger.render(sub_heading, True, red)
        sub_heading_create_rect = sub_heading_create.get_rect()
        sub_heading_create_rect.center = (self.width//2, self.height//2 + 45)

        # Display main text and subheading text
        self.screen.fill(black)
        self.screen.blit(main_text_create, main_text_create_rect)
        self.screen.blit(sub_heading_create, sub_heading_create_rect)
        pygame.display.update()

        # Stopping the game
        paused = True
        while paused:
            for one_event in pygame.event.get():
                if one_event.type == pygame.KEYDOWN:
                    if one_event.key == pygame.K_RETURN:
                        paused = False
                if one_event.type == pygame.QUIT:
                    pygame.quit()

    def reset_game(self):
        """ Reset the game to its default state """
        self.score = 0
        self.round_number = 0

        self.our_player.lives = 5
        self.our_player.enter_safe_zone = 3
        self.start_new_round()

        # # Starting music from the beginning
        # pygame.mixer.music.play(-1, 0.0)
