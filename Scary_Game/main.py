import pygame

from game import Game
from player import Player

def main():

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

    # Group of kids
    kids_group = pygame.sprite.Group()

    # Group of player
    player_group = pygame.sprite.Group()
    one_player = Player(width, height)
    player_group.add(one_player)

    # Object Game
    my_game = Game(one_player, kids_group, screen, fps)
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

if __name__ == "__main__":
    main()
