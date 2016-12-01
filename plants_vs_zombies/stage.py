from pico2d import *
import random

class Stage:
    def __init__(self):
        self.stage1_image = load_image('resource/stage1.png')
        self.stage2_image = load_image('resource/stage2.png')
        self.stage3_image = load_image('resource/stage3.png')
        self.select_image = load_image('resource/select_plant.png')
        self.font = load_font('resource/ConsolaMalgun.ttf', 17)
        self.state = 'stage1'
        self.zombie_cnt, self.random_cnt = 0, 10

    def update(self):
        self.zombie_cnt += 1

    def draw(self, select_plant, sun_point):
        if self.state == 'stage1':
            self.stage1_image.draw(700, 300)
        elif self.state == 'stage2':
            self.stage2_image.draw(700, 300)
        elif self.state == 'stage3':
            self.stage3_image.draw(700, 300)
        self.select_image.clip_draw((select_plant - 1) * 100 + 10, 0, 100, 100, 1350, 545)
        self.font.draw(20, 504, '%d' % sun_point)

    def zombie_set_count(self):
        if self.state == 'stage1':
            self.random_cnt = random.randint(250, 300)
        elif self.state == 'stage2':
            self.random_cnt = random.randint(200, 250)
        elif self.state == 'stage3':
            self.random_cnt = random.randint(150, 200)
        self.zombie_cnt = 0

    def cnt_init(self):
        self.zombie_cnt, self.random_cnt = 0, 10