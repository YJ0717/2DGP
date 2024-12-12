from pico2d import *
import gfw
import config

world = gfw.World(['game_over'])

class GameOver:
    def __init__(self):
        self.image = gfw.image.load('game_over.png')
    
    def draw(self):
        self.image.draw_to_origin(0, 0, get_canvas_width(), get_canvas_height())
    
    def update(self):
        pass

def enter():
    global game_over
    game_over = GameOver()
    world.append(game_over, world.layer.game_over)

def update():
    world.update()

def draw():
    world.draw()

def handle_event(e):
    return False

def exit():
    world.clear()

def pause():
    pass

def resume():
    pass