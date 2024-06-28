import pygame
import random
import json

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Snake properties
snake_block = 20
snake_speed = 15

# Fonts
font = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Initialize clock
clock = pygame.time.Clock()


def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(window, GREEN, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font.render(msg, True, color)
    window.blit(mesg, [width / 6, height / 3])


def draw_scoreboard(score, high_score):
    # Draw scoreboard background
    pygame.draw.rect(window, GRAY, [0, 0, width, 50])

    # Draw current score
    score_text = score_font.render(f"Score: {score}", True, BLACK)
    window.blit(score_text, [10, 10])

    # Draw high score
    high_score_text = score_font.render(f"High Score: {high_score}", True, BLACK)
    window.blit(high_score_text, [width - 200, 10])


def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file)


def show_leaderboard():
    leaderboard = load_leaderboard()
    leaderboard.sort(key=lambda x: x["score"], reverse=True)

    window.fill(BLACK)
    title = font.render("Leaderboard", True, WHITE)
    window.blit(title, [width / 3, 20])

    y = 100
    for i, entry in enumerate(leaderboard[:5], 1):
        text = score_font.render(f"{i}. {entry['name']}: {entry['score']}", True, WHITE)
        window.blit(text, [width / 3, y])
        y += 40

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(50, height - snake_block) / snake_block) * snake_block

    score = 0
    high_score = max([entry["score"] for entry in load_leaderboard()] + [0])

    while not game_over:
        while game_close:
            window.fill(BLACK)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            draw_scoreboard(score, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 50:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        window.fill(BLACK)
        pygame.draw.rect(window, RED, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        draw_scoreboard(score, high_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(50, height - snake_block) / snake_block) * snake_block
            length_of_snake += 1
            score += 10
            if score > high_score:
                high_score = score

        clock.tick(snake_speed)

    # Game over, add score to leaderboard
    name = input("Enter your name: ")
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    save_leaderboard(leaderboard)

    show_leaderboard()

    pygame.quit()
    quit()


game_loop()