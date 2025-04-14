import pygame
import random
import sys

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
FOOD_EMOJI = '🍖'

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lion and Hunter Game")
font = pygame.font.Font('./NotoEmoji-Regular.ttf', CELL_SIZE)

class GameState:
    def __init__(self):
        self.lion_pos = [0, 0]
        self.hunter_pos = [[GRID_SIZE - 1, GRID_SIZE - 1]]
        self.food_pos = [
            [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
            for _ in range(5)
        ]
        self.score = 0
        self.proximity_range = 1  # Proximity range around the hunter

    def draw_cell(self, emoji, position):
        text = font.render(emoji, True, (0, 0, 0))
        rect = text.get_rect(center=((position[1]+0.5)*CELL_SIZE, (position[0]+0.5)*CELL_SIZE))
        screen.blit(text, rect)

    def draw(self):
        screen.fill(WHITE)

        # Highlight the proximity range around each hunter in red
        for hunter in self.hunter_pos:
            for dx in range(-self.proximity_range, self.proximity_range + 1):
                for dy in range(-self.proximity_range, self.proximity_range + 1):
                    x, y = hunter[0] + dx, hunter[1] + dy
                    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                        rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, (255, 0, 0), rect)

        # Draw food
        for food in self.food_pos:
            self.draw_cell(FOOD_EMOJI, food)

        # Draw lion
        self.draw_cell(LION_EMOJI, self.lion_pos)

        # Draw hunters
        for hunter in self.hunter_pos:
            self.draw_cell(HUNTER_EMOJI, hunter)

        pygame.display.flip()

    def move_agent(self, agent, direction):
        x, y = agent
        dx, dy = direction
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            return [new_x, new_y]
        return agent

    def is_lion_caught(self):
        for hunter in self.hunter_pos:
            # Check if the lion is within the proximity range in both x and y directions
            if abs(self.lion_pos[0] - hunter[0]) <= self.proximity_range and abs(self.lion_pos[1] - hunter[1]) <= self.proximity_range:
                return True
        return False

    def update(self, lion_action, hunter_actions):
        # Move the lion
        self.lion_pos = self.move_agent(self.lion_pos, lion_action)
        if self.lion_pos in self.food_pos:
            self.food_pos.remove(self.lion_pos)
            self.score += 10

        # Move the hunters
        self.hunter_pos = [self.move_agent(pos, act) for pos, act in zip(self.hunter_pos, hunter_actions)]

        # Draw the updated state before checking game-over conditions
        self.draw()

        # Check if the lion is caught by the hunter or within proximity
        if self.is_lion_caught():
            self.show_game_over_screen("Lion was caught by the hunter!")

        # Check if all the food is gone
        if not self.food_pos:
            self.show_game_over_screen("Lion ate all the food!")

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

# Agents
class RandomLionAgent:
    def get_action(self):
        return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

class RandomHunterAgent:
    def get_action(self):
        return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

# Main game loop
def main():
    clock = pygame.time.Clock()
    game = GameState()
    lion_agent = RandomLionAgent()
    hunter_agents = [RandomHunterAgent() for _ in game.hunter_pos]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.show_game_over_screen("Game Over!")
                running = False

        lion_move = lion_agent.get_action()
        hunter_moves = [agent.get_action() for agent in hunter_agents]
        game.update(lion_move, hunter_moves)

        clock.tick(5)  # 5 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
