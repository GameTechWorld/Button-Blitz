import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Button Blitz")

# Button dimensions
BUTTON_SIZE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
HOVER_GREEN = (0, 200, 0) # Hover color for green buttons

# Font
font = pygame.font.Font(None, 36)

# Game variables
level = 1
time_limit = 30
click_goal = 10
score = 0
button_x = random.randint(0, WIDTH - BUTTON_SIZE)
button_y = random.randint(0, HEIGHT - BUTTON_SIZE)
accomplished = False
game_over = False
game_started = False # Flag to indicate if the game has started
timer_running = False  # Flag to control the timer

# Navigator bar dimensions
NAV_BAR_HEIGHT = 50

# Button dimensions and positions
button_width = 80
button_height = 30
restart_button_text = font.render("Restart", True, WHITE)
restart_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2-50, HEIGHT // 2 + 50, button_width, button_height)
next_button_text = font.render("Next", True, WHITE)
next_button_rect = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 50, button_width, button_height)
start_button_text = font.render("Start", True, WHITE)
start_button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2, button_width, button_height)

# Function to draw text centered on a given x-coordinate
def draw_centered_text(text, x, y, surface, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Game loop
running = True
start_time = 0 # Initialize start_time to 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if not game_started:
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    game_started = True
                    timer_running = True
                    start_time = time.time() # Start the timer when Start is clicked

            # Check button click only if the game has started, is not over, and not accomplished
            if game_started and not game_over and not accomplished:
                if button_x <= mouse_x <= button_x + BUTTON_SIZE and button_y <= mouse_y <= button_y + BUTTON_SIZE:
                    score += 1
                    button_x = random.randint(0, WIDTH - BUTTON_SIZE)
                    button_y = random.randint(0, HEIGHT - BUTTON_SIZE)

            # Check if the restart button was clicked
            if restart_button_rect.collidepoint(mouse_x, mouse_y) and (accomplished or game_over):
                # Reset game variables
                level = 1
                time_limit = 30
                click_goal = 10
                score = 0
                button_x = random.randint(0, WIDTH - BUTTON_SIZE)
                button_y = random.randint(0, HEIGHT - BUTTON_SIZE)
                accomplished = False
                game_over = False
                game_started = False
                timer_running = False 
                start_time = 0 # Reset start_time

            # Check if the next button was clicked
            if next_button_rect.collidepoint(mouse_x, mouse_y) and accomplished:
                # Increase target score, decrease time limit, and increment level
                level += 1 
                click_goal += 2
                time_limit -= 5
                score = 0
                button_x = random.randint(0, WIDTH - BUTTON_SIZE)
                button_y = random.randint(0, HEIGHT - BUTTON_SIZE)
                accomplished = False
                game_started = True # Game continues after Next
                timer_running = True
                start_time = time.time() 

    # Update time only if the timer is running
    if timer_running:
        time_elapsed = time.time() - start_time
        if time_elapsed >= time_limit:
            game_over = True
            timer_running = False

    # Check if the target score is reached
    if game_started and not game_over and score >= click_goal:
        accomplished = True
        timer_running = False

    # Draw background
    screen.fill (WHITE)

    # Draw navigator bar
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, NAV_BAR_HEIGHT))

    # Draw score, target, level, and time in the nav bar, evenly spaced
    label_width = WIDTH // 5  # Divide the width by 5 for even spacing
    draw_centered_text(f"Score: {score}", label_width, NAV_BAR_HEIGHT // 2, screen)
    draw_centered_text(f"Target: {click_goal}", label_width * 2, NAV_BAR_HEIGHT // 2, screen)
    draw_centered_text(f"Level: {level}", label_width * 3, NAV_BAR_HEIGHT // 2, screen)

    # Only draw time if the game has started
    if game_started:
        if timer_running:
            time_elapsed = time.time() - start_time
            draw_centered_text(f"Time: {int(time_limit - time_elapsed)}", label_width * 4, NAV_BAR_HEIGHT // 2, screen)
        else:
            draw_centered_text(f"Time: 0", label_width * 4, NAV_BAR_HEIGHT // 2, screen)

    # Draw buttons
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if accomplished or game_over:
        if restart_button_rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, HOVER_GREEN, restart_button_rect)
        else:
            pygame.draw.rect(screen, GREEN, restart_button_rect)
        screen.blit(restart_button_text, (restart_button_rect.centerx - restart_button_text.get_width() // 2, restart_button_rect.centery - restart_button_text.get_height() // 2))

        if accomplished:
            if next_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, HOVER_GREEN, next_button_rect)
            else:
                pygame.draw.rect(screen, GREEN, next_button_rect)
            screen.blit(next_button_text, (next_button_rect.centerx - next_button_text.get_width() // 2, next_button_rect.centery - next_button_text.get_height() // 2))

    # Draw start button
    if not game_started:
        pygame.draw.rect(screen, GREEN, start_button_rect)
        screen.blit(start_button_text, (start_button_rect.centerx - start_button_text.get_width() // 2, start_button_rect.centery - start_button_text.get_height() // 2))

    # Draw button
    if game_started and not game_over and not accomplished:
        pygame.draw.rect(screen, RED, (button_x, button_y, BUTTON_SIZE, BUTTON_SIZE))

    # Draw text
    if accomplished:
        draw_centered_text("Accomplished!", WIDTH // 2, HEIGHT // 2, screen, GREEN)
    if game_over:
        draw_centered_text("Game Over!", WIDTH // 2, HEIGHT // 2, screen, RED)

    # Update display
    pygame.display.flip()

    # Cap framerate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
