from pico2d import *
import gfw
from player import CustomPlayer
from Map.stage_1 import get_tile_map, TileMap  

world = gfw.World(['background', 'tile', 'player'])  

class Background:
    def __init__(self):
        self.image = gfw.image.load('background.png')
        self.x = 0
        self.y = 0

    def update(self):
        global player  
        self.x = -player.x * 0.5  # 플레이어 움직임에 따라 x 이동
        self.y = -player.y * 0.1  # 플레이어 점프에 따라 y 이동

    def draw(self):
        self.image.draw_to_origin(self.x, self.y, 3000, 1250)  
#==========================================stage 1 도입==========================================
def enter():
    global player, background, tile_map
    player = CustomPlayer()
    background = Background()
    tile_images, tile_map_data = get_tile_map()
    tile_map = TileMap(tile_images, tile_map_data, 32, player)
    world.append(background, world.layer.background)
    world.append(tile_map, world.layer.tile)  
    world.append(player, world.layer.player)  

def exit():
    world.clear()

def handle_event(e):
    player.handle_event(e)

def update():
    world.update()

def draw():
    world.draw()

if __name__ == '__main__':
    gfw.start_main_module()

