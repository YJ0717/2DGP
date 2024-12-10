from pico2d import *
import gfw
from player import CustomPlayer
import config
from enemy.enemy_01 import Enemy_01
from Map.stage_2 import TileMap, get_tile_map

world = gfw.World(['background', 'tile', 'enemy', 'player'])

#================ 임시 스테이이지 3생성 ===============================

class Background:
    def __init__(self):
        self.image = gfw.image.load('background.png')
        self.x = 0
        self.y = 0

    def update(self):
        global player
        self.x = -player.x * 0.5
        self.y = -player.y * 0.1

    def draw(self):
        self.image.draw_to_origin(self.x, self.y, 3000, 1250)

def enter():
    global player, background, tile_map
    player = CustomPlayer(equip_weapon=True)
    player.x = config.PLAYER_START_X
    player.y = config.PLAYER_START_Y
    
    background = Background()
    tile_images, tile_map_data = get_tile_map()
    tile_map = TileMap(tile_images, tile_map_data, 32, player)
    
    world.append(background, world.layer.background)
    world.append(tile_map, world.layer.tile)
    world.append(player, world.layer.player)

def update():
    world.update()

def draw():
    world.draw()

def handle_event(e):
    player.handle_event(e)

def exit():
    world.clear()

if __name__ == '__main__':
    gfw.start_main_module()