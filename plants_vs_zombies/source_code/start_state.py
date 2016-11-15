import game_framework
import title_state

from pico2d import *

name = "StartState"
image = None
logo_time = 0.0

def enter():
    global image
    open_canvas(1400, 600)
    image = load_image('kpu_credit.png')

def exit():
    global image
    del(image)
    close_canvas()

def update(frame_time):
    global logo_time
    logo_time += frame_time
    if(logo_time > 1.0):
        logo_time = 0
        game_framework.push_state(title_state)

def draw(frame_time):
    global image
    clear_canvas()
    image.draw(700, 300)
    update_canvas()

def handle_events(frame_time):
    events = get_events()

def pause(): pass

def resume(): pass




