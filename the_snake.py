from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        self.position = (0, 0)
        self.body_color = body_color

    def draw_cell(self, position, color):
        """Отрисовка одной ячейки (клетки)."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Метод отрисовки объекта (переопределяется в наследниках)."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Устанавливает случайную позицию яблока вне змейки."""
        # Генерируем список всех возможных координат на поле
        all_cells = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        ]
        # Исключаем координаты, занятые змейкой
        free_cells = list(set(all_cells) - set(snake_positions))

        if free_cells:
            self.position = choice(free_cells)

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.reset()

    def reset(self):
        """Сбрасывает состояние змейки в начальное."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # Согласно критериям, начальное направление должно быть случайным
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении."""
        head = self.get_head_position()
        dx, dy = self.direction

        # Вычисление новой позиции головы с учетом прохождения сквозь границы
        new_head = (
            (head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Проверка на самопересечение (столкновение с телом)
        if new_head in self.positions[1:]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        # Если длина достигла предела, удаляем хвост
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовка змейки."""
        # Отрисовываем тело
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента (если хвост сместился)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обработка действий пользователя."""
    # Словарь для более элегантной смены направления (из рекомендаций)
    key_direction_map = {
        (pygame.K_UP, DOWN): UP,
        (pygame.K_DOWN, UP): DOWN,
        (pygame.K_LEFT, RIGHT): LEFT,
        (pygame.K_RIGHT, LEFT): RIGHT,
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

            # Проверяем, есть ли нажатая клавиша в словаре
            # и не является ли она противоположной текущему направлению
            for (key, opposite_dir), new_dir in key_direction_map.items():
                if event.key == key and game_object.direction != opposite_dir:
                    game_object.next_direction = new_dir


def main():
    """Запускает основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов:
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()