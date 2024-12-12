from pico2d import *
import gfw

class GameClearImage:
    def __init__(self):
        self.image = gfw.image.load('game_clear.png')
        self.layer_index = 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()

    def update(self):
        pass

    def draw(self):
        self.image.draw_to_origin(0, 0, self.canvas_width, self.canvas_height)

def enter():
    global world
    world = gfw.World()
    clear_image = GameClearImage()
    world.append(clear_image)

def update():
    world.update()

def draw():
    clear_canvas()
    world.draw()
    update_canvas()

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    return True

def exit():
    pass

def pause():
    pass

def resume():
    pass 