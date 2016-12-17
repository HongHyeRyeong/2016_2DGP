from pico2d import *
import random

PIXEL_PER_METER = (10.0 / 0.5)  # 10 pixel 50 cm
RUN_SPEED_KMPH = 25.0  # Km / Hour 속도
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

class Stage:
    def __init__(self):
        self.stage1_image = load_image('resource/stage1.png')
        self.stage2_image = load_image('resource/stage2.png')
        self.stage3_image = load_image('resource/stage3.png')
        self.bar_image = load_image('resource/progress_bar.png')
        self.bar_zombie_image = load_image('resource/zombie_bar.png')
        self.font = load_font('resource/ConsolaMalgun.ttf', 17)
        self.state = 'stage1'
        self.zombie_cnt, self.random_cnt = 0, 10
        self.bar_cnt, self.total_bar_cnt = 0, 0

    def update(self):
        self.zombie_cnt += 1
        self.total_bar_cnt += 1
        if int(self.total_bar_cnt % 50) == 0:
            print(self.bar_cnt)
            self.bar_cnt += 1

    def draw(self, sun_point):
        if self.state == 'stage1':
            self.stage1_image.draw(700, 300)
        elif self.state == 'stage2':
            self.stage2_image.draw(700, 300)
        elif self.state == 'stage3':
            self.stage3_image.draw(700, 300)
        self.font.draw(20, 504, '%d' % sun_point)
        self.bar_image.clip_draw(0, 0, 300, 60, 1230, 50)
        self.bar_image.clip_draw_to_origin(0, 60, 300 - self.bar_cnt, 60, 1080, 21)
        self.bar_zombie_image.clip_draw(0, 0, 57, 57, 1370 - self.bar_cnt, 50)

    def zombie_set_count(self):
        if self.bar_cnt < 50:
            self.random_cnt = random.randint(200, 300)
        else:
            if self.state == 'stage1':
                self.random_cnt = random.randint(100, 110)
            elif self.state == 'stage2':
                self.random_cnt = random.randint(80, 100)
            elif self.state == 'stage3':
                self.random_cnt = random.randint(70, 80)
        self.zombie_cnt = 0

    def cnt_init(self):
        self.zombie_cnt, self.random_cnt = 0, 10
        self.bar_cnt, self.total_bar_cnt = 0, 0

class Item:
    def __init__(self):
        self.select_image = load_image('resource/select_plant.png')
        self.shovel_image = load_image('resource/shovel.png')
        self.shovel_frame, self.shovel_total_frames = 0.0, 0.0

    def update(self, frame_time):
        self.shovel_total_frames += FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time
        self.shovel_frame = int(self.shovel_total_frames + 1) % 2

    def draw(self, select_plant, mouse_x, mouse_y):
        if select_plant == 6:
            self.shovel_image.clip_draw(int(self.shovel_frame * 100), 0, 100, 100, mouse_x, mouse_y)
        else:
            self.select_image.clip_draw((select_plant - 1) * 100 + 10, 0, 100, 100, mouse_x, mouse_y)
        self.select_image.clip_draw((select_plant - 1) * 100 + 10, 0, 100, 100, 1350, 545)

class Game_End:
    def __init__(self):
        self.plant_image = load_image('resource/end_plant.png')
        self.zombie_image = load_image('resource/end_zombie.png')
        self.state = 'play'

    def draw(self):
        if self.state == 'plant':
            self.plant_image.draw(700, 300)
        elif self.state == 'zombie':
            self.zombie_image.draw(700, 300)