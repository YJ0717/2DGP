from pico2d import *
import gfw
import gfw.image as image
import config
import time
import random
import enemy.enemy_config as enemy_config

class Enemy_01:
    IDLE, WALK, ATTACK, HIT, DEAD = range(5)   #5개로 상태나뉨

    def __init__(self, x, y):
        self.load_images()
        self.init_attributes(x, y)
        
    def load_images(self):
        self.idle_image = image.load('enemy01_idle.png')
        self.walk_image = image.load('enemy01_walk.png')
        self.attack_image = image.load('enemy01_attack.png')
        self.hit_image = image.load('enemy01_hit.png')
        self.dead_image = image.load('enemy01_dead.png')
        self.current_image = self.idle_image

    def init_attributes(self, x, y):
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.velocity_y = 0
        self.speed = enemy_config.ENEMY_01_WALK_SPEED
        self.direction = 1 
        
        self.state = Enemy_01.IDLE
        self.time = 0
        self.frame = 0
        self.is_dead = False
        
        self.hp = enemy_config.ENEMY_01_HP
        self.max_hp = enemy_config.ENEMY_01_HP
        self.attack_power = enemy_config.ENEMY_01_ATTACK_POWER
        self.defense = enemy_config.ENEMY_01_DEFENSE
        
        self.animations = {
            Enemy_01.IDLE: {'frame_count': 4, 'fps': enemy_config.ENEMY_01_IDLE_FPS, 'width': 100, 'height': 100},
            Enemy_01.WALK: {'frame_count': 6, 'fps': enemy_config.ENEMY_01_WALK_FPS, 'width': 100, 'height': 100},
            Enemy_01.ATTACK: {'frame_count': 6, 'fps': enemy_config.ENEMY_01_ATTACK_FPS, 'width': 120, 'height': 100},
            Enemy_01.HIT: {'frame_count': 3, 'fps': enemy_config.ENEMY_01_HIT_FPS, 'width': 100, 'height': 100},
            Enemy_01.DEAD: {'frame_count': 4, 'fps': enemy_config.ENEMY_01_DEAD_FPS, 'width': 100, 'height': 100}
        }
        
        self.detect_range = enemy_config.ENEMY_01_DETECT_RANGE
        self.attack_range = enemy_config.ENEMY_01_ATTACK_RANGE
        self.last_attack_time = 0
        self.attack_cooldown = enemy_config.ENEMY_01_ATTACK_COOLDOWN
        
    def update(self):
        if self.is_dead:
            return
        
        self.time += gfw.frame_time
        self.update_animation()
        self.update_ai()
        self.apply_gravity()  
        
    def update_animation(self):
        anim = self.animations[self.state]
        fps = anim['fps']
        frame_count = anim['frame_count']
        self.frame = int(self.time * fps) % frame_count
        
    def update_ai(self):
        if self.is_dead:
            self.state = Enemy_01.DEAD
            return
            
        # 플레이어와의 거리 계산
        player = self.get_player()
        if player is None:
            return
            
        # 실제 월드 좌표 기준으로 거리 계산
        world = gfw.top().world
        x_offset = -world.objects[world.layer.player][0].x
        player_world_x = player.x - x_offset  # 플레이어의 실제 월드 좌표
        distance = abs(self.x - player_world_x)
        
        if self.state == Enemy_01.HIT:
            return
            
        if distance <= self.attack_range:
            self.handle_attack(player)
        elif distance <= self.detect_range:
            self.handle_chase(player_world_x)  # 실제 월드 좌표 전달
        else:
            self.handle_idle()
            
    def handle_attack(self, player):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.state = Enemy_01.ATTACK
            self.last_attack_time = current_time
            
    def handle_chase(self, player_world_x):
        self.state = Enemy_01.WALK
        self.direction = 1 if player_world_x > self.x else -1
        self.dx = self.direction * self.speed * gfw.frame_time
        self.x += self.dx  # 실제 월드 좌표 기준으로 이동
        
    def handle_idle(self):
        self.state = Enemy_01.IDLE
        self.dx = 0
        
    def get_player(self):  #플레이어를  찾아 공격 및 추적을 할 수 있는함수
        world = gfw.top().world  
        for obj in world.objects[world.layer.player]:
            return obj
        return None
        
    def draw(self):
        anim = self.animations[self.state]
        frame_width = anim['width']
        frame_height = anim['height']
        
        world = gfw.top().world
        x_offset = -world.objects[world.layer.player][0].x
        y_offset = world.objects[world.layer.player][0].y - get_canvas_height() // 2
        
        screen_x = self.x + x_offset  # x축은 오프셋 적용
        screen_y = self.y - y_offset  # y축도 오프셋 적용하여 상대적 위치 계산
        
        if self.direction > 0:
            self.current_image.clip_composite_draw(
                self.frame * frame_width, 0, frame_width, frame_height,
                0, 'h', screen_x, screen_y,  # screen_y 사용
                frame_width, frame_height
            )
        else:
            self.current_image.clip_draw(
                self.frame * frame_width, 0, frame_width, frame_height,
                screen_x, screen_y  # screen_y 사용
            )
        
    def handle_collision(self, group, other):
        if group == 'player:enemy':
            # 추후 추가 코드
            pass
        elif group == 'tile:enemy':
            if self.velocity_y <= 0:  
                self.velocity_y = 0
                if hasattr(other, 'y'):
                    self.y = other.y + other.height // 2 + self.animations[self.state]['height'] // 2
        
    def get_hit(self, damage):
        if self.is_dead:
            return
            
        self.hp -= max(0, damage - self.defense)
        self.state = Enemy_01.HIT
        self.time = 0  
        
        if self.hp <= 0:
            self.is_dead = True
            self.state = Enemy_01.DEAD
            self.time = 0  

    def apply_gravity(self):
        self.velocity_y = getattr(self, 'velocity_y', 0)
        self.velocity_y += enemy_config.ENEMY_01_GRAVITY
        self.y += self.velocity_y
