import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SNAKE_SIZE = 10
GRID_WIDTH = 50
GRID_HEIGHT = 45
SCREEN_WIDTH = GRID_WIDTH * SNAKE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * SNAKE_SIZE
PLAY_AREA_WIDTH = SCREEN_WIDTH
PLAY_AREA_HEIGHT = (GRID_HEIGHT - 5) * SNAKE_SIZE
FPS = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (202, 224, 31)

# Fonts
LARGE_FONT = pygame.font.Font('freesansbold.ttf', 30)
SMALL_FONT = pygame.font.Font('freesansbold.ttf', 15)

# Initialize Variables
x, y = PLAY_AREA_WIDTH // 2, PLAY_AREA_HEIGHT // 2
food_x = random.randint(0, (PLAY_AREA_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
food_y = random.randint(5, (PLAY_AREA_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
snake_list = []
snake_length = 1
x_change, y_change = 0, 0
score = 0
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
running = True


# Functions
def display_text(text, font, color, position):
    """Render text at a specified position."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


def draw_snake(snake_list):
    """Draw the entire snake body."""
    for segment in snake_list:
        pygame.draw.rect(screen, YELLOW, (*segment, SNAKE_SIZE, SNAKE_SIZE))


def reset_game():
    """Reset game variables when game over."""
    global x, y, food_x, food_y, x_change, y_change, snake_list, snake_length, score
    x, y = PLAY_AREA_WIDTH // 2, PLAY_AREA_HEIGHT // 2
    snake_list.clear()
    snake_length = 1
    x_change, y_change = 0, 0
    score = 0
    food_x = random.randint(0, (PLAY_AREA_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    food_y = random.randint(5, (PLAY_AREA_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE


def game_over():
    """Display game over screen and reset after delay."""
    screen.fill(WHITE)
    display_text("GAME OVER", LARGE_FONT, RED, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
    pygame.display.update()
    time.sleep(2)
    reset_game()


# Main Game Loop
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, 50, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT), 1)

    # Display Score
    display_text(f"Score: {score}", SMALL_FONT, BLACK, (SCREEN_WIDTH - 100, 20))
    display_text("Snake Game", LARGE_FONT, BLACK, (SCREEN_WIDTH // 2 - 80, 10))

    # Draw food and snake
    pygame.draw.rect(screen, RED, (food_x, food_y, SNAKE_SIZE, SNAKE_SIZE))
    draw_snake(snake_list)

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x_change == 0:
                x_change, y_change = -SNAKE_SIZE, 0
            elif event.key == pygame.K_RIGHT and x_change == 0:
                x_change, y_change = SNAKE_SIZE, 0
            elif event.key == pygame.K_UP and y_change == 0:
                x_change, y_change = 0, -SNAKE_SIZE
            elif event.key == pygame.K_DOWN and y_change == 0:
                x_change, y_change = 0, SNAKE_SIZE

    # Update Snake Position
    x += x_change
    y += y_change

    # Check for collisions
    if x < 0 or x >= PLAY_AREA_WIDTH or y < 50 or y >= SCREEN_HEIGHT:
        game_over()

    # Add new head to the snake
    snake_head = [x, y]
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    # Check self-collision
    for segment in snake_list[:-1]:
        if segment == snake_head:
            game_over()

    # Check if the snake eats food
    if x == food_x and y == food_y:
        score += 1
        snake_length += 1
        food_x = random.randint(0, (PLAY_AREA_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        food_y = random.randint(5, (PLAY_AREA_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE

    # Update the screen
    pygame.display.update()
    clock.tick(FPS)

# Exit Pygame
pygame.quit()
