from pico2d import *
import random

class Plant:
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.image = load_image('plant.png')
        self.creatx, self.creaty = 0, 0
        self.attackcnt = 19

    def creat(self, mousex, mousey):
        self.creatx = int(mousex / 100)
        self.creaty = int(mousey / 100)

        self.x = self.creatx * 100 + 55
        self.y = self.creaty * 100 + 50

    def update(self, frame_time):
        self.frame = (self.frame + 1) % 8
        self.attackcnt += 1

    def draw(self, frame_time):
        self.draw_bb()
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Attack:
    def __init__(self):
        self.x, self.y = 0, 0
        self.image = load_image('attack.png')

    def creat(self, plantx, planty):
        self.x, self.y = plantx + 30, planty + 10

    def update(self, frame_time):
        self.x += 10

    def draw(self, frame_time):
        self.draw_bb()
        self.image.clip_draw(0, 0, 26, 26, self.x, self.y)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Flower:
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.image = load_image('flower.png')
        self.creatx, self.creaty = 0, 0

    def creat(self, mousex, mousey):
        self.creatx = int(mousex / 100)
        self.creaty = int(mousey / 100)

        self.x = self.creatx * 100 + 55
        self.y = self.creaty * 100 + 50

    def update(self, frame_time):
        self.frame = (self.frame + 1) % 8

    def draw(self, frame_time):
        self.draw_bb()
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 25, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

class Walnut:
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.image = load_image('walnut.png')
        self.creatx, self.creaty = 0, 0

    def creat(self, mousex, mousey):
        self.creatx = int(mousex / 100)
        self.creaty = int(mousey / 100)

        self.x = self.creatx * 100 + 55
        self.y = self.creaty * 100 + 50

    def update(self, frame_time):
        self.frame = (self.frame + 1) % 8

    def draw(self, frame_time):
        self.draw_bb()
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

# stage2
class Bomb:
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.image = load_image('bomb.png')
        self.creatx, self.creaty = 0, 0

    def creat(self, mousex, mousey):
        self.creatx = int(mousex / 100)
        self.creaty = int(mousey / 100)

        self.x = self.creatx * 100 + 55
        self.y = self.creaty * 100 + 50

    def update(self, frame_time):
        self.frame = (self.frame + 1) % 4

    def draw(self, frame_time):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_bb(self):
        return self.x - 30, self.y - 10, self.x + 30, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
