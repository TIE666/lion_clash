import random
from actions import ACTIONS

class RandomLionAgent:
    def get_action(self, lion_pos, hunter_pos, sheep_positions):
        # Example logic: Move randomly using action strings
        return random.choice(ACTIONS)

class LionAgent(RandomLionAgent):
    def __init__(self):
        super().__init__()