import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Bottle Flip Game")

# Define colors
white = (226, 223, 210)
black = (0, 0, 0)

# Set up the bottle image
bottle_image = pygame.image.load("bottle.png")
bottle_width = 65
bottle_height = 170

# Set up the initial position of the bottle
bottle_x = window_width // 2 - bottle_width // 2
bottle_y = window_height - bottle_height

# Set up the physics variables
gravity = 0.5
velocity = 0

# Set up the jump state
is_jumping = False

# Set up the flip animation variables
flip_angle = 0
flip_speed = 10

# Set up the score
score = 0
counting_score = False

# Set up the clock
clock = pygame.time.Clock()

# Set up the font for the messages
font = pygame.font.SysFont(None, 36)

# Display the instructions message
instruction_message = "Hold SPACEBAR to flip the bottle and land it upright correctly"
instruction_text = font.render(instruction_message, True, black)
instruction_text_rect = instruction_text.get_rect(center=(window_width // 2, window_height // 2))

# Display the start message
start_message = "Press ENTER to start"
start_text = font.render(start_message, True, black)
start_text_rect = start_text.get_rect(center=(window_width // 2, window_height // 2 + 40))

# Main game loop
running = True
game_started = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_started and event.key == pygame.K_RETURN:
                game_started = True
            elif game_started and event.key == pygame.K_SPACE and not is_jumping:
                velocity = -10
                is_jumping = True
                counting_score = True
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                is_jumping = False

    # Update bottle position and velocity
    velocity += gravity
    bottle_y += velocity

    # Check if the bottle has hit the ground
    if bottle_y >= window_height - bottle_height:
        velocity = 0
        bottle_y = window_height - bottle_height

        # Check if the bottle has landed upright
        if flip_angle == 0 and counting_score:
            score += 1
            counting_score = False

    # Rotate the bottle for flip animation
    if is_jumping:
        flip_angle += flip_speed
        if flip_angle >= 360:
            flip_angle = 0

    # Clear the window
    window.fill(white)

    if not game_started:
        # Display the instructions message
        window.blit(instruction_text, instruction_text_rect)
        # Display the start message
        window.blit(start_text, start_text_rect)
    else:
        # Draw the floor
        floor_color = (160, 160, 160)
        floor_rect = pygame.Rect(0, window_height - 20, window_width, 20)
        pygame.draw.rect(window, floor_color, floor_rect)

        # Rotate the bottle image
        rotated_bottle = pygame.transform.rotate(bottle_image, flip_angle)

        # Draw the bottle
        bottle_rect = rotated_bottle.get_rect(center=(bottle_x + bottle_width // 2, bottle_y + bottle_height // 2))
        window.blit(rotated_bottle, bottle_rect)

        # Draw the score
        score_text = font.render("Score: " + str(score), True, black)
        score_text_rect = score_text.get_rect(topright=(window_width - 10, 10))
        window.blit(score_text, score_text_rect)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
