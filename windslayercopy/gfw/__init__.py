#----------- gfw 모듈 초기화
from gfw.gfw import *
import gfw.image as image
from gfw.image import AnimSprite
from gfw.world import World

bgm = None

def init_audio():
    global bgm
    if bgm is None:  
        bgm = load_music('res/bgm.mp3')
        bgm.set_volume(10)
        bgm.repeat_play()

