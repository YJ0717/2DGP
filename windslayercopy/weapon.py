from pico2d import *
import gfw
import config
import gfw.image as image

class Weapon:
    # ======================무기를 장착한 스프리트 가져오기======================   
    # ======================무기 애니메이션을 캐릭터 움직임에 따라 동기화 해야되기 때문에 player.py의 행동함수를 가져옴======================
    def __init__(self, walk_left_image_file='weapon_walk.png', idle_image_file='weapon_idle.png', dash_image_file='weapon_dash.png', jump_image_file='weapon_jump.png', double_jump_image_file='weapon_jump2.png'):
        self.load_images(walk_left_image_file, idle_image_file, dash_image_file, jump_image_file, double_jump_image_file)
        self.init_attributes()

    def load_images(self, walk_left_image_file, idle_image_file, dash_image_file, jump_image_file, double_jump_image_file):
        self.walk_left_image = image.load(walk_left_image_file)
        self.idle_image = image.load(idle_image_file)
        self.dash_image = image.load(dash_image_file)
        self.jump_image = image.load(jump_image_file)
        self.double_jump_image = image.load(double_jump_image_file)

    def init_attributes(self):
        self.current_image = self.idle_image
        self.frame = 0
        self.time = 0
        self.frame_width = config.IDLE_FRAME_WIDTH
        self.frame_height = config.IDLE_FRAME_HEIGHT

    def update(self, player):
        self.time += gfw.frame_time
        if player.is_dashing:
            self.update_dash(player)
        elif player.is_jumping:
            self.update_jump(player)
        else:
            self.update_movement(player)

    def update_dash(self, player):
        self.current_image = self.dash_image
        self.frame_width = config.WEAPON_DASH_FRAME_WIDTH
        self.frame_height = config.WEAPON_DASH_FRAME_HEIGHT
        fps = config.WEAPON_DASH_FPS
        frame_count = config.WEAPON_DASH_FRAME_COUNT
        self.frame = round(self.time * fps) % frame_count

    def update_movement(self, player):
        if player.dx != 0:
            self.current_image = self.walk_left_image
            self.frame_width = config.WEAPON_WALK_FRAME_WIDTH
            self.frame_height = config.WEAPON_WALK_FRAME_HEIGHT
            fps = config.WEAPON_WALK_FPS
            frame_count = config.WEAPON_WALK_FRAME_COUNT
        else:
            self.current_image = self.idle_image
            self.frame_width = config.WEAPON_IDLE_FRAME_WIDTH
            self.frame_height = config.WEAPON_IDLE_FRAME_HEIGHT
            fps = config.WEAPON_IDLE_FPS
            frame_count = config.WEAPON_IDLE_FRAME_COUNT

        self.frame = round(self.time * fps) % frame_count

    def update_jump(self, player):
        if player.can_double_jump:
            self.current_image = self.jump_image
            self.frame_width = config.WEAPON_JUMP_FRAME_WIDTH
            self.frame_height = config.WEAPON_JUMP_FRAME_HEIGHT
            fps = config.WEAPON_JUMP_FPS
            frame_count = config.WEAPON_JUMP_FRAME_COUNT
            self.frame = round(self.time * fps) % frame_count
        else:
            # 더블 점프 애니메이션
            self.current_image = self.double_jump_image
            self.frame_width = config.WEAPON_DOUBLE_JUMP_FRAME_WIDTH
            self.frame_height = config.WEAPON_DOUBLE_JUMP_FRAME_HEIGHT
            fps = config.WEAPON_DOUBLE_JUMP_FPS
            frame_count = config.WEAPON_DOUBLE_JUMP_FRAME_COUNT
            self.frame = round(self.time * fps) % frame_count
            
            if self.frame == 0 and self.time > 0:   #------ 더블 점프중 남는 프레임이 다음 더블점프에 영향을줌 -> 초기화 시켜야 됨--------------------------------
                self.time = 0

    def draw(self, x, y, flip='h'):
       
        x_offset = self.frame * self.frame_width
        self.current_image.clip_composite_draw(
            x_offset, 0, self.frame_width, self.frame_height,
            0, flip, x, y,
            self.frame_width, self.frame_height
        ) 