from pico2d import *
import gfw
import Map.stage_1 as stage_1

class TitleImage:
    def __init__(self):
        self.image = gfw.image.load('title_screen.png')
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
    title_image = TitleImage()
    world.append(title_image)
    
    gfw.init_audio()

def update():
    world.update()

def draw():
    clear_canvas()
    world.draw()
    update_canvas()

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.quit()
        elif e.key == SDLK_RETURN:  
            gfw.change(stage_1)
    return True

def exit():
    pass

def pause():
    pass

def resume():
    pass 