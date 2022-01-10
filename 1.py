import pygame

WIDTH = 680
HEIGHT = 640 # устанавливаю константы для удобства
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0) # устанавливаю цвета для удобства
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)


pygame.init() # иницализация

myfont = pygame.font.SysFont('Arial', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_window_surface = pygame.Surface((WIDTH, HEIGHT))
game_window_surface = pygame.Surface((WIDTH, HEIGHT)) #
start_window_surface.fill(WHITE)
game_window_surface.fill(GREY)

pygame.display.set_caption("Игра жизнь") # название
clock = pygame.time.Clock() #часики для установки FPS

#создаем картинки, которые будут необходимы для игры
start_button_image = pygame.Surface((300, 50))
start_button_image.fill(GREY)

empty_cell_image = pygame.Surface((39, 39))
empty_cell_image.fill(WHITE)

cell_with_life_image = pygame.Surface((39, 39))
cell_with_life_image.fill(BLACK)

run_game_button_image = pygame.Surface((40, 170))
run_game_button_image.fill(RED)

next_step_button_image = pygame.Surface((40, 170))
next_step_button_image.fill(GREEN)

clear_button_image = pygame.Surface((40, 170))
clear_button_image.fill(YELLOW)
#тексты для кнопок
text_start_game = myfont.render('Начать игру', False, BLACK)
text_next_step = myfont.render('>', False, BLACK)
text_run_game = myfont.render('>>', False, BLACK)
text_clear = myfont.render('X', False, BLACK)
#спрайты
start_window_sprites = pygame.sprite.Group()
button_game_sprites = pygame.sprite.Group()
cell_sprites = pygame.sprite.Group()


class Button(pygame.sprite.Sprite): #кнопочки
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        size = self.image.get_rect().size
        self.height = size[1]
        self.width = size[0]
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def pressed(self, mouse): # проверка на нажатие
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            return True
        return False

    def change_image(self, image): # смена картинки
        self.image = image


class Field:
    def __init__(self):
        self.table = [[0] * 16 for k in range(16)]
        for ind_y in range(16):
            for ind_x in range(16):
                cell = Cell(ind_x * 40, ind_y * 40)
                self.table[ind_y][ind_x] = cell
                cell_sprites.add(cell)

    def update(self):
        self.new_table = [[0] * 16 for k in range(16)] # создание доски для инф-ии на след. шаге
        for ind_y in range(16):
            for ind_x in range(16):
                self.check_cell(ind_y, ind_x)
        for ind_y in range(16):
            for ind_x in range(16):
                if self.new_table[ind_y][ind_x] == 1:
                    self.table[ind_y][ind_x].change_value_on_life()
                else:
                    self.table[ind_y][ind_x].change_value_on_empty()

    def check_cell(self, index_y, index_x):
        count_cell_with_life = 0

        if index_y - 1 >= 0:
            if self.table[index_y - 1][index_x].is_living:
                count_cell_with_life += 1
            if index_x - 1 >= 0:
                if self.table[index_y - 1][index_x - 1].is_living:
                    count_cell_with_life += 1
            if index_x + 1 <= 15:
                if self.table[index_y - 1][index_x + 1].is_living:
                    count_cell_with_life += 1

        if index_x - 1 >= 0:
            if self.table[index_y][index_x - 1].is_living:
                count_cell_with_life += 1
        if index_x + 1 <= 15:
            if self.table[index_y][index_x + 1].is_living:
                count_cell_with_life += 1

        if index_y + 1 <= 15:
            if self.table[index_y + 1][index_x].is_living:
                count_cell_with_life += 1
            if index_x - 1 >= 0:
                if self.table[index_y + 1][index_x - 1].is_living:
                    count_cell_with_life += 1
            if index_x + 1 <= 15:
                if self.table[index_y + 1][index_x + 1].is_living:
                    count_cell_with_life += 1

        if self.table[index_y][index_x].is_living:
            if count_cell_with_life == 2 or count_cell_with_life == 3:
                self.new_table[index_y][index_x] = 1
        else:
            if count_cell_with_life == 3:
                self.new_table[index_y][index_x] = 1

    def return_game_over(self): # возвращение инф-ии о конце игры(если не осталось живых клеток)
        for ind_y in range(16):
            for ind_x in range(16):
                if self.table[ind_y][ind_x].is_living:
                    return False
        return True

    def reborn(self): #пересоздание
        for sprite in cell_sprites:
            sprite.kill()
        self.__init__()


class Cell(Button):
    def __init__(self, x, y):
        self.is_living = False
        super().__init__(x, y, empty_cell_image)

    def change_value_on_life(self):
        self.image = cell_with_life_image
        self.is_living = True

    def change_value_on_empty(self):
        self.image = empty_cell_image
        self.is_living = False

    def change_value(self):
        if self.is_living:
            self.change_value_on_empty()
        else:
            self.change_value_on_life()



start_button = Button(190, 295, start_button_image)
start_window_sprites.add(start_button)

run_game_button = Button(640, 0, run_game_button_image)
button_game_sprites.add(run_game_button)

next_step_button = Button(640, 170, next_step_button_image)
button_game_sprites.add(next_step_button)

clear_button = Button(640, 340, clear_button_image)
button_game_sprites.add(clear_button)

start_window = True
run_processing = False
one_step = False
game_running = False
running = True
while running:
    clock.tick(FPS)
    if start_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.pressed(event.pos):
                    start_window = False
                    game_running = True
                    game_field = Field() #создание поля
        start_window_surface.fill(WHITE)
        start_window_sprites.update()
        start_window_sprites.draw(start_window_surface)
        screen.blit(start_window_surface, (0, 0))

        screen.blit(text_start_game, (260, 295))
    elif game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not run_processing:
                    if run_game_button.pressed(event.pos):
                        run_processing = True
                    elif next_step_button.pressed(event.pos):
                        run_processing = True
                        one_step = True
                    else:
                        for i in cell_sprites:
                            if i.pressed(event.pos):
                                i.change_value()
                                print(i.y, i.x, i.is_living)
                if clear_button.pressed(event.pos):
                    game_field.reborn()
                    run_processing = False

        if run_processing:
            game_field.update()
            if one_step or game_field.return_game_over(): #остановка игры
                run_processing = False
                one_step = False

        game_window_surface.fill(GREY)

        cell_sprites.update()
        button_game_sprites.update()

        cell_sprites.draw(game_window_surface)
        button_game_sprites.draw(game_window_surface)

        screen.blit(game_window_surface, (0, 0))

        screen.blit(text_run_game, (640, 70))
        screen.blit(text_next_step, (650, 170 + 70)) #текст на кнопках
        screen.blit(text_clear, (650, 340 + 70))
    pygame.display.flip()
pygame.quit()