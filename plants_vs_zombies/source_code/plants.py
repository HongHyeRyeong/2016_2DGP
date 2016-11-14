from pico2d import *
import random

PIXEL_PER_METER = (10.0 / 0.5)  # 10 pixel 50 cm
RUN_SPEED_KMPH = 25.0  # Km / Hour 속도
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class Plant:
    def __init__(self):
        self.image = load_image('plant.png')
        self.x, self.y = 0, 0
        self.frame, self.total_frames = 0.0, 0.0
        self.attackcnt = 0

    def creat(self, mousex, mousey):
        self.x = int(mousex / 100) * 100 + 55
        self.y = int(mousey / 100) * 100 + 50

    def update(self, frame_time):
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 8

        self.attackcnt += 1

    def draw(self, frame_time):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Attack:
    def __init__(self):
        self.image = load_image('attack.png')
        self.x, self.y = 0, 0

    def creat(self, plantx, planty):
        self.x, self.y = plantx + 30, planty + 10

    def update(self, frame_time):
        distance = RUN_SPEED_PPS * frame_time
        self.x += distance

    def draw(self, frame_time):
        self.image.clip_draw(0, 0, 26, 26, self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Flower:
    def __init__(self):
        self.image = load_image('flower.png')
        self.x, self.y = 0, 0
        self.frame, self.total_frames = 0.0, 0.0
        self.suncnt = 0

    def creat(self, mousex, mousey):
        self.x = int(mousex / 100) * 100 + 55
        self.y = int(mousey / 100) * 100 + 50

    def update(self, frame_time):
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 8

        self.suncnt += 1

    def draw(self, frame_time):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 25, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Sun:
    FRAMES_PER_ACTION = 2

    def __init__(self):
        self.image = load_image('sun.png')
        self.x, self.y = random.randint(100, 1000), random.randint(100, 500)
        self.frame, self.total_frames = 0.0, 0.0

    def update(self, frame_time):
        self.total_frames += Sun.FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 2

    def draw(self, frame_time):
        self.image.clip_draw(int(self.frame * 100), 0, 100, 100, self.x, self.y)

class Walnut:
    def __init__(self):
        self.image = load_image('walnut.png')
        self.x, self.y = 0, 0
        self.frame, self.total_frames = 0.0, 0.0
        self.life = 1

    def creat(self, mousex, mousey):
        self.x = int(mousex / 100) * 100 + 55
        self.y = int(mousey / 100) * 100 + 50

    def update(self, frame_time):
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 8

    def draw(self, frame_time):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())