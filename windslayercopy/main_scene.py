from pico2d import *
import gfw
from player import CustomPlayer
from Map.stage_1 import get_tile_map  #테스트

world = gfw.World(['background', 'tile', 'player'])  

class Background:
    def __init__(self):
        self.image = gfw.image.load('background.png')
        self.x = 0

    def update(self):
        global player  
        self.x = -player.x * 0.5  # 플레이어 움직임에 따라 이동

    def draw(self):
        self.image.draw_to_origin(self.x, 0, 3000, 720)  

class TileMap:
    def __init__(self, tile_images, tile_map_data, tile_size):
        self.tile_images = tile_images
        self.tile_map_data = tile_map_data
        self.tile_size = tile_size
        self.x_offset = 0  

    def update(self):
        self.x_offset = -player.x

    def draw(self):
        for y in range(len(self.tile_map_data)):
            row = self.tile_map_data[y]
            for x in range(len(row)):
                tile_index = row[x]
                if tile_index >= 0:
                    tile_image = self.tile_images[tile_index]
                    tile_image.draw(x * self.tile_size + self.tile_size // 2 + self.x_offset, y * self.tile_size + self.tile_size // 2)

def enter():
    global player, background, tile_map
    player = CustomPlayer()
    background = Background()
    tile_images, tile_map_data = get_tile_map()
    tile_map = TileMap(tile_images, tile_map_data, 32)
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

