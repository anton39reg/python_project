import random
import sys
import time

import pygame
from pygame.rect import Rect


class GameObject:
    """This is a basic class.

    Attributes:
        x(int), y(int): object coordinates
        w(int), h(int): size of object
        bounds(RectType): object
        color(tuple is long 3): object color

    """
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bounds = Rect(x, y, w, h)
        self.color = (0, 0, 0)

    def draw(self, surface):
        """Draw object on transmitted surface

        Args:
            surface(pygame.Surface): surface where we will draw object

        Returns:
            nothing

        """
        pygame.draw.rect(surface, self.color, self.bounds)


class Square(GameObject):
    """This is special square for drawing of snake.

    """
    def __init__(self, x, y, side_of_square, color):
        GameObject.__init__(self, x, y, side_of_square, side_of_square)
        self.color = color


class Apple(GameObject):
    """

    Attributes:
        w(int), h(int): size of surface for correct choose coordinates for drawing apple.
        side_of_square(int):

    """
    def __init__(self, x, y, side_of_square, color, width_of_field, height_of_field):
        GameObject.__init__(self, x, y, side_of_square, side_of_square)
        self.color = color
        self.side_of_square = side_of_square
        self.w = width_of_field
        self.h = height_of_field

    def update(self):
        """Update coordinates.

        When snake eat an apple we choose new coordinates.

        Returns:
            nothing

        """
        self.x = random.randrange(0, self.w//self.side_of_square)*self.side_of_square
        self.y = random.randrange(0, self.h//self.side_of_square)*self.side_of_square
        self.bounds = Rect(self.x, self.y, self.side_of_square, self.side_of_square)


class Bonus(Apple):
    """

    Like an apple but bonus disappears after max_time seconds.

    Attributes:
        time(time): time when bonus born
        max_time(int): max time of life

    """
    def __init__(self, x, y, side_of_square, color, width_of_field, height_of_field):
        Apple.__init__(self, x, y, side_of_square, color, width_of_field, height_of_field)
        self.time = time.time()
        self.max_time = 5


class Snake:
    """

    Snake consists of Squares.

    Attributes:
        head(tuple): head coordinates
        body(list with tuple): body coordinates
        side_of_square(int):
        direction(str): snake move this direction
        color(tuple is long 3): color of snake

    """
    def __init__(self, list_of_pos, side_of_square, direction, color):
        self.head = list_of_pos[0]
        self.body = []
        self.side_of_square = side_of_square
        self.color = color
        for i in list_of_pos:
            self.body.append(Square(i[0], i[1], side_of_square, self.color))
        self.direction = direction

    def draw(self, surface):
        """

        Draw all squares on surface.

        Args:
            surface(pygame.Surface): surface where we will draw snake

        Returns:
            nothing

        """
        for i in self.body:
            i.draw(surface)

    def update(self):
        """

        Add new head coordinates in the right place that depends on the direction

        Returns:
            nothing

        """
        if self.direction == 'RIGHT':
            self.head = self.head[0] + self.side_of_square, self.head[1]
        elif self.direction == 'LEFT':
            self.head = self.head[0] - self.side_of_square, self.head[1]
        elif self.direction == 'UP':
            self.head = self.head[0], self.head[1] - self.side_of_square
        elif self.direction == 'DOWN':
            self.head = self.head[0], self.head[1] + self.side_of_square
        self.body.insert(0, Square(self.head[0], self.head[1], self.side_of_square, self.color))

    def delete_tail(self):
        """

        Delete last element of body if snake did not eat an apple.

        Returns:
            nothing

        """
        self.body.pop()

    def new_direction(self, command):
        """

        Choose new direction that user wants if new direction is correct for snake.

        Args:
            command(str): new direction that user wants

        Returns:
            nothing

        """
        if command == 'LEFT' and self.direction != 'RIGHT':
            self.direction = command
        if command == 'RIGHT' and self.direction != 'LEFT':
            self.direction = command
        if command == 'UP' and self.direction != 'DOWN':
            self.direction = command
        if command == 'DOWN' and self.direction != 'UP':
            self.direction = command


class TextObject:
    """

    Attributes:
        x(int), y(int): coordinates
        color(tuple is long 3): color of text
        font_name(str): font of text
        font_size(int): size of font

    """
    def __init__(self, x, y, color, text, font_name, font_size):
        self.pos = (x, y)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)

    def get_surface(self, text):
        """

        Args:
            text(str): text that we draw

        Returns:
            render of text

        """
        text_surface = self.font.render(text, False, self.color)
        return text_surface

    def draw(self, surface):
        """Draw text on surface.

        Args:
            surface(pygame.Surface): surface where we will draw text

        Returns:
            nothing

        """
        text_surface = self.get_surface(self.text)
        pos = self.pos
        surface.blit(text_surface, pos)

    def get_update(self, text):
        """Update text.

        Args:
            text(str): new text

        Returns:
            nothing

        """
        self.text = text


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
        pygame.init()
        self.score = 0
        self.text = TextObject(0, 0, (0, 0, 0), 'Score: {}'.format(self.score), 'monaco', 36)
        self.width = width
        self.height = height
        self.side_of_square = 15
        body_snake = [((width//100)*self.side_of_square - self.side_of_square * i, (height//200)*self.side_of_square)
                      for i in range(3)]
        self.objects = {'Snake': Snake(body_snake, self.side_of_square, 'RIGHT', (0, 255, 0)),
                        'Apple': Apple(random.randrange(0, width//self.side_of_square)*self.side_of_square,
                                       random.randrange(0, height//self.side_of_square)*self.side_of_square,
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
        if self.objects['Snake'].head[0] < 0 or self.objects['Snake'].head[0] > self.width or\
           self.objects['Snake'].head[1] < 0 or self.objects['Snake'].head[1] > self.height:
            return False
        return True

    def crash_himself(self):
        """

        Check that snake did not crash himself.

        Returns:
            bool: True if all right, False if snake crashed himself

        """
        for i in self.objects['Snake'].body[1:]:
            if self.objects['Snake'].head == (i.x, i.y):
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
            if self.objects['Snake'].head == (self.objects['Bonus'].x, self.objects['Bonus'].y):
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
        if self.objects['Snake'].head == (self.objects['Apple'].x, self.objects['Apple'].y):
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
                                          random.randrange(0, self.height//self.side_of_square) * self.side_of_square,
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


if __name__ == "__main__":
    a = Game('snake', 1280, 640, 10)
    a.run()
