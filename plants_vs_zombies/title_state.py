import game_framework
import stage_1
import stage_2
import stage_3
from pico2d import *


name = "TitleState"
image = None

def enter():
    global image
    image = load_image('title.png')

def exit():
    global image
    del(image)

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    game_framework.quit()
                elif event.key == SDLK_SPACE:
                    game_framework.change_state(stage_1)

def draw(frame_time):
    clear_canvas()
    image.draw(700, 300)
    update_canvas()

def update(frame_time):
    pass

def pause():
    pass

def resume():
    pass






