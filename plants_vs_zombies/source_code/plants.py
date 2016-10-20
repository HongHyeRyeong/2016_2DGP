from pico2d import *
import random

class Plant:
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.image = load_image('plant.png')
        self.creatx, self.creaty = 0, 0
        self.attackcnt = 20

    def creat(self, mousex, mousey):
        self.creatx = int(mousex / 100)
        self.creaty = int(mousey / 100)

        self.x = self.creatx * 100 + 55
        self.y = self.creaty * 100 + 50

    def update(self, frame_time):
        self.frame = (self.frame + 1) % 8
        self.attackcnt += 1

    def draw(self, frame_time):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

class Attack:
    def __init__(self):
        self.x, self.y = 0, 0
        self.image = load_image('attack.png')

    def creat(self, plantx, planty):
        self.x, self.y = plantx + 30, planty + 10

    def update(self, frame_time):
        self.x += 10

    def draw(self, frame_time):
        self.image.clip_draw(0, 0, 26, 26, self.x, self.y)

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
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

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
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

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
