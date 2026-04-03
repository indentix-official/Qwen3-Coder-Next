import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        start_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT // 2
        self.body = [
            [start_x, start_y],
            [start_x - CELL_SIZE, start_y],
            [start_x - 2 * CELL_SIZE, start_y]
        ]
        self.direction = RIGHT
        self.grow = False

    def move(self):
        head = self.body[0].copy()
        head[0] += self.direction[0] * CELL_SIZE
        head[1] += self.direction[1] * CELL_SIZE
        self.body.insert(0, head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def check_collision(self):
        head = self.body[0]
        
        # Wall collision
        if (head[0] < 0 or head[0] >= WINDOW_WIDTH or
            head[1] < 0 or head[1] >= WINDOW_HEIGHT):
            return True
        
        # Self collision
        if head in self.body[1:]:
            return True
        
        return False

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            color = DARK_GREEN if i == 0 else GREEN
            pygame.draw.rect(screen, color, 
                           (segment[0], segment[1], CELL_SIZE, CELL_SIZE))


class Food:
    def __init__(self):
        self.position = [0, 0]
        self.spawn()

    def spawn(self, snake_body=None):
        while True:
            x = random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            self.position = [x, y]
            
            # Make sure food doesn't spawn on snake
            if snake_body is None or self.position not in snake_body:
                break

    def draw(self, screen):
        pygame.draw.rect(screen, RED, 
                        (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
        
        return True

    def update(self):
        if self.game_over:
            return

        self.snake.move()

        # Check food collision
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.score += 10
            self.food.spawn(self.snake.body)

        # Check game over
        if self.snake.check_collision():
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)
        
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            
            self.screen.blit(game_over_text, 
                           (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                            WINDOW_HEIGHT // 2 - 60))
            self.screen.blit(score_text, 
                           (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 
                            WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(restart_text, 
                           (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 
                            WINDOW_HEIGHT // 2 + 30))
        
        pygame.display.flip()

    def reset(self):
        self.snake.reset()
        self.food.spawn()
        self.score = 0
        self.game_over = False

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
