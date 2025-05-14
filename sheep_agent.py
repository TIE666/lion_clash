import random
from actions import ACTIONS

class RandomSheepAgent:
    def __init__(self, proximity_range=2):
        self.proximity_range = proximity_range  # Proximity range for sheep to detect the lion

    def get_action(self, sheep_pos, lion_pos):
        # Calculate the Manhattan distance between the sheep and the lion
        distance = abs(sheep_pos[0] - lion_pos[0]) + abs(sheep_pos[1] - lion_pos[1])
        if distance <= self.proximity_range:
            # Move randomly if the lion is within proximity
            return random.choice(ACTIONS)
        # Stay in place if the lion is not within proximity
        return "STAY"

class SheepAgent(RandomSheepAgent):
    def __init__(self):
        super().__init__()