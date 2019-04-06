import random
import time

import pygame
from pygame.rect import Rect


class GameObject:
    """This is a basic class.

    Attributes:
        x_coordinate(int), y_coordinate(int): object coordinates
        width(int), height(int): size of object
        bounds(RectType): object
        color(tuple is long 3): object color

    """
    def __init__(self, x_coordinate, y_coordinate, width, height):
        """

        Args:
            x_coordinate(int): x coordinate
            y_coordinate(int): y coordinate
            width(int): width of object
            height(int): height of object

        """
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width = width
        self.height = height
        self.bounds = Rect(x_coordinate, y_coordinate, width, height)
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
    def __init__(self, x_coordinate, y_coordinate, side_of_square, color):
        """

        Args:
            x_coordinate(int): x coordinate
            y_coordinate(int): y coordinate
            side_of_square(int): size of square
            color(tuple is a long 3): color of square

        """
        GameObject.__init__(self, x_coordinate, y_coordinate, side_of_square, side_of_square)
        self.color = color


class Apple(GameObject):
    """

    Attributes:
        w(int), h(int): size of surface for correct choose coordinates for drawing apple.
        side_of_square(int):

    """
    def __init__(self, x_coordinate, y_coordinate, side_of_square, color, width_of_field, height_of_field):
        """

        Args:
            x_coordinate(int): x coordinate
            y_coordinate(int): y coordinate
            side_of_square(int):
            color(tuple is a long 3):
            width_of_field(int):
            height_of_field(int):

        """
        GameObject.__init__(self, x_coordinate, y_coordinate, side_of_square, side_of_square)
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
        self.x_coordinate = random.randrange(0, self.w//self.side_of_square)*self.side_of_square
        self.y_coordinate = random.randrange(0, self.h//self.side_of_square)*self.side_of_square
        self.bounds = Rect(self.x_coordinate, self.y_coordinate, self.side_of_square, self.side_of_square)


class Bonus(Apple):
    """

    Like an apple but bonus disappears after max_time seconds.

    Attributes:
        time(time): time when bonus born
        max_time(int): max time of life

    """
    def __init__(self, x_coordinate, y_coordinate, side_of_square, color, width_of_field, height_of_field):
        """

        Args:
            x_coordinate(int): x coordinate
            y_coordinate(int): y coordinate
            side_of_square(int):
            color(tuple is a long 3):
            width_of_field(int):
            height_of_field(int):

        """
        Apple.__init__(self, x_coordinate, y_coordinate, side_of_square, color, width_of_field, height_of_field)
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
        """

        Args:
            list_of_pos(list with tuple): body coordinates
            side_of_square(int):
            direction(str):
            color(tuple is a long 3):
        """
        self.head = list_of_pos[0]
        self.body = []
        self.side_of_square = side_of_square
        self.color = color
        for pos in list_of_pos:
            self.body.append(Square(pos[0], pos[1], side_of_square, self.color))
        self.direction = direction

    def draw(self, surface):
        """

        Draw all squares on surface.

        Args:
            surface(pygame.Surface): surface where we will draw snake

        Returns:
            nothing

        """
        for body_square in self.body:
            body_square.draw(surface)

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
        font_size(int): size of text

    """
    def __init__(self, x, y, color, text, font_name, font_size):
        """

        Args:
            x(int): x coordinate
            y(int): y coordinate
            color(tuple is a long 3):
            text(str):
            font_name(str): font of text
            font_size(int): size of text
        """
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


