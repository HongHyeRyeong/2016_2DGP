from pico2d import *
import random

class Zombie:
    PIXEL_PER_METER = (10.0 / 0.15)           # 10 pixel 15 cm
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 6

    RUN_SPEED_KMPH = 1.3                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    attack_time = 0.0
    die_time = 0.0

    WALK, ATTACK, DIE, END = 1, 2, 3, 4

    def __init__(self):
        self.walk_image = load_image('zom_walk.png')
        self.attack_image = load_image('zom_attack.png')
        self.die_image = load_image('zom_die.png')
        self.x, self.y = 1400, (random.randint(0, 4)*100)+60
        self.total_frames = 0.0
        self.walk_frame = random.randint(0, 5)
        self.attack_frame = 0
        self.die_frame = 0
        self.state = self.WALK

    def update(self, frame_time):
        self.total_frames += Zombie.FRAMES_PER_ACTION * Zombie.ACTION_PER_TIME * frame_time

        if self.state == self.WALK:
            self.walk_frame = int(self.total_frames) % 8
            self.x -= 10
        elif self.state == self.ATTACK:
            self.attack_frame = int(self.total_frames) % 5
            self.attack_time += frame_time
            if int(self.attack_time) == 1:
                self.attack_time = 0.0
                self.state = self.WALK
        elif self.state == self.DIE:
            if self.total_frames != 0.0:
                self.total_frames = 0.0
            self.die_frame = int(self.total_frames) % 8
            self.die_time += frame_time
            if int(self.die_time) == 2:
                self.state = self.END

    def draw(self, frame_time):
        if self.state == self.WALK:
            self.walk_image.clip_draw(self.walk_frame*150, 0, 150, 150, self.x, self.y)
        if self.state == self.ATTACK:
            self.attack_image.clip_draw(self.attack_frame*150, 0, 150, 150, self.x, self.y)
        if self.state == self.DIE:
            self.die_image.clip_draw(self.die_frame*200, 0, 200, 200, self.x, self.y)

    def attack(self):
        self.state = self.ATTACK

    def get_bb(self):
        return self.x - 15, self.y - 55, self.x + 35, self.y + 25

    def draw_bb(self):
        draw_rectangle(*self.get_bb())