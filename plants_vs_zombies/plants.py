from pico2d import *
import random
import time

PIXEL_PER_METER = (10.0 / 0.5)  # 10 pixel 50 cm
RUN_SPEED_KMPH = 25.0  # Km / Hour 속도
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class Plant:
    def __init__(self, mouse_x, mouse_y):
        self.image = load_image('resource/plant.png')
        self.x, self.y = int(mouse_x / 100) * 100 + 55, int(mouse_y / 100) * 100 + 50
        self.frame, self.total_frames = 0.0, 0.0
        self.check_time, self.attack_time = time.time(), 0

    def update(self, frame_time):
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 8

        if self.check_time + 1 < time.time():
            self.check_time = time.time()
            self.attack_time += 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Attack:
    def __init__(self, plant_x, plant_y):
        self.image = load_image('resource/attack.png')
        self.x, self.y = plant_x + 30, plant_y + 10

    def update(self, frame_time):
        distance = RUN_SPEED_PPS * frame_time
        self.x += distance

    def draw(self):
        self.image.clip_draw(0, 0, 26, 26, self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Flower:
    def __init__(self, mouse_x, mouse_y):
        self.image = load_image('resource/flower.png')
        self.x, self.y = int(mouse_x / 100) * 100 + 55, int(mouse_y / 100) * 100 + 50
        self.frame, self.total_frames = 0.0, 0.0
        self.check_time, self.sun_time = time.time(), 0

    def update(self, frame_time):
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 8

        if self.check_time + 1 < time.time():
            self.check_time = time.time()
            self.sun_time += 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 25, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Sun:
    FRAMES_PER_ACTION = 2

    def __init__(self):
        self.image = load_image('resource/sun.png')
        self.x, self.y = random.randint(100, 1000), random.randint(100, 500)
        self.frame, self.total_frames = 0.0, 0.0

    def update(self, frame_time):
        self.total_frames += Sun.FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 2

    def draw(self):
        self.image.clip_draw(int(self.frame * 100), 0, 100, 100, self.x, self.y)

class Walnut:
    def __init__(self, mouse_x, mouse_y):
        self.image = load_image('resource/walnut.png')
        self.x, self.y = int(mouse_x / 100) * 100 + 55, int(mouse_y / 100) * 100 + 50
        self.frame, self.total_frames = 0.0, 0.0
        self.life = 1

    def update(self, frame_time):
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 8

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

# stage2
class Bomb:
    def __init__(self, mouse_x, mouse_y):
        self.image = load_image('resource/bomb.png')
        self.x, self.y = int(mouse_x / 100) * 100 + 55, int(mouse_y / 100) * 100 + 50
        self.frame, self.total_frames = 0.0, 0.0

    def update(self, frame_time):
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

# stage3
class Snow_Plant:
    def __init__(self, mouse_x, mouse_y):
        self.image = load_image('resource/snow_plant.PNG')
        self.x, self.y = int(mouse_x / 100) * 100 + 55, int(mouse_y / 100) * 100 + 50
        self.frame, self.total_frames = 0.0, 0.0
        self.check_time, self.attack_time = time.time(), 0

    def update(self, frame_time):
        self.total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames + 1) % 8

        if self.check_time + 1 < time.time():
            self.check_time = time.time()
            self.attack_time += 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Snow_Attack:
    def __init__(self, snow_x, snow_y):
        self.image = load_image('resource/snow_attack.png')
        self.x, self.y = snow_x + 30, snow_y + 10

    def update(self, frame_time):
        distance = RUN_SPEED_PPS * frame_time
        self.x += distance

    def draw(self):
        self.image.clip_draw(0, 0, 26, 26, self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())