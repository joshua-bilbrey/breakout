"""Contains level and block data for Breakout Game."""
import math

BLUE = 177/255, 188/255, 230/255
LIGHT_BLUE = 183/255, 229/255, 221/255
PURPLE = 154/255, 134/255, 164/255

BLOCK_COORDS = [(((num % 9) * 110) + 10, (math.floor(num / 9) * 35) + 400) for num in range(90)]
BLOCK_ROWS = {f'row{row}': BLOCK_COORDS[row * 9: (row + 1) * 9] for row in range(math.ceil(len(BLOCK_COORDS) / 9))}


class LevelManager:
    def __init__(self):
        self.levels = {}

    def create_levels(self):

        # LEVEL 0 (TEST LEVEL)
        level_0 = {}
        for block_coord in BLOCK_COORDS:
            level_0.update({BLOCK_COORDS.index(block_coord): {'position': block_coord, 'value': 5, 'color': PURPLE}})
        # num = 0
        # for row in BLOCK_ROWS:
        #     for coord in BLOCK_ROWS[row]:
        #         level_0.update({num: {'position': coord, 'value': 1, 'color': PURPLE}})
        #         num += 1
        self.levels.update(level_0=level_0)

        # LEVEL 1
        level_1 = {}
        num = 0
        for row in BLOCK_ROWS:
            if row in ['row6', 'row7', 'row8', 'row9']:
                for coord in BLOCK_ROWS[row]:
                    level_1.update({num: {'position': coord, 'value': 1, 'color': BLUE}})
                    num += 1

        self.levels.update(level_1=level_1)

        # LEVEL 2
        level_2 = {}

        num = 0
        for row in BLOCK_ROWS:
            if row in ['row9', 'row3']:
                for coord in BLOCK_ROWS[row][3:6]:
                    level_2.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                    num += 1

        for row in BLOCK_ROWS:
            if row in ['row8', 'row4']:
                for coord in BLOCK_ROWS[row][2:7]:
                    level_2.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                    num += 1

        for row in BLOCK_ROWS:
            if row in ['row7', 'row5']:
                for coord in BLOCK_ROWS[row][1:8]:
                    level_2.update({num: {'position': coord, 'value': 1, 'color': BLUE}})
                    num += 1

        for coord in BLOCK_ROWS['row6']:
            level_2.update({num: {'position': coord, 'value': 1, 'color': PURPLE}})
            num += 1

        self.levels.update(level_2=level_2)

        # LEVEL 3
        level_3 = {}

        num = 0
        for row in BLOCK_ROWS:
            if row in ['row1', 'row3', 'row5', 'row7', 'row9']:
                for coord in BLOCK_ROWS[row]:
                    level_3.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                    num += 1

        for row in BLOCK_ROWS:
            if row in ['row2', 'row4', 'row6', 'row8']:
                for coord in BLOCK_ROWS[row]:
                    if BLOCK_ROWS[row].index(coord) % 2:
                        level_3.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                        num += 1

        self.levels.update(level_3=level_3)

        # LEVEL 4
        level_4 = {}

        num = 0
        for row in BLOCK_ROWS:
            if row in ['row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8']:
                for coord in BLOCK_ROWS[row]:
                    if BLOCK_ROWS[row].index(coord) == 0 or BLOCK_ROWS[row].index(coord) == 8:
                        level_4.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                        num += 1

        for row in BLOCK_ROWS:
            if row in ['row1', 'row9']:
                for coord in BLOCK_ROWS[row]:
                    level_4.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                    num += 1

        for row in BLOCK_ROWS:
            if row in ['row4', 'row6']:
                for coord in BLOCK_ROWS[row][3:6]:
                    level_4.update({num: {'position': coord, 'value': 1, 'color': PURPLE}})
                    num += 1

        for coord in BLOCK_ROWS['row5']:
            if BLOCK_ROWS['row5'].index(coord) == 3 or BLOCK_ROWS['row5'].index(coord) == 5:
                level_4.update({num: {'position': coord, 'value': 1, 'color': PURPLE}})
                num += 1
            elif BLOCK_ROWS['row5'].index(coord) == 4:
                level_4.update({num: {'position': coord, 'value': 1, 'color': BLUE}})
                num += 1

        self.levels.update(level_4=level_4)


level_manager = LevelManager()
level_manager.create_levels()
