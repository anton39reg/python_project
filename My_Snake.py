import pygame
import sys
import random
import time

from pygame.rect import Rect


class GameObject:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bounds = Rect(x, y, w, h)

    def draw(self, surface):
        pass

    def update(self):
        pass


class Square(GameObject):
    def __init__(self, x, y, a, color):
        GameObject.__init__(self, x, y, a, a)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)


class Apple(GameObject):
    def __init__(self, x, y, a, color):
        GameObject.__init__(self, x, y, a, a)
        self.color = color
        self.a = a

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def update(self, w, h):
        self.x = random.randrange(0, w//self.a)*self.a
        self.y = random.randrange(0, h//self.a)*self.a
        self.bounds = Rect(self.x, self.y, self.a, self.a)


class Snake:
    def __init__(self, list_of_pos, a, direction, color):
        self.head = list_of_pos[0]
        self.body = []
        self.a = a
        self.color = color
        for i in list_of_pos:
            self.body.append(Square(i[0], i[1], a, self.color))
        self.direction = direction

    def draw(self, surface):
        for i in self.body:
            i.draw(surface)

    def update(self):
        if self.direction == 'RIGHT':
            self.head = self.head[0] + self.a, self.head[1]
        elif self.direction == 'LEFT':
            self.head = self.head[0] - self.a, self.head[1]
        elif self.direction == 'UP':
            self.head = self.head[0], self.head[1] - self.a
        elif self.direction == 'DOWN':
            self.head = self.head[0], self.head[1] + self.a
        self.body.insert(0, Square(self.head[0], self.head[1], self.a, self.color))

    def delete_tail(self):
        self.body.pop()

    def new_direction(self, command):
        if command == 'LEFT' and self.direction != 'RIGHT':
            self.direction = command
        if command == 'RIGHT' and self.direction != 'LEFT':
            self.direction = command
        if command == 'UP' and self.direction != 'DOWN':
            self.direction = command
        if command == 'DOWN' and self.direction != 'UP':
            self.direction = command


class TextObject:
    def __init__(self, x, y, text_func, color, font_name, font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface

    def draw(self, surface, centralized=False):
        text_surface = self.get_surface(self.text_func)
        pos = self.pos
        surface.blit(text_surface, pos)

    def get_update(self):
        pass


def crash_into_wall(w, h, snake):
    if snake.head[0] < 0 or snake.head[0] > w or snake.head[1] < 0 or snake.head[1] > h:
        return False
    return True


def crash_himself(snake):
    for i in snake.body[1:]:
        if snake.head == (i.x, i.y):
            return False
    return True


def check_problems(w, h, objects):
    if not crash_into_wall(w, h, objects[0]):
        return False
    if not crash_himself(objects[0]):
        return False
    return True


def gameOver(Surface):
    myFont = pygame.font.SysFont('monaco', 108)
    GOsurf = myFont.render("Game Over", True, (255, 0, 0))
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (400, 25)
    Surface.blit(GOsurf, GOrect)
    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self, caption, width, height, frame_rate):
        pygame.init()
        self.score = 0
        self.text = TextObject(0, 0, 'Score: {}'.format(self.score), (0, 0, 0), 'monaco', 36)
        self.width = width
        self.height = height
        a = 15
        body_snake = [((width//100)*a - a * i, (height//200)*a) for i in range(3)]
        self.objects = [Snake(body_snake, a, 'RIGHT', (0, 255, 0)),
                        Apple(random.randrange(0, width//a)*a, random.randrange(0, height//a)*a, a, (255, 0, 0))]
        self.surface = pygame.display.set_mode((width, height))
        self.frame_rate = frame_rate
        self.game_over = False
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.objects[0].new_direction('RIGHT')
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.objects[0].new_direction('LEFT')
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.objects[0].new_direction('UP')
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.objects[0].new_direction('DOWN')
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        if self.objects[0].head == (self.objects[1].x, self.objects[1].y):
            self.score += 1
            self.text = self.text = TextObject(0, 0, 'Score: {}'.format(self.score), (0, 0, 0), 'monaco', 36)
            self.frame_rate += 0.5
            self.objects[0].update()
            self.objects[1].update(self.width, self.height)
        else:
            self.objects[0].update()
            self.objects[0].delete_tail()

    def draw(self):
        for elem in self.objects:
            elem.draw(self.surface)
        self.text.draw(self.surface)

    def run(self):
        while not self.game_over:
            self.surface.fill((244, 164, 96))

            if not check_problems(self.width, self.height, self.objects):
                gameOver(self.surface)
                break

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)


a = Game('snake', 1280, 640, 10)
a.run()
