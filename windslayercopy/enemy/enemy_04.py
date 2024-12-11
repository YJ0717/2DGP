from pico2d import *
import gfw
import gfw.image as image
import enemy.enemy_config as enemy_config
from enemy.enemy_01 import Enemy_01
import time

class Enemy_04(Enemy_01):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.load_enemy04_images()
        self.init_enemy04_attributes()
        self.target_x = x

    def load_enemy04_images(self):
        self.idle_image = image.load('enemy04_idle.png')
        self.walk_image = image.load('enemy04_walk.png')
        self.attack_image = image.load('enemy04_attack.png')
        self.hit_image = image.load('enemy04_hit.png')
        self.dead_image = image.load('enemy04_dead.png')
        self.current_image = self.idle_image

    def init_enemy04_attributes(self):
        self.hp = enemy_config.ENEMY_04_HP
        self.max_hp = enemy_config.ENEMY_04_HP
        self.attack_power = enemy_config.ENEMY_04_ATTACK_POWER
        self.defense = enemy_config.ENEMY_04_DEFENSE
        self.speed = enemy_config.ENEMY_04_WALK_SPEED
        
        self.animations = {
            Enemy_01.IDLE: {'frame_count': 2, 'fps': enemy_config.ENEMY_04_IDLE_FPS, 'width': 60, 'height': 93},
            Enemy_01.WALK: {'frame_count': 4, 'fps': enemy_config.ENEMY_04_WALK_FPS, 'width': 60, 'height': 93},
            Enemy_01.ATTACK: {'frame_count': 3, 'fps': enemy_config.ENEMY_04_ATTACK_FPS, 'width': 82, 'height': 93},
            Enemy_01.HIT: {'frame_count': 2, 'fps': enemy_config.ENEMY_04_HIT_FPS, 'width': 58, 'height': 96},
            Enemy_01.DEAD: {'frame_count': 3, 'fps': enemy_config.ENEMY_04_DEAD_FPS, 'width': 80, 'height': 94}
        }

        self.detect_range = enemy_config.ENEMY_04_DETECT_RANGE
        self.attack_range = enemy_config.ENEMY_04_ATTACK_RANGE
        self.attack_cooldown = enemy_config.ENEMY_04_ATTACK_COOLDOWN 

    def update(self):
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