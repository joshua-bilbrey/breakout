"""Contains level and block data for Breakout Game."""

BLUE = 177/255, 188/255, 230/255


class LevelManager:
    def __init__(self):
        self.levels = {}

    def create_levels(self):

        # LEVEL 1
        level_1 = {}
        row = 0
        for num in range(36):
            if not num % 9:
                row += 1
            level_1.update({num: {'position': (((num % 9) * 110) + 10, (row * 35) + 600), 'value': 1, 'color': BLUE}})
        self.levels.update(level_1=level_1)


level_manager = LevelManager()
level_manager.create_levels()
