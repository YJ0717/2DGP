from pico2d import *
import gfw
from player import CustomPlayer

world = gfw.World(['background', 'player']) #배경 추가,나중에 배경이미지 조정

class Background:
    def __init__(self):
        self.image = gfw.image.load('background.png')
        self.x = 0

    def update(self):
        self.x = -player.x * 0.5  # 배경이 플레이어의 절반 속도로 움직이도록 설정 나중에 조절가능

    def draw(self):
        self.image.draw(self.x, 0)

def enter():
    global player, background
    player = CustomPlayer()
    background = Background()
    world.append(background, world.layer.background)
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

