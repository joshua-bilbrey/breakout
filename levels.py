"""Contains level and block data for Breakout Game."""
import math
import random

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
        # level_0 = {0: {'position': (400, 400), 'value': 1, 'color': BLUE}}
        for block_coord in BLOCK_COORDS:
            level_0.update({BLOCK_COORDS.index(block_coord): {'position': block_coord, 'value': 5, 'color': PURPLE}})

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

        # LEVEL 5
        level_5 = {}

        num = 0
        for color in [BLUE, LIGHT_BLUE, PURPLE]:
            index_1 = 0
            index_2 = 8
            row_num = 9
            if color == LIGHT_BLUE:
                index_1, index_2 = 1, 7
            if color == BLUE:
                row_num = 8
            while True:
                level_5.update({num: {'position': BLOCK_ROWS[f'row{row_num}'][index_1], 'value': 1, 'color': color}})
                num += 1
                level_5.update({num: {'position': BLOCK_ROWS[f'row{row_num}'][index_2], 'value': 1, 'color': color}})
                num += 1
                index_1 += 1
                index_2 -= 1
                row_num -= 1
                if index_1 == index_2:
                    level_5.update({num: {'position': BLOCK_ROWS[f'row{row_num}'][index_1], 'value': 1, 'color': color}})
                    num += 1
                    break

        self.levels.update(level_5=level_5)

        # LEVEL 6
        level_6 = {}

        num = 0
        for row in BLOCK_ROWS:
            if row in ['row3', 'row4', 'row5', 'row6', 'row7']:
                for coord in BLOCK_ROWS[row]:
                    if BLOCK_ROWS[row].index(coord) in [0, 2, 4, 6, 8]:
                        level_6.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                        num += 1

        for coord in BLOCK_ROWS['row2']:
            if BLOCK_ROWS['row2'].index(coord) in [0, 4, 8]:
                level_6.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                num += 1

        for coord in BLOCK_ROWS['row8']:
            if BLOCK_ROWS['row8'].index(coord) in [0, 2, 6, 8]:
                level_6.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                num += 1

        for row in BLOCK_ROWS:
            if row in ['row1', 'row9']:
                for coord in BLOCK_ROWS[row]:
                    level_6.update({num: {'position': coord, 'value': 1, 'color': LIGHT_BLUE}})
                    num += 1

        self.levels.update(level_6=level_6)

        # LEVEL 7
        level_7 = {}

        num = 0
        row_num = 0
        colors = [BLUE, PURPLE, LIGHT_BLUE, PURPLE, BLUE]
        for row in BLOCK_ROWS:
            if row in ['row1', 'row3', 'row5', 'row7', 'row9']:
                for coord in BLOCK_ROWS[row]:
                    level_7.update({num: {'position': coord, 'value': 1, 'color': colors[row_num]}})
                    num += 1
                row_num += 1

        self.levels.update(level_7=level_7)

        # LEVEL 8
        level_8 = {}

        num = 0
        for row in BLOCK_ROWS:
            if row in ['row2', 'row9']:
                for coord in BLOCK_ROWS[row][2:7]:
                    level_8.update({num: {'position': coord, 'value': 1, 'color': BLUE}})
                    num += 1

        for row in BLOCK_ROWS:
            if row in ['row3', 'row5', 'row6']:
                for coord in BLOCK_ROWS[row]:
                    if BLOCK_ROWS[row].index(coord) in [0, 2, 3, 4, 5, 6, 8]:
                        level_8.update({num: {'position': coord, 'value': 1, 'color': BLUE}})
                        num += 1

        for coord in BLOCK_ROWS['row7']:
            level_8.update({num: {'position': coord, 'value': 1, 'color': BLUE}})
            num += 1

        for coord in BLOCK_ROWS['row8'][2:7]:
            if BLOCK_ROWS['row8'].index(coord) in [3, 5]:
                level_8.update({num: {'position': coord, 'value': 1, 'color': PURPLE}})
                num += 1
            else:
                level_8.update({num: {'position': coord, 'value': 1, 'color': BLUE}})
                num += 1

        for coord in BLOCK_ROWS['row4']:
            if BLOCK_ROWS['row4'].index(coord) in [3, 4, 5]:
                level_8.update({num: {'position': coord, 'value': 1, 'color': PURPLE}})
                num += 1
            if BLOCK_ROWS['row4'].index(coord) in [0, 2, 6, 8]:
                level_8.update({num: {'position': coord, 'value': 1, 'color': BLUE}})
                num += 1

        self.levels.update(level_8=level_8)

        # LEVEL 9
        level_9 = {}

        num = 0
        colors = [BLUE, PURPLE, LIGHT_BLUE]
        for row in BLOCK_ROWS:
            if row in ['row1', 'row9']:
                for coord in BLOCK_ROWS[row][3:6]:
                    level_9.update({num: {'position': coord, 'value': 1, 'color': random.choice(colors)}})
                    num += 1
            if row in ['row2', 'row3', 'row4', 'row5', 'row6', 'row7', 'row8']:
                for coord in BLOCK_ROWS[row][2:7]:
                    level_9.update({num: {'position': coord, 'value': 1, 'color': random.choice(colors)}})
                    num += 1

        self.levels.update(level_9=level_9)

        # Add 10 more levels in as copies in random order
        self.levels.update(level_10=level_0)
        all_levels = [level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8, level_9]
        random.shuffle(all_levels)

        num = 1
        for level in all_levels:
            new_level = {f'level_1{num}': level}
            self.levels.update(new_level)
            num += 1

        # SECRET LEVEL
        secret_level = {}

        num = 0
        for block in range(50):
            x = random.randint(10, 890)
            y = random.randint(400, 720)
            coord = (x, y)
            secret_level.update({num: {'position': coord, 'value': 1, 'color': random.choice(colors)}})
            num += 1

        self.levels.update(level_chaos=secret_level)

        print(self.levels.keys())


level_manager = LevelManager()
level_manager.create_levels()
