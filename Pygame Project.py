# PygameProject.py

import pygame
import random
pygame.font.init()

# Global constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WIDTH = 800
HEIGHT = 600
FONT = pygame.font.SysFont("Comic Sans", 50)
HEART = pygame.transform.scale(pygame.image.load("./assets/heart.png"), (35, 35))

class Player(pygame.sprite.Sprite):
    """" This class represents the sprite that the player controls. """

    def __init__(self):
        super().__init__()

        # Set the image of the sprite and scale it
        self.image = pygame.image.load("./assets/kirby.png")
        self.image = pygame.transform.scale(self.image, (40, 40))

        # Make a hitbox
        self.rect = self.image.get_rect()

        # Set the speed vector of player
        self.change_x = 0
        self.change_y = 0

        # Set the starting point
        self.rect.x = (WIDTH/2)
        self.rect.y = (HEIGHT/2)

    def update(self):
        """" Moves the player (arrow keys). """

        # Move the player according to its speed/vectors
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.x < 0:
            self.rect.x = WIDTH
        if self.rect.x > WIDTH:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = HEIGHT
        if self.rect.y > HEIGHT:
            self.rect.y = 0

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def go_up(self):
        """ Called when the user hits the up arrow. """
        self.change_y = -6

    def go_down(self):
        """ Called when the user hits the down arrow. """
        self.change_y = 6

    def stop_horizontal(self):
        """ Called when the user lets go of the left or right. """
        self.change_x = 0

    def stop_vertical(self):
        """ Called when the user lets go of up or down. """
        self.change_y = 0

class Bullet(pygame.sprite.Sprite):
    """" This class represents the bullets that will be launched at the player"""

    def __init__(self):
        super().__init__()

        # Set the image of the sprite and scale it
        self.image = pygame.image.load("./assets/bullet.png")
        self.image = pygame.transform.scale(self.image, (21, 21))

        # Make a hitbox
        self.rect = self.image.get_rect()

        # Set the speed vector of bullet
        self.change_x = random.randrange(-4, 4)
        self.change_y = random.randrange(-4, 4)

        if self.change_x == 0:
            self.change_x += 1
        elif self.change_y == 0:
            self.change_y += 1

        # Set the start point
        if self.change_x > 0:
            self.rect.x = random.randrange(0, 50)
        else:
            self.rect.x = random.randrange(WIDTH - 50, WIDTH)

        if self.change_y > 0:
            self.rect.y = random.randrange(0, 50)
        else:
            self.rect.y = random.randrange(HEIGHT - 50, HEIGHT)


    def update(self):
        """" Moves the bullet """

        # Move the bullet according to its speed/vectors
        self.rect.x += self.change_x
        self.rect.y += self.change_y

def main():
    """ Main Program. """
    pygame.init()

    # ----- SCREEN PROPERTIES -----
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Dodgeball")

    # ----- LOCAL VARIABLES -----
    done = False
    clock = pygame.time.Clock()
    num_bullets = 15
    lives = 3
    score = 0

    # Create sprite groups and fill them
    all_sprites_group = pygame.sprite.Group()
    bullet_sprites_group = pygame.sprite.Group()
    player = Player()
    all_sprites_group.add(player)

    for i in range(num_bullets):
        bullet = Bullet()
        all_sprites_group.add(bullet)
        bullet_sprites_group.add(bullet)

    # ----- MAIN LOOP -----
    while not done:

        # -- Event Handler -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Make the player move around depending on the arrow keys pressed down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.go_up()
                if event.key == pygame.K_DOWN:
                    player.go_down()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop_horizontal()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop_horizontal()
                if event.key == pygame.K_UP and player.change_y < 0:
                    player.stop_vertical()
                if event.key == pygame.K_DOWN and player.change_y > 0:
                    player.stop_vertical()


        # ----- LOGIC -----
        all_sprites_group.update()

        # Collide the player with any bullets
        collisions = pygame.sprite.spritecollide(player, bullet_sprites_group, dokill=True)

        # take away a life for every collision and lower the current number of bullets
        for collision in collisions:
            num_bullets -= 1
            lives -= 1

        # If a bullet goes out of bounds, delete it and lower the current number of bullets
        for bullet in bullet_sprites_group:
            if bullet.rect.x < 0 or bullet.rect.x > WIDTH:
                bullet.kill()
                num_bullets -= 1

            if bullet.rect.y < 0 or bullet.rect.y > HEIGHT:
                bullet.kill()
                num_bullets -= 1

        # Make sure there are always ten bullets
        if num_bullets < 15:

            # Replace the bullet
            bullet = Bullet()
            all_sprites_group.add(bullet)
            bullet_sprites_group.add(bullet)
            num_bullets += 1

        # ----- RENDER -----
        screen.fill(BLACK)
        all_sprites_group.draw(screen)

        # If the player is still alive
        if lives > 0:
            # Add 1 to the score every tick
            score += 1

            # Display a timer at the bottom right as the score
            screen.blit(FONT.render(f'Score: {score}', True, GREEN), (20, HEIGHT - 80))

        # If the player has three lives
        if lives == 3:
            # Display three hearts
            screen.blit(HEART, (0, 0))
            screen.blit(HEART, (45, 0))
            screen.blit(HEART, (90, 0))

        # If the player has two lives
        if lives == 2:
            # Display two hearts
            screen.blit(HEART, (0, 0))
            screen.blit(HEART, (45, 0))

        # If the player has one life left
        if lives == 1:
            # Display one heart
            screen.blit(HEART, (0, 0))

        # If the player runs out of lives
        if lives <= 0:
            # Kill the player
            player.kill()

            # Display a Game Over Screen and the final score
            screen.blit(FONT.render('Game Over', True, GREEN), ((WIDTH/2) - 120, (HEIGHT/2) - 50))
            screen.blit(FONT.render(f'Score: {score}', True, GREEN), (20, HEIGHT - 80))

        # ----- UPDATE DISPLAY -----
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()




if __name__ == "__main__":
    main()