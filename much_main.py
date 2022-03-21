import pygame
import os
import sys
from random import randrange, choice


# определяю все важные константы
ALL_DIR = 'data/'
SIZE = WIDTH, HEIGHT = 576, 676
FPS = 25
LEFT, TOP = 0, 98
SCREEN = None
CELL_SIZE = None

WHITE = pygame.Color(204, 204, 191)
GREEN = pygame.Color(103, 173, 115)
BLUE = pygame.Color(124, 164, 197)
DARK_BLUE = pygame.Color(67, 52, 85)
GREY = pygame.Color(78, 96, 128)

pygame.init()
pygame.display.set_caption('lines_attempt1212143')
SCREEN = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

pygame.mixer.music.load(ALL_DIR + 'sounds/calm_music.mp3')
pygame.mixer.music.play(-1)


def load_image(name, colorkey=None):
    """функция загрузки изображений + сразу убирает фон, если надо"""
    fullname = os.path.join(ALL_DIR, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    """начальный экран со всеми правилами"""
    screen.fill(WHITE)
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, WIDTH // 2))
    jess_ims = {0: load_image('jess_0.png'), 1: load_image('jess_1.png'), 2: load_image('jess_1.png')}
    cur_jess = 0
    jx, jy = jess_ims[0].get_width(), jess_ims[0].get_height()
    intro = {0: ["Правила игры:", "",
                 "Собери линию из 5+ одинаковых цветов",
                 "И помоги Джесс в её лавке!",
                 "Нажми ENTER, чтобы начать игру", ""
                 "Или перетащи Джесс, зажав",
                 "Левую кнопку мыши :-) "]}

    grab = False
    x, y = WIDTH - jx, HEIGHT - jy - 290
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                grab = True
            elif event.type == pygame.MOUSEBUTTONUP:
                grab = False
                x, y = WIDTH - jx, HEIGHT - jy - 290
            elif event.type == pygame.MOUSEMOTION and grab:
                new_x, new_y = event.rel
                x += new_x
                y += new_y
        screen.blit(fon, (0, HEIGHT - fon.get_rect().height))
        font = pygame.font.Font(f'{ALL_DIR}pix_font.ttf', 14)
        text_coord = 50
        for line in intro[0]:
            string_rendered = font.render(line, True, GREY)
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.bottom = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        jess = jess_ims[cur_jess]
        screen.blit(jess, (x, y))
        cur_jess = (cur_jess + 1) % 3
        pygame.display.flip()
        screen.fill(WHITE)
        clock.tick(15)


def load_screen(screen):
    """я не знаю какую пользу он мне приносит, но зато красиво :)"""
    loading_end = pygame.USEREVENT + 1
    cur_pic = 0
    cur_let = 0
    pygame.time.set_timer(loading_end, 5000, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == loading_end:
                return
        screen.fill(WHITE)
        num = str(cur_pic) if cur_pic >= 10 else '0' + str(cur_pic)
        fon = pygame.transform.scale(load_image('load_fon' + num + '.png', -1), (WIDTH, HEIGHT - 100))
        screen.blit(fon, (0, 120))
        line = "LOADING..."[:cur_let]
        font = pygame.font.Font(f'{ALL_DIR}pix_font.ttf', 45)
        string_rendered = font.render(line, True, BLUE)
        intro_rect = string_rendered.get_rect()
        intro_rect.centerx = WIDTH // 2
        intro_rect.centery = 70
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        cur_pic = (cur_pic + 1) % 30
        cur_let = (cur_let + 1) % 11
        clock.tick(12)


def gameover_screen(screen):
    """возникает при завершении игры"""
    

    screen.fill(WHITE)
    text = '- GAME OVER -'
    font = pygame.font.Font(f'{ALL_DIR}pix_font.ttf', 55)
    text_coord = 200
    for _ in range(3):
        screen.fill(WHITE)
        for i, color in enumerate((GREY, BLUE, GREEN)):
            st = font.render(text, True, color)
            rect = st.get_rect()
            rect.bottom = text_coord + i * 35
            rect.x = 20
            screen.blit(st, rect)
            pygame.display.flip()
            clock.tick(10)
    screen.fill(WHITE)
    screen.blit(st, rect)

    new_game = ('новая игра', 70, 400)
    leave = ('выйти', 370, 400)
    font1 = pygame.font.Font(f'{ALL_DIR}pix_font.ttf', 25)
    for g in (new_game, leave):
        t, x, y = g
        st = font1.render(t, True, GREY)
        rect = st.get_rect()
        rect.bottom = y
        rect.x = x
        screen.blit(st, rect)
        pygame.display.flip()
        clock.tick(10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 70 <= x <= 270 and 370 <= y <= 400:
                    return  # начинаем игру заново
                elif 370 <= x <= 450 and 370 <= y <= 400:
                    terminate()
        x, y = pygame.mouse.get_pos()
        g = '00'
        if 70 <= x <= 270 and 370 <= y <= 400:
            g = '10'
        elif 370 <= x <= 450 and 370 <= y <= 400:
            g = g[0] + '1'
        if g == '00':
            colors = (GREY, GREY)
        elif g == '11':
            colors = (GREEN, BLUE)
        elif g == '10':
            colors = (GREEN, GREY)
        else:
            colors = (GREY, GREEN)

        new_game = ('новая игра', 70, 400)
        leave = ('выйти', 370, 400)
        i = 0
        for g in (new_game, leave):
            t, x, y = g
            st1 = font1.render(t, True, colors[i])
            rect1 = st1.get_rect()
            rect1.bottom = y
            rect1.x = x
            i += 1
            screen.blit(st1, rect1)
            pygame.display.flip()

        pygame.display.flip()
        clock.tick(14)


# тут все картинки шаров-суккулентов
plant_images = {}
for i in range(1, 7):
    plant_images[i] = load_image(str(i) + 'ball.png')


class Lines:
    # self.board - двумерный список, хранящий все шары
    # или None, если таковых в определенной клетке нет
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[None] * width for _ in range(height)]
        self.free = [(i, j) for i in range(width) for j in range(height)]
        self.cell_size = WIDTH // width
        # да, так делать не очень хорошо, но пока так :)))
        global CELL_SIZE
        CELL_SIZE = self.cell_size
        self.cur_ball = None
        self.ball_count = 81
        self.count = 0
        self.add_balls(3)

    def on_click(self, cell):
        """обрабатывем клик пользователя"""
        # если кликнули не на поле - выходим
        if cell is None:
            return
        y, x = cell
        if self.is_free((y, x)):
            if self.cur_ball is not None:
                y0, x0 = self.cur_ball.get_position()
                path = self.find_path((y0, x0), (x, y))
                if len(path) > 1:
                    # передвигаю шар на нужное место
                    self.free.append((y0, x0))
                    self.free.remove((y, x))
                    self.board[y0][x0] = None
                    self.board[y][x] = self.cur_ball
                    self.cur_ball.way = path
                    self.cur_ball.on_click = False
                    self.cur_ball = None
                    clock.tick(FPS)
                    found, lines = self.find_lines()
                    if found:
                        self.count += len(lines) * 2
                        self.clear_balls(lines)
                    else:
                        self.add_balls(3)
                        again_found, lines = self.find_lines()
                        if again_found:
                            self.count += len(lines) * 2
                            self.clear_balls(lines)
        elif self.board[y][x] is not None:
            b = self.board[y][x]
            if b.on_click:
                b.on_click = False
                self.cur_ball = None
            else:
                if self.cur_ball is not None:
                    self.cur_ball.on_click = False
                self.cur_ball = b
                self.cur_ball.on_click = True

    def clear_balls(self, balls):
        """метод убирает шары, стоящие на определенных позициях с поля"""
        for el in balls:
            b = self.board[el[0]][el[1]]
            b.kill()
            self.ball_count += 1
            self.board[el[0]][el[1]] = None
            self.free += [el]

    def add_balls(self, n):
        """метод добавляет н шаров на поле"""
        for i in range(n):
            if len(self.free) > 0:
                pos = choice(self.free)  # выбираю случайную позицию
                self.board[pos[0]][pos[1]] = self.get_new_ball(pos)  # вставляю в выбранное поле новый шар

    def get_cell(self, mouse_pos):
        """метод получает позицию, на которую указал курсор"""
        x, y = mouse_pos
        i = x // self.cell_size
        j = (y - TOP) // self.cell_size
        if i > self.width - 1 or i < 0 or j < 0 or j > self.height - 1:
            return None
        return j, i

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def is_free(self, pos):
        """метод проверяет свободна ли определенная позиция"""
        if self.board[pos[0]][pos[1]] is None:
            return True
        return False

    def find_lines(self):
        """ищем линнии, собранные из 5ех и больше шаров"""
        found = False
        lines = set()
        # по горизонтали
        for j in range(self.height):
            r = ''
            for el in self.board[j]:
                if el is not None:
                    r += str(el.color)
                else:
                    r += '0'
            for i in range(1, 7):
                a = r.find(str(i) * 5)
                if a == -1:
                    continue
                else:
                    lines |= set((j, a + i) for i in range(5))
                    a += 5
                    while a < len(r) and r[a] == str(i):
                        lines.add((j, a))
                        a += 1
        # поиск по вертикали
        for j in range(self.width):
            c = ''
            for el in [self.board[i][j] for i in range(self.height)]:
                if el is not None:
                    c += str(el.color)
                else:
                    c += '0'
            for i in range(1, 7):
                a = c.find(str(i) * 5)
                if a == -1:
                    continue
                else:
                    lines |= set((a + i, j) for i in range(5))
                    a += 5
                    while a < len(c) and c[a] == str(i):
                        lines.add((a, j))
                        a += 1
        # поиск по диагонали
        start = [(0, i) for i in range(self.width - 4)] + [(i, 0) for i in range(1, self.height - 4)]
        for el in start:
            d = ''
            y, x = el
            for i in range(min(self.width - x, self.height - y)):
                b = self.board[y + i][x + i]
                if b is None:
                    d += '0'
                else:
                    d += str(b.color)
            for i in range(1, 7):
                a = d.find(str(i) * 5)
                if a == -1:
                    continue
                else:
                    # ИСПРАВИЛА тут и ниже :) теперь ошибки не возникает!
                    lines |= set((y + a + i, x + a + i) for i in range(5))
                    a += 5
                    while a < len(d) and d[a] == str(i):
                        lines.add((y + a, x + a))
                        a += 1
        # поиск по диагонали
        start = [(8, i) for i in range(self.width - 4)] + [(i, 0) for i in range(4, self.height - 1)]
        for el in start:
            d = ''
            y, x = el
            for i in range(abs(x - y) + 1):
                b = self.board[y - i][x + i]
                if b is None:
                    d += '0'
                else:
                    d += str(b.color)
            for i in range(1, 7):
                a = d.find(str(i) * 5)
                if a == -1:
                    continue
                else:
                    # тут тоже изменила немного, вроде не должно быть ошибок
                    lines |= set((y - a - i, x + a + i) for i in range(5))
                    a += 5
                    while a < len(d) and d[a] == str(i):
                        lines.add((y - a, x + a))
                        a += 1
        if len(lines) >= 5:
            found = True
        return found, lines

    def find_path(self, start, target):
        """метод ищет путь от одной клетки доски до другой с помощью алгоритма ли"""
        m = [[0] * len(self.board[0]) for _ in range(len(self.board))]
        x, y = start
        m[x][y] = 1
        k = 0
        x1, y1 = target
        while m[y1][x1] == 0:
            k += 1
            if not self.make_step(k, m):
                break
            # выполняя шаг, в то же время проверяем, возможно шагнуть вообще или нет
            # если нет, то, конечно, заканчиваем волну.
        # pprint(m)
        # восстанавливаем путь для шара
        k = m[y1][x1]
        path = [(y1, x1)]
        while k > 1:
            if y1 > 0 and m[y1 - 1][x1] == k - 1:
                y1, x1 = y1 - 1, x1
                path.append((y1, x1))
                k -= 1
            elif x1 > 0 and m[y1][x1 - 1] == k - 1:
                y1, x1 = y1, x1 - 1
                path.append((y1, x1))
                k -= 1
            elif y1 < len(m) - 1 and m[y1 + 1][x1] == k - 1:
                y1, x1 = y1 + 1, x1
                path.append((y1, x1))
                k -= 1
            elif x1 < len(m[y1]) - 1 and m[y1][x1 + 1] == k - 1:
                y1, x1 = y1, x1 + 1
                path.append((y1, x1))
                k -= 1
        # print(path[::-1])
        return path[::-1]

    def make_step(self, k, m):
        """один шаг волнового алгоритма ли"""
        flag = False
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == k:
                    if i > 0 and m[i - 1][j] == 0 and self.is_free((i - 1, j)):  #self.board[i - 1][j].is_free is None:
                        m[i - 1][j] = k + 1
                        flag = True
                    if j > 0 and m[i][j - 1] == 0 and self.is_free((i, j - 1)):  #self.board[i][j - 1] is None:
                        m[i][j - 1] = k + 1
                        flag = True
                    if i < len(m) - 1 and m[i + 1][j] == 0 and self.is_free((i + 1, j)):  #self.board[i + 1][j] is None:
                        m[i + 1][j] = k + 1
                        flag = True
                    if j < len(m[i]) - 1 and m[i][j + 1] == 0 and self.is_free((i, j + 1)):  #self.board[i][j + 1] is None:
                        m[i][j + 1] = k + 1
                        flag = True
        if not flag:
            # если мы никуда ни откуда не можем сделать шаг, то пора заканчивать
            return False
        return True

    def get_new_ball(self, pos):
        # создаю новый шар
        self.ball_count -= 1
        self.free.remove(pos)  # удаляю занятое поле из списка
        return Ball(pos, color=randrange(1, 7))


class Ball(pygame.sprite.Sprite):
    def __init__(self, position, color=1, size=10):
        super().__init__(all_sprites)
        self.ball_image = plant_images[color]
        self.image = pygame.transform.scale(self.ball_image, (size, size))
        self.position = position
        self.color = color  # color - параметр, задающий цвет шарика, целое число от 1 до 6
        self.rect = self.image.get_rect()
        self.size = size
        self.set_position(position)
        self.on_click = False  # on_click - выбран ли шар в данный момент
        self.way = []  # way - путь, который должен пройти шар
        self.d = -2  # d - изменение шара (нужно для выделения его при выборе)

    def get_position(self):
        """возвращаю позицию шара на доске"""
        return self.position

    def set_position(self, position):
        """задаю шару определенную позицию на доске"""
        y, x = position
        self.position = position
        self.rect.x, self.rect.y = (x + 0.5) * CELL_SIZE + LEFT - self.size // 2,\
                   (y + 0.5) * CELL_SIZE + TOP - self.size // 2

    def update(self):
        """вид шара на экране"""
        if self.size <= 50 and not self.on_click:  # если это новый шар
            self.image = pygame.transform.scale(self.ball_image, (self.size, self.size))
            self.set_position(self.position)
            self.size += 5
        elif self.on_click:  # делаем видимым выбранный шар
            if self.size <= 44:
                self.d = 2
            elif self.size >= 56:
                self.d = -2
            self.size = self.size + self.d
            self.image = pygame.transform.scale(self.ball_image, (self.size, self.size))
            self.set_position(self.position)
        elif not self.on_click and self.way == []:  # если выбрали другой шарик, то пульсирование остановить
            self.image = pygame.transform.scale(self.ball_image, (self.size, self.size))
            self.set_position(self.position)
        if len(self.way) > 1:
            # если шар нужно передвинуть на другую позицию
            self.move()

    def move(self):
        # движение шара на одну позицию
        a, b = self.way[1]
        self.way = self.way[1:]
        self.set_position((a, b))


def show_results(screen, count, new_game_off, fon):
    """метод выводит результаты и какие-то числовые данные на экран"""
    screen.fill(DARK_BLUE)
    screen.blit(fon, (0, TOP))
    font = pygame.font.Font(f'{ALL_DIR}pix_font.ttf', 17)
    text_coord = 35
    line1 = f'Счет:{" " * (13 - len("Счет:"))}Рекорд:{" " * (13 - len("Рекорд:"))}Осталось:'
    line2 = f'{count}{" " * (17 - len(str(count)))}{record}{" " * (20 - len(str(record)))} {board.ball_count}'
    string_rendered1 = font.render(line1, True, GREEN)
    intro_rect1 = string_rendered1.get_rect()
    text_coord += 10
    intro_rect1.bottom = text_coord
    intro_rect1.x = 10
    text_coord += intro_rect1.height
    screen.blit(string_rendered1, intro_rect1)
    string_rendered = font.render(line2, True, GREEN)
    intro_rect = string_rendered.get_rect()
    text_coord += 10
    intro_rect.bottom = text_coord
    intro_rect.x = 10
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    screen.blit(new_game_off, (420, 35))


all_sprites = pygame.sprite.Group()
#load_screen(SCREEN)
#start_screen(SCREEN)

board = Lines(9, 9)

# еще нужные надписи
ngame_on = pygame.transform.scale(load_image('new_game_on.png'), (138, 29))
ngame_off = pygame.transform.scale(load_image('new_game_of.png'), (138, 29))
fon = pygame.transform.scale(load_image('field.png'), (WIDTH, HEIGHT))

f = open(ALL_DIR + 'record.txt', 'r')
record = int(f.read())
f.close()
running = True
#running = False

gameover_screen(SCREEN)

while running:
    ngame = ngame_off
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            f = open(ALL_DIR + 'record.txt', 'w')
            f.write(str(record))
            f.close()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # если начали игру заново
            if 420 <= pos[0] <= 558 and 35 <= pos[1] <= 64:
                for b in all_sprites:
                    b.kill()
                board = Lines(9, 9)
                pygame.mixer.music.unpause()
            else:
                board.get_click(pos)

    if 420 <= pygame.mouse.get_pos()[0] <= 558 and 35 <= pygame.mouse.get_pos()[1] <= 64:
        ngame = ngame_on

    if board.ball_count == 0:
        pygame.mixer.music.pause()
        gameover_screen(SCREEN)
        for b in all_sprites:
            b.kill()
        board = Lines(9, 9)
        pygame.mixer.music.unpause()

    if board.count > record:
        record = board.count


    show_results(SCREEN, board.count, ngame, fon)
    all_sprites.draw(SCREEN)
    all_sprites.update()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()