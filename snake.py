import random
import sys
import time

import pygame

from objects import TextObject, Snake, Apple, Bonus


def game_over(surface):
    """

    Displays a message about the end of the game.

    Args:
        surface(pygame.Surface): surface where we will draw 'game over'

    Returns:

    """
    my_font = pygame.font.SysFont('monaco', 108)
    go_surf = my_font.render("Game Over", True, (255, 0, 0))
    position = (400, 25)
    surface.blit(go_surf, position)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit()


class Game:
    """Main class.

    Attributes:
        score(int): score that user has
        text(str): string for drawing score
        width(int), height(int): size of surface
        side_of_square(int):
        objects(dict): objects that draw on the surface
        surface(pygame.Surface): surface
        frame_rate(int): speed of the game
        game_over(bool): status of the game
        time(time): value for checking when we must give a new bonus
        clock: parameter for frame rate

    """

    def __init__(self, caption, width, height, frame_rate):
        """

        Args:
            caption(str): name of the game
            width(int): width of surface
            height(int): height of surface
            frame_rate(int): speed of the game
        """
        pygame.init()
        self.score = 0
        self.text = TextObject(0, 0, (0, 0, 0), 'Score: {}'.format(self.score), 'monaco', 36)
        self.width = width
        self.height = height
        self.side_of_square = 15
        self.default_length = 3
        body_snake = [
            ((width // 100) * self.side_of_square - self.side_of_square * i, (height // 200) * self.side_of_square)
            for i in range(self.default_length)]
        self.objects = {'Snake': Snake(body_snake, self.side_of_square, 'RIGHT', (0, 255, 0)),
                        'Apple': Apple(random.randrange(0, width // self.side_of_square) * self.side_of_square,
                                       random.randrange(0, height // self.side_of_square) * self.side_of_square,
                                       self.side_of_square, (255, 0, 0), self.width, self.height)}
        self.surface = pygame.display.set_mode((width, height))
        self.frame_rate = frame_rate
        self.game_over = False
        pygame.display.set_caption(caption)
        self.time = time.time()
        self.bonus_apple = False
        self.clock = pygame.time.Clock()

    def check_problems(self):
        """Check snake coordinates.

        Returns:
            bool: True if all right, else False

        """
        if not self.crash_into_wall():
            return False
        if not self.crash_himself():
            return False
        return True

    def crash_into_wall(self):
        """

        Check that snake did not crash into wall.

        Returns:
            bool: True if all right, False if snake crashed into wall

        """
        if self.objects['Snake'].head[0] < 0 or self.objects['Snake'].head[0] > self.width or \
                self.objects['Snake'].head[1] < 0 or self.objects['Snake'].head[1] > self.height:
            return False
        return True

    def crash_himself(self):
        """

        Check that snake did not crash himself.

        Returns:
            bool: True if all right, False if snake crashed himself

        """
        for body_square in self.objects['Snake'].body[1:]:
            if self.objects['Snake'].head == (body_square.x_coordinate, body_square.y_coordinate):
                return False
        return True

    def handle_events(self):
        """

        Read user clicks and send command to the snake.

        Returns:
            nothing

        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.objects['Snake'].new_direction('RIGHT')
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.objects['Snake'].new_direction('LEFT')
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.objects['Snake'].new_direction('UP')
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.objects['Snake'].new_direction('DOWN')
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        """

        Update the state of the game. Check problems and check that snake eat apple or bonus

        Returns:
            nothing

        """
        flag = True
        if self.bonus_apple:
            if self.objects['Snake'].head == (self.objects['Bonus'].x_coordinate, self.objects['Bonus'].y_coordinate):
                self.score += 3
                self.text.get_update('Score: {}'.format(self.score))
                self.objects['Snake'].update()
                self.objects.pop('Bonus')
                flag = True
                self.bonus_apple = False
            elif time.time() - self.objects['Bonus'].time > self.objects['Bonus'].max_time:
                self.objects.pop('Bonus')
                self.time = time.time()
                self.bonus_apple = False
        if self.objects['Snake'].head == (self.objects['Apple'].x_coordinate, self.objects['Apple'].y_coordinate):
            self.score += 1
            self.text.get_update('Score: {}'.format(self.score))
            self.frame_rate += 0.5
            self.objects['Snake'].update()
            self.objects['Apple'].update()
        elif flag:
            self.objects['Snake'].update()
            self.objects['Snake'].delete_tail()

    def draw(self):
        """

        Draw all objects of the game.

        Returns:
            nothing

        """
        for elem in self.objects:
            self.objects[elem].draw(self.surface)
        self.text.draw(self.surface)

    def get_bonus_apple(self):
        """

        Create bonus and add in objects of the game.

        Returns:
            nothing

        """
        if time.time() - self.time > 25:
            self.time = time.time()
            self.bonus_apple = True
            self.objects['Bonus'] = Bonus(random.randrange(0, self.width // self.side_of_square) * self.side_of_square,
                                          random.randrange(0, self.height // self.side_of_square) * self.side_of_square,
                                          self.side_of_square, (255, 255, 0), self.width, self.height)

    def run(self):
        """

        Start the game.

        Returns:
            nothing

        """
        while not self.game_over:
            self.surface.fill((244, 164, 96))

            if not self.check_problems():
                game_over(self.surface)
                break

            self.handle_events()
            self.get_bonus_apple()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
