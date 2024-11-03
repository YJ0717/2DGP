#----------- 이미지 캐싱,애니메이션 스프라이트
from pico2d import *
import time

_images = {}

def load(file):
    global _images
    if file in _images:
        return _images[file]

    image = load_image('res/' + file)  
    _images[file] = image
    return image

class AnimSprite:
    def __init__(self, filename, x, y, fps, frame_count=0):
        self.image = load(filename)
        self.x, self.y = x, y
        self.fps = fps
        if frame_count == 0:
            frame_count = self.image.w // self.image.h

        self.width = self.image.w // frame_count
        self.frame_count = frame_count
        self.created_on = time.time()

    def draw(self):
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        self.image.clip_draw(index * self.width, 0, self.width, self.image.h, self.x, self.y)  # Fixed height reference
