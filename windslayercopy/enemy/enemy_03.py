from pico2d import *
import gfw
import gfw.image as image
import enemy.enemy_config as enemy_config
from enemy.enemy_01 import Enemy_01
import time

class Enemy_03(Enemy_01):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.load_enemy03_images()
        self.init_enemy03_attributes()
        self.roll_speed = enemy_config.ENEMY_03_ROLL_SPEED
        self.target_x = x

    def load_enemy03_images(self):
        self.idle_image = image.load('enemy03_idle.png')
        self.walk_image = image.load('enemy03_walk.png')
        self.attack_image = image.load('enemy03_attack.png')
        self.hit_image = image.load('enemy03_hit.png')
        self.dead_image = image.load('enemy03_dead.png')
        self.current_image = self.idle_image

    def init_enemy03_attributes(self):
        self.hp = enemy_config.ENEMY_03_HP
        self.max_hp = enemy_config.ENEMY_03_HP
        self.attack_power = enemy_config.ENEMY_03_ATTACK_POWER
        self.defense = enemy_config.ENEMY_03_DEFENSE
        self.speed = enemy_config.ENEMY_03_WALK_SPEED
        
        self.animations = {
            Enemy_01.IDLE: {'frame_count': 4, 'fps': enemy_config.ENEMY_03_IDLE_FPS, 'width': 65, 'height': 67},
            Enemy_01.WALK: {'frame_count': 6, 'fps': enemy_config.ENEMY_03_WALK_FPS, 'width': 80, 'height': 72},
            Enemy_01.ATTACK: {'frame_count': 4, 'fps': enemy_config.ENEMY_03_ATTACK_FPS, 'width': 65, 'height': 61},
            Enemy_01.HIT: {'frame_count': 3, 'fps': enemy_config.ENEMY_03_HIT_FPS, 'width': 74, 'height': 71},
            Enemy_01.DEAD: {'frame_count': 3, 'fps': enemy_config.ENEMY_03_DEAD_FPS, 'width': 100, 'height': 100}
        }

        self.detect_range = enemy_config.ENEMY_03_DETECT_RANGE
        self.attack_range = enemy_config.ENEMY_03_ATTACK_RANGE
        self.attack_cooldown = enemy_config.ENEMY_03_ATTACK_COOLDOWN 

    def update(self):
        #====================== 구르는 몬스터 설정 ===============================
        if self.state == Enemy_01.ATTACK:
            move_distance = self.roll_speed * gfw.frame_time
            self.x += self.direction * move_distance

            # ===========돌진 거리===========
            if self.time >= 10:  
                self.state = Enemy_01.IDLE
                self.time = 0
    
        super().update()

#===================== 주인공 추격 기능 도입========================
    def chase_player(self, player):
        if self.state == Enemy_01.ATTACK:
            return
        
        current_time = time.time()
        distance = player.x - self.x
        
        if abs(distance) < self.detect_range:
            self.direction = 1 if distance > 0 else -1
            
            if abs(distance) < self.attack_range and current_time - self.last_attack_time > self.attack_cooldown:
                self.target_player = player  
                self.start_attack()
                self.last_attack_time = current_time
            else:
                self.state = Enemy_01.WALK
                self.dx = self.direction * self.speed
        else:
            self.state = Enemy_01.IDLE
            self.dx = 0
#===================== 공격 시작 기능 도입========================
    def start_attack(self):
        if self.state != Enemy_01.ATTACK:
            self.state = Enemy_01.ATTACK
            self.time = 0
            self.current_image = self.attack_image
            if hasattr(self, 'target_player'):
                self.direction = 1 if self.target_player.x > self.x else -1
