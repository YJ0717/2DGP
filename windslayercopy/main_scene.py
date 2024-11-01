from pico2d import *
import gfw
from player import CustomPlayer

world = gfw.World(['player'])

def enter():
    global player
    player = CustomPlayer()
    world.append(player, world.layer.player)

def exit():
    world.clear()

def handle_event(e):
    player.handle_event(e)

def update():
    player.update()

def draw():
    player.draw()

if __name__ == '__main__':
    gfw.start_main_module()

