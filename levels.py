"""Contains level and block data for Breakout Game."""

BLUE = 177/255, 188/255, 230/255
LIGHT_BLUE = 183/255, 229/255, 221/255
PURPLE = 154/255, 134/255, 164/255


class LevelManager:
    def __init__(self):
        self.levels = {}

    def create_levels(self):

        # LEVEL 0 (TEST LEVEL)
        level_0 = {0: {'position': (450, 600), 'value': 5, 'color': PURPLE}}
        self.levels.update(level_0=level_0)

        # LEVEL 1
        level_1 = {}
        row = 0
        for num in range(36):
            if not num % 9:
                row += 1
            level_1.update({num: {'position': (((num % 9) * 110) + 10, (row * 35) + 565), 'value': 1, 'color': BLUE}})
        self.levels.update(level_1=level_1)

        # LEVEL 2
        level_2 = {}
        num = 0
        for row in range(7):
            row_num = 0
            if row == 0 or row == 6:
                for _ in range(3):
                    level_2.update(
                        {num: {'position': (((row_num % 9) * 110) + 340, (row * 35) + 495),
                               'value': 1,
                               'color': LIGHT_BLUE}}
                    )
                    num += 1
                    row_num += 1
            elif row == 1 or row == 5:
                for _ in range(5):
                    level_2.update(
                        {num: {'position': (((row_num % 9) * 110) + 230, (row * 35) + 495), 'value': 1, 'color': LIGHT_BLUE}}
                    )
                    num += 1
                    row_num += 1
            elif row == 2 or row == 4:
                for _ in range(7):
                    level_2.update(
                        {num: {'position': (((row_num % 9) * 110) + 120, (row * 35) + 495),
                               'value': 1,
                               'color': BLUE}}
                    )
                    num += 1
                    row_num += 1
            elif row == 3:
                for _ in range(9):
                    level_2.update(
                        {num: {'position': (((row_num % 9) * 110) + 10, (row * 35) + 495),
                               'value': 1,
                               'color': PURPLE}}
                    )
                    num += 1
                    row_num += 1
        self.levels.update(level_2=level_2)


level_manager = LevelManager()
level_manager.create_levels()
