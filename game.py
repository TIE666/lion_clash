import pygame
import random
import sys
from actions import ACTIONS, DIRECTIONS
from hunter_agent import HunterAgent
from lion_agent import LionAgent
from sheep_agent import SheepAgent

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)

# Emojis
LION_EMOJI = '🦁'
HUNTER_EMOJI = '🏹'
SHEEP_EMOJI = '🐑'

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lion Clash")
font = pygame.font.Font('./NotoEmoji-Regular.ttf', CELL_SIZE)

class GameState:
    def __init__(self):
        self.lion_pos = [0, 0]
        self.hunter_pos = [GRID_SIZE - 1, GRID_SIZE - 1]  # Single hunter
        self.sheep_pos = [
            [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
            for _ in range(5)
        ]
        self.score = 0
        self.proximity_range = 1  # Proximity range around the hunter

    def draw_cell(self, emoji, position):
        text = font.render(emoji, True, (0, 0, 0))
        rect = text.get_rect(center=((position[1] + 0.5) * CELL_SIZE, (position[0] + 0.5) * CELL_SIZE))
        screen.blit(text, rect)

    def draw(self, remaining_time=None):
        screen.fill(WHITE)

        # Highlight the proximity range around the hunter in red
        for dx in range(-self.proximity_range, self.proximity_range + 1):
            for dy in range(-self.proximity_range, self.proximity_range + 1):
                x, y = self.hunter_pos[0] + dx, self.hunter_pos[1] + dy
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                    rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, (255, 0, 0), rect)

        # Draw sheep
        for sheep in self.sheep_pos:
            self.draw_cell(SHEEP_EMOJI, sheep)

        # Draw lion
        self.draw_cell(LION_EMOJI, self.lion_pos)

        # Draw hunter
        self.draw_cell(HUNTER_EMOJI, self.hunter_pos)

        # Draw remaining time if provided
        if remaining_time is not None:
            timer_font = pygame.font.SysFont('arial', 20)
            timer_text = timer_font.render(f"Time Left: {remaining_time}s", True, (0, 0, 0))
            screen.blit(timer_text, (10, 10))

        pygame.display.flip()

    def move_agent(self, agent, action):
        if action not in DIRECTIONS or action == "STAY":
            return agent  # No movement
        dx, dy = DIRECTIONS[action]
        x, y = agent
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            return [new_x, new_y]
        return agent

    def is_lion_caught(self):
        # Check if the lion is within the proximity range of the hunter
        if abs(self.lion_pos[0] - self.hunter_pos[0]) <= self.proximity_range and abs(self.lion_pos[1] - self.hunter_pos[1]) <= self.proximity_range:
            return True
        return False

    def remove_eaten_sheep(self):
        # Check if the lion's position matches any sheep's position
        if self.lion_pos in self.sheep_pos:
            self.sheep_pos.remove(self.lion_pos)
            self.score += 10

    def update(self, lion_action, hunter_action, sheep_actions):
        # Move the lion
        self.lion_pos = self.move_agent(self.lion_pos, lion_action)

        # Move the hunter
        self.hunter_pos = self.move_agent(self.hunter_pos, hunter_action)

        # Move the sheep
        self.sheep_pos = [self.move_agent(pos, act) for pos, act in zip(self.sheep_pos, sheep_actions)]

        # Draw the updated state before checking game-over conditions
        self.draw()

        # Remove eaten sheep after all movements
        self.remove_eaten_sheep()
        
        # Check if the lion is caught by the hunter
        if self.is_lion_caught():
            self.show_game_over_screen("Lion was caught by the hunter!")

        # Check if all the sheep are gone
        if not self.sheep_pos:
            self.show_game_over_screen("Lion ate all the sheep!")

    def show_game_over_screen(self, message):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)  # Set transparency (0 = fully transparent, 255 = fully opaque)
        overlay.fill((255, 255, 255))  # White background for the overlay
        screen.blit(overlay, (0, 0))

        # Display the game-over message
        game_over_font = pygame.font.SysFont('arial', 30)
        message_text = game_over_font.render(message, True, (255, 0, 0))  # Red text for visibility
        score_text = game_over_font.render(f"Score: {self.score}", True, (0, 0, 0))

        # Center the text on the screen
        screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        # Wait for a click or quit event
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

# Main game loop
def main():
    clock = pygame.time.Clock()
    game = GameState()
    lion_agent = LionAgent()
    hunter_agent = HunterAgent()
    sheep_agents = [SheepAgent() for _ in game.sheep_pos]

    game_duration = 20  # Game duration in seconds
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = max(0, game_duration - elapsed_time)
        if remaining_time == 0:
            game.show_game_over_screen("Time's up!")
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.show_game_over_screen("Game Over!")
                running = False

        lion_move = lion_agent.get_action(game.lion_pos, game.hunter_pos, game.sheep_pos)
        hunter_move = hunter_agent.get_action(game.hunter_pos, game.lion_pos)
        sheep_moves = [
            agent.get_action(sheep_pos, game.lion_pos)
            for agent, sheep_pos in zip(sheep_agents, game.sheep_pos)
        ]
        game.update(lion_move, hunter_move, sheep_moves)
        game.draw(remaining_time)

        clock.tick(5)  # 5 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
