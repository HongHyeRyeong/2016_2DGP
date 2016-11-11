from pico2d import *
import random

class Zombie:
    image = None

    def __init__(self):
        self.walk_image = load_image('zom_walk.png')
        self.dead_image = load_image('zom_die.png')
        self.x, self.y = 1400, (random.randint(0, 4)*100)+60
        self.walk_frame = random.randint(0, 5)
        self.state = 0

    def update(self, frame_time):
        self.walk_frame = (self.walk_frame + 1) % 8
        self.x -= 10

    def draw(self, frame_time):
        self.walk_image.clip_draw(self.walk_frame*150, 0, 130, 130, self.x, self.y)