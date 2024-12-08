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
        #========================================== 깜빡거림 관련 속성 추가 ==========================================
        self.invincible = False
        self.invincible_time = 0
        self.invincible_duration = 0.5  
        self.blink_interval = 0.1  
        self.visible = True  
        
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
            Enemy_01.IDLE: {'frame_count': 2, 'fps': enemy_config.ENEMY_01_IDLE_FPS, 'width': 100, 'height': 100},
            Enemy_01.WALK: {'frame_count': 5, 'fps': enemy_config.ENEMY_01_WALK_FPS, 'width': 100, 'height': 100},
            Enemy_01.ATTACK: {'frame_count': 3, 'fps': enemy_config.ENEMY_01_ATTACK_FPS, 'width': 165, 'height': 100},
            Enemy_01.HIT: {'frame_count': 2, 'fps': enemy_config.ENEMY_01_HIT_FPS, 'width': 100, 'height': 100},
            Enemy_01.DEAD: {'frame_count': 3, 'fps': enemy_config.ENEMY_01_DEAD_FPS, 'width': 100, 'height': 100}
        }
        
        self.detect_range = enemy_config.ENEMY_01_DETECT_RANGE
        self.attack_range = enemy_config.ENEMY_01_ATTACK_RANGE
        self.last_attack_time = 0
        self.attack_cooldown = enemy_config.ENEMY_01_ATTACK_COOLDOWN
        
        self.last_damage = 0  # 마지막으로 받은 데미지
        self.damage_display_time = 0  # 데미지 표시 시간
        
        #========================================== 죽었을 때 or 맞았을 때 객체 처리 ==========================================
    def update(self):
        self.time += gfw.frame_time
        
        # 무미지 표시 시간 업데이트
        if self.damage_display_time > 0:
            self.damage_display_time -= gfw.frame_time
        
        # 죽은 상태일 때 처리
        if self.state == Enemy_01.DEAD:
            anim = self.animations[Enemy_01.DEAD]
            self.frame = int(self.time * anim['fps']) % anim['frame_count']
            if self.time >= (anim['frame_count'] / anim['fps']):
                self.is_dead = True
                world = gfw.top().world
                world.remove(self, world.layer.enemy)
            return
        
        # 무적 시간 처리
        if self.invincible:
            self.invincible_time += gfw.frame_time
            if self.invincible_time % self.blink_interval < self.blink_interval / 2:
                self.visible = False
            else:
                self.visible = True
            if self.invincible_time >= self.invincible_duration:
                self.invincible = False
                self.visible = True
        
        # 피격 상태일 때 처리
        if self.state == Enemy_01.HIT:
            if self.time >= 0.5:
                self.state = Enemy_01.IDLE
                self.time = 0
        
        self.update_animation()
        self.update_ai()
        self.apply_gravity()

        player = self.get_player()
        if player:
            self.check_collision_with_player(player)
        
    def update_animation(self):
        anim = self.animations[self.state]
        fps = anim['fps']
        frame_count = anim['frame_count']
        self.frame = int(self.time * fps) % frame_count
        
    def update_ai(self):
        if self.is_dead:
            self.state = Enemy_01.DEAD
            self.current_image = self.dead_image
            return
            
        player = self.get_player()
        if player is None:
            return
            
    #========================== 몬스터가 플레이어를 탐지 x,y모두 감지되어야 추격 ====================    
        world = gfw.top().world
        x_offset = -world.objects[world.layer.player][0].x
        player_world_x = player.x - x_offset
        player_world_y = player.y  # 플레이어의 y 좌표
        
        distance_x = abs(self.x - player_world_x)
        distance_y = abs(self.y - player_world_y)
        
        y_detect_range = 300
        
        if self.state == Enemy_01.HIT:
            self.current_image = self.hit_image
            return
            
        if distance_x <= self.attack_range and distance_y <= y_detect_range:
            self.handle_attack(player)
        elif distance_x <= self.detect_range and distance_y <= y_detect_range:
            self.handle_chase(player_world_x)
        else:
            self.handle_idle()
            
    def handle_attack(self, player):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.state = Enemy_01.ATTACK
            self.current_image = self.attack_image
            self.last_attack_time = current_time
            
    def handle_chase(self, player_world_x):
        self.state = Enemy_01.WALK
        self.current_image = self.walk_image
        self.direction = 1 if player_world_x > self.x else -1
        self.dx = self.direction * self.speed * gfw.frame_time
        self.x += self.dx
        
    def handle_idle(self):
        self.state = Enemy_01.IDLE
        self.current_image = self.idle_image
        self.dx = 0
        
    def get_player(self): 
        world = gfw.top().world  
        for obj in world.objects[world.layer.player]:
            return obj
        return None
        
    def draw(self):
        if self.is_dead:
            return
        
        if not self.visible and self.state != Enemy_01.DEAD:
            return
        
        anim = self.animations[self.state]
        frame_width = anim['width']
        frame_height = anim['height']
        
        world = gfw.top().world
        x_offset = -world.objects[world.layer.player][0].x
        y_offset = world.objects[world.layer.player][0].y - get_canvas_height() // 2
        
        screen_x = self.x + x_offset
        screen_y = self.y - y_offset
        
        if self.direction > 0:
            self.current_image.clip_composite_draw(
                self.frame * frame_width, 0, frame_width, frame_height,
                0, 'h', screen_x, screen_y,
                frame_width, frame_height
            )
        else:
            self.current_image.clip_draw(
                self.frame * frame_width, 0, frame_width, frame_height,
                screen_x, screen_y
            )
        
        if not self.state == Enemy_01.DEAD:
            draw_rectangle(
                screen_x - frame_width // 2, screen_y - frame_height // 2,
                screen_x + frame_width // 2, screen_y + frame_height // 2
            )
            
            # ============================= HP 바 그리기 =============================
            hp_bar_width = 50
            hp_bar_height = 5
            hp_bar_y = screen_y + frame_height // 2 + 10
            
            draw_rectangle(
                screen_x - hp_bar_width // 2, hp_bar_y - hp_bar_height // 2,
                screen_x + hp_bar_width // 2, hp_bar_y + hp_bar_height // 2
            )
            
            # 현재 HP 바 (빨간색)
            current_hp_width = (hp_bar_width * self.hp) // self.max_hp
            if current_hp_width > 0:
                hp_bar = image.load('hp_bar.png')  
                hp_bar.draw_to_origin(
                    screen_x - hp_bar_width // 2, 
                    hp_bar_y - hp_bar_height // 2,
                    current_hp_width, 
                    hp_bar_height
                )
            
            # 데미지 숫자 표시
            if self.damage_display_time > 0:
                x = screen_x
                y = screen_y + frame_height // 2 + 40
                
                numbers_image = image.load('number_red.png')
                damage_str = str(self.last_damage)
                number_width = 40
                number_height = 59
                text_width = len(damage_str) * number_width
                
                for i, num in enumerate(damage_str):
                    numbers_image.clip_draw(
                        int(num) * number_width, 0,
                        number_width, number_height,
                        x - text_width//2 + i*number_width,
                        y,
                        number_width, number_height//2
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
        if self.is_dead or self.invincible:
            return
            
        actual_damage = max(0, damage - self.defense)
        self.hp -= actual_damage
        self.last_damage = actual_damage
        self.damage_display_time = 1.0
        self.invincible = True
        self.invincible_time = 0
        
        if self.hp <= 0:
            self.hp = 0  
            self.state = Enemy_01.DEAD
            self.time = 0
            self.current_image = self.dead_image
            self.frame = 0 
        else:
            self.state = Enemy_01.HIT
            self.time = 0

    def apply_gravity(self):
        self.velocity_y = getattr(self, 'velocity_y', 0)
        self.velocity_y += enemy_config.ENEMY_01_GRAVITY
        self.y += self.velocity_y
# ====================================== 적 캐릭터의 bb를 계산하는 함수 ===============  
    def get_bounding_box(self):
        screen_x, screen_y = self.get_screen_position()
        anim = self.animations[self.state]
        half_width = anim['width'] // 2
        half_height = anim['height'] // 2
        return (screen_x - half_width, screen_y - half_height, screen_x + half_width, screen_y + half_height)
#========================== 적 캐릭터의 화면 좌표 계산 ========================
    def get_screen_position(self):
        world = gfw.top().world
        x_offset = -world.objects[world.layer.player][0].x
        y_offset = world.objects[world.layer.player][0].y - get_canvas_height() // 2
        
        screen_x = self.x + x_offset
        screen_y = self.y - y_offset
        return screen_x, screen_y
#========================== 적 캐릭터와 플레이어 충돌 체크 ========================
    def check_collision_with_player(self, player):
        if player.is_hit or player.invincible:
            return False
            
        if self.collide(player):
            self.handle_player_collision(player)
            return True
        return False
#========================== 두 객체간의 충돌처리 검사 aabb  ========================
    def collide(self, other):
        left_a, bottom_a, right_a, top_a = self.get_bounding_box()
        
        left_b, bottom_b, right_b, top_b = other.get_bounding_box()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True
#========================== 플레이어와 몬스터가  충돌 했을때의 처리 담당 ========================
    def handle_player_collision(self, player):
        if not player.is_hit and not player.invincible:
            player.is_hit = True
            player.hit_time = 0
            if self.state == Enemy_01.ATTACK:
                player.hp -= self.attack_power
            else:
                player.hp -= self.attack_power // 2  
