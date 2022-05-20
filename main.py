from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.config import Config
from time import time, sleep
from levels import LevelManager, BLUE

level_manager = LevelManager()
level_manager.create_levels()


# TODO 2: Block Class
class Block(Widget):
    def __init__(self, color=BLUE, value=1, **kwargs):
        self.color = color
        self.value = value
        super(Block, self).__init__(**kwargs)


# TODO 3: Paddle Class
class Paddle(Widget):
    lives = NumericProperty(3)
    score = NumericProperty(0)
    time_since_bounce = time()

    def bounce_ball(self, ball):
        # TODO 3.9: Made paddle change direction of ball
        if self.collide_widget(ball) and (time() - self.time_since_bounce > 0.1) and ball.velocity != [0, 0]:
            x = min(abs(self.x - ball.right), abs(self.right - ball.x))
            y = abs(self.top - ball.y)
            if y <= x:
                direction = (ball.center_x - self.center_x) / 75
                ball.velocity_x = direction * 3
                if ball.velocity_y >= 0:
                    ball.velocity_y = (25 - (ball.velocity_x ** 2)) ** (1 / 2) * -1
                else:
                    ball.velocity_y = (25 - (ball.velocity_x ** 2)) ** (1 / 2)
                print(f'Speed: {(ball.velocity_x ** 2 + ball.velocity_y ** 2) ** (1 / 2)}')
            else:
                ball.velocity_x *= -1
            self.time_since_bounce = time()


# TODO 3.5: Ball Class
class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


# TODO 1: Kivy Screen creation
class BreakoutGame(Widget):
    ball = ObjectProperty(None)
    paddle = ObjectProperty(None)
    current_level = 1
    time_since_bounce_x = time()
    time_since_bounce_y = time()
    update_game = None

    def reset_ball(self):
        self.paddle.center_x = self.center_x
        self.ball.center_x = self.center_x
        self.ball.y = self.paddle.top
        self.ball.velocity = (0, 0)

    def serve_ball(self, vel=(3, 4)):
        self.ball.velocity = vel

    def create_blocks(self):
        level_dict = level_manager.levels[f'level_{self.current_level}']
        for block in level_dict:
            new_block = Block(pos=level_dict[block]['position'],
                              color=level_dict[block]['color'],
                              value=level_dict[block]['value'])
            self.add_widget(new_block)

    def start_game(self):
        self.update_game = Clock.schedule_interval(self.update, 1/60)

    def score(self, block):
        value = block.value
        self.paddle.score += value

    def update(self, dt):
        self.ball.move()

        # TODO 3.75: Code wall bounce and paddle bounce
        # bounce off blocks
        for wid in self.walk():
            if isinstance(wid, Block):
                if self.ball.collide_widget(wid):
                    x = min(abs(wid.x - self.ball.right), abs(wid.right - self.ball.x))
                    y = min(abs(wid.y - self.ball.top), abs(wid.top - self.ball.y))
                    if x <= y and time() - self.time_since_bounce_x > 0.1:
                        self.ball.velocity_x *= -1
                        self.time_since_bounce_x = time()
                        self.score(wid)
                        self.remove_widget(wid)
                    if y <= x and time() - self.time_since_bounce_y > 0.1:
                        self.ball.velocity_y *= -1
                        self.time_since_bounce_y = time()
                        # TODO 3.875: Blocks disappear when hit
                        self.score(wid)
                        self.remove_widget(wid)

        # bounce off paddle
        self.paddle.bounce_ball(self.ball)

        # bounce off top and sides
        if self.ball.top > self.height:
            self.ball.velocity_y *= -1
        if self.ball.x < 0 or self.ball.right > self.width:
            self.ball.velocity_x *= -1

        # TODO 5: Print lives and scores to screen
        # lose life
        if self.ball.y <= self.y:
            self.paddle.lives -= 1
            self.reset_ball()

        # end game if lives hit zero
        if self.paddle.lives == 0:
            self.end_game()

    def on_touch_move(self, touch):
        self.paddle.center_x = touch.x

        # serve ball if needed
        if self.ball.velocity == [0, 0]:
            self.serve_ball()

    def end_game(self):
        self.update_game.cancel()


class BreakoutApp(App):
    def build(self):
        game = BreakoutGame()
        print(game.ball.velocity)
        game.create_blocks()
        game.start_game()
        return game


# TODO 4: Scoring System

# TODO 5.5: Fix ending game, maybe buttons to go to main menu or play again?

# TODO 6: Create various levels

# TODO: 7: A kv file for main menu too

Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 800)
Config.set('graphics', 'resizable', False)

if __name__ == "__main__":
    BreakoutApp().run()
