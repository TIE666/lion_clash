import random
from actions import ACTIONS

class RandomHunterAgent:
    def get_action(self, hunter_pos, lion_pos, sheep_pos):
        # Example logic: Move randomly using action strings
        return random.choice(ACTIONS)

class HunterAgent(RandomHunterAgent):
    def __init__(self):
        super().__init__()