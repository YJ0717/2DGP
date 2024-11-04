from pico2d import *
import gfw
import config
import time

class Player:
    #==========================================기본적인 움직임==========================================
    def __init__(self, walk_left_image_file='walk.png', walk_right_image_file='walk2.png', idle_image_file='idle.png'):
        self.load_images(walk_left_image_file, walk_right_image_file, idle_image_file)
        self.init_attribute()
    #==========================================행동이미지 로드==========================================
    def load_images(self, walk_left_image_file, walk_right_image_file, idle_image_file):
        self.walk_left_image = gfw.image.load(walk_left_image_file)
        self.walk_right_image = gfw.image.load(walk_right_image_file)
        self.idle_image = gfw.image.load(idle_image_file)
        self.dash_image_left = gfw.image.load('dash.png')
        self.jump_image = gfw.image.load('jump.png')
        self.double_jump_image = gfw.image.load('jump2.png')

    def init_attribute(self):
        # --------------------------이미지 관련 수치 설정
        self.current_image = self.idle_image
        
        # --------------------------시간 및 프레임 관련 수치 설정
        self.time = 0
        self.frame = 0
        
        # --------------------------위치 및 이동 관련 수치 설정
        self.x, self.y = config.PLAYER_START_X, config.PLAYER_START_Y
        self.dx, self.dy = 0, 0
        self.speed = config.PLAYER_SPEED
        
        # --------------------------행동 및 애니메이션 관련 수치 설정
        self.action = 0
        self.frame_width = config.IDLE_FRAME_WIDTH
        self.frame_height = config.IDLE_FRAME_HEIGHT
        
        # --------------------------대쉬 관련 수치 설정
        self.is_dashing = False
        self.dash_time = 0
        self.dash_duration = config.DASH_DURATION
        self.dash_speed_multiplier = config.DASH_SPEED_MULTIPLIER
        self.key_press_interval = config.KEY_PRESS_INTERVAL
        self.dash_fps = config.DASH_FPS
        self.dash_frame_count = config.DASH_FRAME_COUNT
        self.last_key_time = 0
        self.dash_frame = 0
        self.dash_frame_sizes = config.DASH_FRAME_SIZES
        self.dash_frame_time = 0
        self.dash_max_time = config.DASH_DURATION
        self.last_direction = None
        self.dash_cooldown = config.PLAYER_DASH_COOLDOWN
        self.last_dash_time = -self.dash_cooldown
        
        # --------------------------점프 관련 수치 설정
        self.is_jumping = False
        self.can_double_jump = False
        self.jump_speed = config.PLAYER_JUMP_SPEED
        self.gravity = config.PLAYER_GRAVITY
        self.velocity_y = 0
        self.start_y = self.y
        self.double_jump_frame = 0
        self.double_jump_fps = config.PLAYER_DOUBLE_JUMP_FPS
        self.double_jump_frame_count = config.PLAYER_DOUBLE_JUMP_FRAME_COUNT
        self.double_jump_time = 0
    #==========================================행동 업데이트==========================================
    def update(self):
        self.time += gfw.frame_time
        if self.is_dashing:
            self.update_dash()
        else:
            self.update_movement()
            self.update_jump()
    #==========================================대쉬 업데이트==========================================
    def update_dash(self):
        self.dash_time += gfw.frame_time
        self.dash_frame_time += gfw.frame_time
        time_per_frame = 1 / config.DASH_FPS

        if self.dash_frame_time >= time_per_frame:
            self.dash_frame = (self.dash_frame + 1) % config.DASH_FRAME_COUNT
            self.dash_frame_time = 0

        if self.dash_time >= config.DASH_DURATION:
            self.is_dashing = False
        else:
            new_x = self.x + self.dx * self.speed * config.DASH_SPEED_MULTIPLIER * gfw.frame_time
            
            #===대쉬 시 캔버스를 벗어나지 않도록 설정하기===
            if 0 <= new_x <= get_canvas_width():
                self.x = new_x
    #==========================================이동 업데이트==========================================
    def update_movement(self):
        if self.dx != 0 or self.dy != 0:
            fps = config.WALK_FPS
            frame_count = 5
            if self.dx > 0:
                self.current_image = self.walk_right_image
                self.frame_width = config.WALK_RIGHT_FRAME_WIDTH
                self.frame_height = config.WALK_RIGHT_FRAME_HEIGHT
            else:
                self.current_image = self.walk_left_image
                self.frame_width = config.WALK_FRAME_WIDTH
                self.frame_height = config.WALK_FRAME_HEIGHT
        else:
            fps = config.IDLE_FPS
            frame_count = 2
            self.current_image = self.idle_image
            self.frame_width = config.IDLE_FRAME_WIDTH
            self.frame_height = config.IDLE_FRAME_HEIGHT

        self.frame = round(self.time * fps) % frame_count

        # =================플레이어의 현재 위치에 따른 캔버스 이동=================
        new_x = self.x + self.dx * self.speed * gfw.frame_time
        new_y = self.y + self.dy * self.speed * gfw.frame_time

        #===플레이어가 캔버스에서 못벗어나게  설정하기===
        if 0 <= new_x <= get_canvas_width():
            self.x = new_x
        if 0 <= new_y <= get_canvas_height():
            self.y = new_y
    #==========================================점프 업데이트==========================================
    def update_jump(self):
        if self.is_jumping:
            self.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.y <= self.start_y:
                self.y = self.start_y
                self.is_jumping = False
                self.can_double_jump = True
                self.double_jump_time = 0
            if not self.can_double_jump:
                self.double_jump_time += gfw.frame_time
                self.double_jump_frame = round(self.double_jump_time * config.DOUBLE_JUMP_FPS) % self.double_jump_frame_count
    #==========================================그리기========================================== 
    def draw(self):
        if self.is_dashing:
            self.draw_dash()
        elif self.is_jumping:
            self.draw_jump()
        else:
            x = self.frame * self.frame_width
            y = self.action * self.frame_height
            self.current_image.clip_draw(x, y, self.frame_width, self.frame_height, self.x, self.y)
    #==========================================대쉬 그리기==========================================
    def draw_dash(self):
        frame_width, frame_height = config.DASH_FRAME_SIZES[self.dash_frame]
        x = self.dash_frame * frame_width
        if self.dx > 0:
            # 오른쪽 대쉬: dash.png를 수평 반전하여 사용
            self.dash_image_left.clip_composite_draw(
                x, 0, frame_width, frame_height,
                0, 'h',  # 'h'는 수평 반전을 의미
                self.x, self.y,
                frame_width, frame_height  # 크기를 명시적으로 지정
            )
        else:
            # 왼쪽 대쉬: dash.png를 그대로 사용
            self.dash_image_left.clip_draw(x, 0, frame_width, frame_height, self.x, self.y)

    def draw_jump(self):
        if not self.can_double_jump:
            x = self.double_jump_frame * config.WALK_FRAME_WIDTH
            flip = ' ' if self.dx < 0 else 'h'
            self.double_jump_image.clip_composite_draw(
                x, 0, config.WALK_FRAME_WIDTH, config.WALK_FRAME_HEIGHT,
                0, flip, self.x, self.y,
                config.WALK_FRAME_WIDTH, config.WALK_FRAME_HEIGHT
            )
        else:
            flip = ' ' if self.dx < 0 else 'h'
            self.jump_image.clip_composite_draw(
                0, 0, config.WALK_FRAME_WIDTH, config.WALK_FRAME_HEIGHT,
                0, flip, self.x, self.y,
                config.WALK_FRAME_WIDTH, config.WALK_FRAME_HEIGHT
            )

    #==========================================키 이벤트==========================================
    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            self.handle_keydown(e)
        elif e.type == SDL_KEYUP:
            self.handle_keyup(e)

    def handle_keydown(self, e):
        current_time = time.time()  # 대쉬를 위한 시간
        if e.key in (SDLK_LEFT, SDLK_RIGHT): #걷는 방향 
            direction = -1 if e.key == SDLK_LEFT else 1
            
            # =================대쉬 조건 =================
            if self.last_direction == direction and current_time - self.last_key_time < self.key_press_interval:
                # 점프 중이 아니고 대쉬 쿨타임이 지났다면 대쉬 시작
                if not self.is_jumping and current_time - self.last_dash_time >= self.dash_cooldown:
                    self.is_dashing = True  
                    self.dash_time = 0  
                    self.last_dash_time = current_time  # 마지막 대쉬 시간기록하기
            
            # =================이동 방향 및 시간 업데이트=================
            self.dx = direction
            self.last_key_time = current_time  # 마지막 키 입력 시간 기록
            self.last_direction = direction  # 마지막 방향 업데이트

        # =================점프 처리=================
        elif e.key == SDLK_UP:
            if not self.is_jumping:
                self.is_jumping = True  
                self.velocity_y = self.jump_speed  
            elif self.can_double_jump:
                self.can_double_jump = False  
                self.velocity_y = self.jump_speed 
                self.double_jump_time = 0  

        # 아래 방향키 입력 처리
        elif e.key == SDLK_DOWN:
            self.dy = -1  #추후 삭제 예정

        # 대쉬 키 입력 처리
        elif e.key == SDLK_LSHIFT:
            if not self.is_jumping:
                self.is_dashing = True  
                self.dash_time = 0  

    def handle_keyup(self, e):
        if e.key == SDLK_LEFT and self.dx < 0:
            self.dx = 0
        elif e.key == SDLK_RIGHT and self.dx > 0:
            self.dx = 0
        elif e.key == SDLK_DOWN and self.dy < 0:
            self.dy = 0

class CustomPlayer(Player):
    def __init__(self, walk_left_image_file='walk.png', walk_right_image_file='walk2.png', idle_image_file='idle.png'):
        super().__init__(walk_left_image_file, walk_right_image_file, idle_image_file)