from pico2d import *  
import gfw  
import config  

class Player:
    def __init__(self, walk_left_image_file='walk.png', walk_right_image_file='walk2.png', idle_image_file='idle.png'):
        self.walk_left_image = gfw.image.load(walk_left_image_file)  
        self.walk_right_image = gfw.image.load(walk_right_image_file)  
        self.idle_image = gfw.image.load(idle_image_file)  
        self.current_image = self.idle_image  
        self.time = 0  
        self.frame = 0  
        self.x, self.y = 100, 100  
        self.dx, self.dy = 0, 0  
        self.speed = 200  
        self.action = 0  
        self.frame_width = config.IDLE_FRAME_WIDTH  
        self.frame_height = config.IDLE_FRAME_HEIGHT  

    def update(self):
        self.time += gfw.frame_time  
        if self.dx != 0 or self.dy != 0:  
            fps = 10  
            frame_count = 4  
            if self.dx > 0:
                self.current_image = self.walk_right_image  
                self.frame_width = config.WALK_RIGHT_FRAME_WIDTH  
                self.frame_height = config.WALK_RIGHT_FRAME_HEIGHT  
            else:
                self.current_image = self.walk_left_image  
                self.frame_width = config.WALK_FRAME_WIDTH  
                self.frame_height = config.WALK_FRAME_HEIGHT  
        else:  
            fps = 2  
            frame_count = 2  
            self.current_image = self.idle_image  
            self.frame_width = config.IDLE_FRAME_WIDTH  
            self.frame_height = config.IDLE_FRAME_HEIGHT 

        self.frame = round(self.time * fps) % frame_count  # 프레임 계산
        self.x += self.dx * self.speed * gfw.frame_time  # x 위치 업데이트
        self.y += self.dy * self.speed * gfw.frame_time  # y 위치 업데이트

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:  
            if e.key == SDLK_LEFT:  
                self.dx = -1  
            elif e.key == SDLK_RIGHT:  
                self.dx = 1  
            elif e.key == SDLK_UP:  
                self.dy = 1  
            elif e.key == SDLK_DOWN:  
                self.dy = -1  
        elif e.type == SDL_KEYUP:  
            if e.key == SDLK_LEFT and self.dx < 0:  
                self.dx = 0  
            elif e.key == SDLK_RIGHT and self.dx > 0:  
                self.dx = 0  
            elif e.key == SDLK_UP and self.dy > 0:  
                self.dy = 0  
            elif e.key == SDLK_DOWN and self.dy < 0:  
                self.dy = 0  

    def draw(self):
        x = self.frame * self.frame_width  
        y = self.action * self.frame_height  
        self.current_image.clip_draw(x, y, self.frame_width, self.frame_height, self.x, self.y)  

class CustomPlayer(Player):
    def __init__(self, walk_left_image_file='walk.png', walk_right_image_file='walk2.png', idle_image_file='idle.png'):
        super().__init__(walk_left_image_file, walk_right_image_file, idle_image_file)  
        self.current_image = self.idle_image  
        self.dx = 0  
        self.dy = 0  

    def update(self):
        super().update()  

    def draw(self):
        super().draw()  