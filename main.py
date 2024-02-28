import pygame
import random

WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GRAY = (50, 50, 50)

SPEEDS = {'Easy': 5, 'Medium': 10, 'Hard': 15}

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont("Courier New", 25)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((720, 480))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.difficulty = None
        self.best_scores = {'Easy': 0, 'Medium': 0, 'Hard': 0}
        self.reset()
        self.snake = [(20, 20)]
        self.buttons = []
        self.snake_direction = (1, 0)
        self.lost = False
        self.score = 0
        self.food = self.generate_food()
        self.choose_difficulty()

    def reset(self):
        self.snake = [(20, 20)]
        self.snake_direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.lost = False

    def choose_difficulty(self):
        self.buttons = []
        difficulty_text = "CHOOSE YOUR DIFFICULTY LEVEL FOR YOUR GAME:"
        button_width = 300
        button_height = 40
        button_spacing = 10

        total_buttons_height = len(SPEEDS) * (button_height + button_spacing) - button_spacing
        start_y = (self.screen.get_height() - total_buttons_height) // 2 - 50
        button_x = (self.screen.get_width() - button_width) // 2

        self.screen.fill(WHITE)

        self.draw_difficulty_text(difficulty_text, start_y)

        selected_button_index = 0

        for i, (difficulty, _) in enumerate(SPEEDS.items()):
            button = Button(button_x, start_y + int(i) * (button_height + button_spacing), button_width, button_height,
                            DARK_GRAY, difficulty)
            self.buttons.append(button)

        self.buttons[selected_button_index].color = RED

        self.display_buttons()

        self.handle_difficulty_selection(selected_button_index)

    def display_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()

    def handle_difficulty_selection(self, selected_button_index):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_button_index = (selected_button_index - 1) % len(self.buttons)
                    elif event.key == pygame.K_DOWN:
                        selected_button_index = (selected_button_index + 1) % len(self.buttons)
                    elif event.key == pygame.K_RETURN:
                        self.difficulty = self.buttons[selected_button_index].text
                        return

                    self.highlight_selected_button(selected_button_index)
                    pygame.display.update()

    def highlight_selected_button(self, selected_button_index):
        for i, button in enumerate(self.buttons):
            if i == selected_button_index:
                button.color = RED
            else:
                button.color = DARK_GRAY
        self.display_buttons()

    def draw_difficulty_text(self, difficulty_text, start_y):
        font = pygame.font.SysFont("Courier New", 30)
        text_surface = font.render(difficulty_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, start_y - 30))
        self.screen.blit(text_surface, text_rect)

    def generate_food(self):
        while True:
            food_x = random.randint(0, self.screen.get_width() // 20 - 1)
            food_y = random.randint(0, self.screen.get_height() // 20 - 1)
            food = (food_x, food_y)
            if food not in self.snake:
                return food

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake_direction != DOWN:
                    self.snake_direction = UP
                elif event.key == pygame.K_DOWN and self.snake_direction != UP:
                    self.snake_direction = DOWN
                elif event.key == pygame.K_LEFT and self.snake_direction != RIGHT:
                    self.snake_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.snake_direction != LEFT:
                    self.snake_direction = RIGHT

    def move_snake(self):
        new_head = (self.snake[0][0] + self.snake_direction[0], self.snake[0][1] + self.snake_direction[1])

        if (
                new_head[0] < 0 or new_head[0] >= self.screen.get_width() // 20 or
                new_head[1] < 0 or new_head[1] >= self.screen.get_height() // 20 or
                new_head in self.snake
        ):
            self.lost = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(DARK_GRAY)
        self.draw_snake()
        self.draw_food()
        self.draw_score()
        pygame.display.update()

    def draw_snake(self):
        for block in self.snake:
            pygame.draw.rect(self.screen, GREEN, (block[0] * 20, block[1] * 20, 20, 20))

    def draw_food(self):
        pygame.draw.circle(self.screen, RED,
                           (self.food[0] * 20 + 10, self.food[1] * 20 + 10), 10)

    def draw_score(self):
        font = pygame.font.SysFont("Courier New", 25)
        score_text = font.render('Score: ' + str(self.score), True, WHITE)
        self.screen.blit(score_text, [10, 10])

    def run(self):
        while True:
            self.reset()
            while not self.lost:
                self.handle_events()
                self.move_snake()
                self.draw()
                self.clock.tick(SPEEDS[self.difficulty])

            self.update_best_score()
            self.display_loss_message()

    def update_best_score(self):
        if self.difficulty is not None and self.difficulty in self.best_scores:
            if self.score > self.best_scores[self.difficulty]:
                self.best_scores[self.difficulty] = self.score

    def display_loss_message(self):
        font_large = pygame.font.SysFont("Courier New", 40, bold=True)
        font_medium = pygame.font.SysFont("Courier New", 30)
        font_small = pygame.font.SysFont("Courier New", 25)

        message_large = font_large.render('YOU LOST!', True, RED)
        message_score = font_medium.render('Your best score is: ' + str(self.best_scores[self.difficulty]),
                                           True, WHITE)

        message_small = font_small.render('Press SPACE to play again.', True, RED)
        message_change_difficulty = font_small.render('Press ESC to change difficulty.', True, RED)

        large_text_rect = message_large.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        score_text_rect = message_score.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        small_text_rect = message_small.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 1.5))
        change_difficulty_rect = message_change_difficulty.get_rect(center=(self.screen.get_width() // 2,
                                                                            self.screen.get_height() // 1.3))

        self.screen.blit(message_large, large_text_rect)
        self.screen.blit(message_score, score_text_rect)
        self.screen.blit(message_small, small_text_rect)
        self.screen.blit(message_change_difficulty, change_difficulty_rect)
        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_input = False
                    elif event.key == pygame.K_ESCAPE:
                        self.choose_difficulty()
                        waiting_for_input = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
