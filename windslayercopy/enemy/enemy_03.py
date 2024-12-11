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
            Enemy_01.IDLE: {'frame_count': 3, 'fps': enemy_config.ENEMY_03_IDLE_FPS, 'width': 100, 'height': 100},
            Enemy_01.WALK: {'frame_count': 3, 'fps': enemy_config.ENEMY_03_WALK_FPS, 'width': 100, 'height': 100},
            Enemy_01.ATTACK: {'frame_count': 3, 'fps': enemy_config.ENEMY_03_ATTACK_FPS, 'width': 165, 'height': 100},
            Enemy_01.HIT: {'frame_count': 2, 'fps': enemy_config.ENEMY_03_HIT_FPS, 'width': 100, 'height': 100},
            Enemy_01.DEAD: {'frame_count': 3, 'fps': enemy_config.ENEMY_03_DEAD_FPS, 'width': 100, 'height': 100}
        }

        self.detect_range = enemy_config.ENEMY_03_DETECT_RANGE
        self.attack_range = enemy_config.ENEMY_03_ATTACK_RANGE
        self.attack_cooldown = enemy_config.ENEMY_03_ATTACK_COOLDOWN 