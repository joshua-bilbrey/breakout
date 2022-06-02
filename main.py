import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button
from time import time
import pickle
from levels import LevelManager, BLUE

level_manager = LevelManager()
level_manager.create_levels()


def _on_resize(self, width, height):
    Window.size = (1000, 800)
    return True


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
            base_velocity_sqr = ball.velocity_x ** 2 + ball.velocity_y ** 2
            if y <= x:
                direction = (ball.center_x - self.center_x) / 75
                ball.velocity_x = direction * 3
                if ball.velocity_y >= 0:
                    ball.velocity_y = (base_velocity_sqr - (ball.velocity_x ** 2)) ** (1 / 2) * -1
                else:
                    ball.velocity_y = (base_velocity_sqr - (ball.velocity_x ** 2)) ** (1 / 2)
                print(f'Speed: {base_velocity_sqr ** (1/2)}')
            else:
                ball.velocity_x *= -1
            self.time_since_bounce = time()

    def move(self, direction=1, movement_speed=20):
        self.center_x += (direction * movement_speed)


# TODO 3.5: Ball Class
class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    speed_modifier = 1

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


# TODO 1: Kivy Screen creation
class BreakoutGame(Widget):
    ball = ObjectProperty(None)
    paddle = ObjectProperty(None)
    current_level = 1
    high_score = NumericProperty(0)
    time_since_bounce_x = time()
    time_since_bounce_y = time()
    update_game = None
    game_on = True

    def __init__(self, **kwargs):
        super(BreakoutGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def on_touch_move(self, touch):
        if not self.paddle.disabled and self.game_on:
            self.paddle.center_x = touch.x

            # serve ball if needed
            if self.ball.velocity == [0, 0]:
                self.serve_ball()

    def on_touch_down(self, touch):
        if self.paddle.disabled and self.game_on:
            self.paddle.disabled = False
        return super(BreakoutGame, self).on_touch_down(touch)

    # TODO 8: Add control for paddle with keys
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not self.paddle.disabled and self.game_on:
            if keycode[1] == 'right':
                self.paddle.move()
            elif keycode[1] == 'left':
                self.paddle.move(direction=-1)

            # serve ball if needed
            if self.ball.velocity == [0, 0]:
                self.serve_ball()
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if self.paddle.disabled:
            if keycode[1] == 'right' or keycode[1] == 'left':
                self.paddle.disabled = False
        return True

    def return_to_menu(self, on_touch_down=None, touch=None):
        self.parent.manager.current = 'start_screen'

    def get_high_score(self):
        try:
            with open('score.dat', 'rb') as file:
                self.high_score = pickle.load(file)
            print(f'opened file - high score {self.high_score}')
        except FileNotFoundError:
            self.high_score = 0
            print(f'{self.high_score}')

    def set_high_score(self):
        self.high_score = self.paddle.score
        with open('score.dat', 'wb') as file:
            pickle.dump(self.high_score, file)
            print(f'new high score {self.high_score}')

    def reset_ball(self):
        self.paddle.center_x = self.center_x
        self.ball.center_x = self.center_x
        self.ball.y = self.paddle.top
        self.ball.velocity = (0, 0)

    def serve_ball(self, vel=(3, 4)):
        self.ball.velocity = (vel[0] * self.ball.speed_modifier, vel[1] * self.ball.speed_modifier)

    # TODO 6: Create various levels
    def create_blocks(self):
        level_dict = level_manager.levels[f'level_{self.current_level}']
        for block in level_dict:
            new_block = Block(pos=level_dict[block]['position'],
                              color=level_dict[block]['color'],
                              value=level_dict[block]['value'])
            self.add_widget(new_block)

    def start_game(self, on_touch_down=None, touch=None):
        self.current_level = 0
        self.game_on = True
        self.paddle.lives = 3
        self.paddle.score = 0
        # clear blocks
        for wid in self.walk():
            if isinstance(wid, Block) or isinstance(wid, Button):
                self.remove_widget(wid)
        self.create_blocks()
        self.update_game = Clock.schedule_interval(self.update, 1/90)

    def score(self, block):
        value = block.value
        self.paddle.score += value

    def end_game(self):
        self.update_game.cancel()

    def update(self, dt):
        self.ball.move()

        # TODO 3.75: Code wall bounce and paddle bounce
        # bounce off blocks
        no_blocks = True
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
                no_blocks = False

        # bounce off paddle
        self.paddle.bounce_ball(self.ball)

        # bounce off top and sides
        if self.ball.top > 750:
            self.ball.velocity_y *= -1
        if self.ball.x < 0 or self.ball.right > self.width:
            self.ball.velocity_x *= -1

        # TODO 5: Print lives and scores to screen
        # lose life
        if self.ball.y <= self.y:
            self.paddle.lives -= 1
            self.reset_ball()
            self.paddle.disabled = True

        # start next level
        if no_blocks:
            self.reset_ball()
            self.current_level += 1
            self.ball.speed_modifier *= 1.05
            self.create_blocks()

        # end game if lives hit zero
        if self.paddle.lives == 0:
            self.end_game()
            if self.high_score < self.paddle.score:
                self.set_high_score()
            self.game_on = False
            # TODO 5.5: Fix ending game, maybe buttons to go to main menu or play again?
            retry_button = Button(text='Try Again?', size=(100, 30), pos=(450, 375), on_press=self.start_game)
            quit_button = Button(text='Quit to Menu', size=(100, 30), pos=(450, 315), on_press=self.return_to_menu)
            self.add_widget(retry_button)
            self.add_widget(quit_button)


class StartScreen(Screen):
    Window.size = (1000, 800)
    Window.bind(on_resize=_on_resize)


class GameScreen(Screen):
    Window.bind(on_resize=_on_resize)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = BreakoutGame()
        self.add_widget(self.game)

    def on_pre_enter(self, *args):
        self.game.start_game()
        self.game.get_high_score()


class BreakoutApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        # TODO: 7: A kv file for main menu too
        sm.add_widget(StartScreen(name='start_screen'))
        sm.add_widget(GameScreen(name='game_screen'))
        return sm


# TODO 4: Scoring System

# TODO 7.5: Increase speed or difficulty?

if __name__ == "__main__":
    BreakoutApp().run()
