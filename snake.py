import pygame
import sys
import random
from pygame.math import Vector2


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_element(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()  # reposition the fruit
            self.snake.add_block()  # add another block to the snake
            self.snake.play_crunch_sound()

        # 혹시나 몸에 생기면 다시 생성
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        # check if snake if outside ot the screen
        if not 0 <= self.snake.body[0].x < cell_number or \
                not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        # check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        # pygame.quit()
        # sys.exit()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size*cell_number - 60)
        score_y = int(cell_size*cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        apple_rect = apple.get_rect(
            midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width+score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load(
            'Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(
            'Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(
            'Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(
            'Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            # 1. we still need a rect for the positioning
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # 2. what direction is the face heading
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                # same y => 수평 (0,1),(1,1),(2,1)
                # same x => 수직 (1,1),(1,2),(1,3)
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)

                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    # 코너부분
                    if previous_block.x == -1 and next_block.y == -1 or\
                            previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)

                    elif previous_block.x == -1 and next_block.y == 1 or\
                            previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)

                    elif previous_block.x == 1 and next_block.y == -1 or\
                            previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)

                    elif previous_block.x == 1 and next_block.y == 1 or\
                            previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

                        # else:
                        #     pygame.draw.rect(screen, (150, 100, 100), block_rect)

    def update_head_graphics(self):
        # 현재 내 머리가 어느 방향을 향하고 있는지?? 0번째 : 머리, 1번째 : 몸통
        # [(0,0),(1,0),(2,0)]
        # [(0,1),(1,1),(2,1)]
        # [(0,2),(1,2),(2,2)]
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(0, 1):  # 위 => 몸통 - 머리 == (0,1)
            self.head = self.head_up
        elif head_relation == Vector2(-1, 0):  # 오른쪽 => 몸통 - 머리 == (-1,0)
            self.head = self.head_right
        elif head_relation == Vector2(0, -1):  # 아래 => 몸통 - 머리 == (0,-1)
            self.head = self.head_down
        elif head_relation == Vector2(1, 0):  # 왼쪽 => 몸통 - 머리 == (1,0)
            self.head = self.head_left

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
        elif tail_relation == Vector2(1, 0):
            self.tail = self.tail_left

    def move_snake(self):
        if self.new_block == True:
            # 사과를 먹어서 길이가 들어남 => 원래길이 전부 복사후 첫번째항목을 추가
            body_copy = self.body[:]
            # 첫번째항목: 머리 부분을 방향을 추가해서 이동
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            # 마지막 원소 빼고 복사
            body_copy = self.body[:-1]
            # 첫번째항목: 머리 부분을 방향을 추가해서 이동
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        # create a rectangle
        # draw the rectangle
        # x,y,w,h
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size),
                                 int(self.pos.y*cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        # create and x and y position
        # draw a square
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)  # x,y


pygame.mixer.pre_init(44100, -16, 2, 512)  # 사운드 딜레이 제거
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode(
    (cell_number * cell_size, cell_number * cell_size))  # width,heigth
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font(
    'Font/PoetsenOne-Regular.ttf', 25)  # font, fontsize


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  # milliseconds

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # 위로 가는 도중에 아래로 이동전환 불가능
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)

            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)

            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))

    main_game.draw_element()

    # draw all our elements.
    pygame.display.update()
    clock.tick(60)  # framerate
