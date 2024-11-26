from pico2d import *
import gfw
from player import CustomPlayer

world = gfw.World(['background', 'tile', 'player'])

def enter():
    global player, tile_map
    player = CustomPlayer()
    tile_images, tile_map_data = get_tile_map()
    tile_map = TileMap(tile_images, tile_map_data, 32, player)
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

def get_tile_map():
    tile_images = [
        gfw.image.load('tile0.png'),  
        gfw.image.load('tile1.png')   
    ]

    # 타일맵 데이터 설정
    tile_map_data = [
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    ]

    return tile_images, tile_map_data

class TileMap:
    def __init__(self, tile_images, tile_map_data, tile_size, player):
        self.tile_images = tile_images
        self.tile_map_data = tile_map_data
        self.tile_size = tile_size
        self.player = player

    def update(self):
        pass

    def draw(self):
        pass
