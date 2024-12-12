from pico2d import *
import gfw
import gfw.image as image
import enemy.enemy_config as enemy_config
from enemy.enemy_01 import Enemy_01
import time

class Enemy_05(Enemy_01):
    def __init__(self, x, y, player=None):
        super().__init__(x, y)
        self.target_player = player
        self.load_enemy05_images()
        self.init_enemy05_attributes()
        self.target_x = x
        self.projectiles = []
        self.projectile_image = image.load('enemy05_projectile.png')
        self.projectile_speed = 250  
        self.projectile_damage = 20  
        self.projectile_frame_count = 1
        self.projectile_fps = 6
        self.projectile_width = self.projectile_image.w // self.projectile_frame_count
        self.projectile_height = self.projectile_image.h
        self.attack_frame = 0

    def load_enemy05_images(self):
        self.idle_image = image.load('enemy05_idle.png')
        self.walk_image = image.load('enemy05_walk.png')
        self.attack_image = image.load('enemy05_attack.png')
        self.hit_image = image.load('enemy05_hit.png')
        self.dead_image = image.load('enemy05_dead.png')
        self.current_image = self.idle_image

    def init_enemy05_attributes(self):
        self.hp = enemy_config.ENEMY_05_HP
        self.max_hp = enemy_config.ENEMY_05_HP
        self.attack_power = enemy_config.ENEMY_05_ATTACK_POWER
        self.defense = enemy_config.ENEMY_05_DEFENSE
        self.speed = enemy_config.ENEMY_05_WALK_SPEED
        
        self.animations = {
            Enemy_01.IDLE: {'frame_count': 3, 'fps': enemy_config.ENEMY_05_IDLE_FPS, 'width': 190, 'height': 150},
            Enemy_01.WALK: {'frame_count': 3, 'fps': enemy_config.ENEMY_05_WALK_FPS, 'width': 190, 'height': 150},
            Enemy_01.ATTACK: {'frame_count': 4, 'fps': enemy_config.ENEMY_05_ATTACK_FPS, 'width': 229, 'height': 195},
            Enemy_01.HIT: {'frame_count': 3, 'fps': enemy_config.ENEMY_05_HIT_FPS, 'width': 201, 'height': 172},
            Enemy_01.DEAD: {'frame_count': 3, 'fps': enemy_config.ENEMY_05_DEAD_FPS, 'width': 202, 'height': 182}
        }

        self.detect_range = enemy_config.ENEMY_05_DETECT_RANGE
        self.attack_range = enemy_config.ENEMY_05_ATTACK_RANGE
        self.attack_cooldown = enemy_config.ENEMY_05_ATTACK_COOLDOWN

    def update(self):
        super().update()
        
        if self.state == Enemy_01.ATTACK:
            anim = self.animations[Enemy_01.ATTACK]
            current_frame = int(self.time * anim['fps']) % anim['frame_count']
            if current_frame == anim['frame_count'] - 1 and self.attack_frame != current_frame:
                self.create_projectile()
            self.attack_frame = current_frame
        
        for projectile in self.projectiles[:]:
            projectile['x'] += projectile['direction'] * self.projectile_speed * gfw.frame_time
            projectile['time'] += gfw.frame_time
            
            if hasattr(self, 'target_player'):
                screen_x, screen_y = self.get_screen_position()
                offset_x = screen_x - self.x
                offset_y = self.y - screen_y
                
                proj_screen_x = projectile['x'] + offset_x
                proj_screen_y = projectile['y'] - offset_y
                
                proj_box = (
                    proj_screen_x - 15,
                    proj_screen_y - 15,
                    proj_screen_x + 15,
                    proj_screen_y + 15
                )
                
                player_box = self.target_player.get_bounding_box()
                
                if (proj_box[0] < player_box[2] and
                    proj_box[2] > player_box[0] and
                    proj_box[1] < player_box[3] and
                    proj_box[3] > player_box[1]):
                    if not self.target_player.invincible:
                        self.target_player.hp -= self.projectile_damage
                        self.target_player.state = 'hit'
                        self.target_player.invincible = True
                        self.target_player.invincible_time = 1.0
                        self.target_player.hit_start_time = time.time()
                        self.target_player.hit_timer = 0
                    
                    self.projectiles.remove(projectile)
                    continue
            
            projectile['frame_time'] += gfw.frame_time
            if projectile['frame_time'] >= 1 / self.projectile_fps:
                projectile['frame'] = (projectile['frame'] + 1) % self.projectile_frame_count
                projectile['frame_time'] = 0
            
            if abs(projectile['x'] - self.x) > 500:
                self.projectiles.remove(projectile)

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

    def start_attack(self):
        if self.state != Enemy_01.ATTACK:
            self.state = Enemy_01.ATTACK
            self.time = 0
            self.current_image = self.attack_image
            self.attack_frame = 0
            if hasattr(self, 'target_player'):
                self.direction = 1 if self.target_player.x > self.x else -1

    def create_projectile(self):
        projectile = {
            'x': self.x + (30 * self.direction),
            'y': self.y,
            'direction': self.direction,
            'time': 0,
            'active': True,
            'frame': 0,
            'frame_time': 0
        }
        self.projectiles.append(projectile)

    def draw(self):
        super().draw()
        for projectile in self.projectiles:
            screen_x, screen_y = self.get_screen_position()
            offset_x = projectile['x'] - self.x
            offset_y = self.y - screen_y
            
            self.projectile_image.clip_composite_draw(
                projectile['frame'] * self.projectile_width, 0,
                self.projectile_width, self.projectile_height,
                0, 'h' if projectile['direction'] > 0 else ' ',
                screen_x + offset_x, projectile['y'] - offset_y,
                self.projectile_width, self.projectile_height
            ) 

    def get_projectile_damage(self):
        return self.projectile_damage

    def get_projectile_boxes(self):
        boxes = []
        screen_x, screen_y = self.get_screen_position()
        offset_x = screen_x - self.x
        offset_y = screen_y - self.y
        
        for projectile in self.projectiles:
            proj_screen_x = projectile['x'] + offset_x
            proj_screen_y = projectile['y'] + offset_y
            
            box = (
                proj_screen_x - self.projectile_width//2,
                proj_screen_y - self.projectile_height//2,
                proj_screen_x + self.projectile_width//2,
                proj_screen_y + self.projectile_height//2
            )
            boxes.append((box, projectile))
        
        return boxes

    def remove_projectile(self, projectile):
        if projectile in self.projectiles:
            self.projectiles.remove(projectile)

    def get_bb(self):
        return (
            self.x - self.animations[self.state]['width']//2,
            self.y - self.animations[self.state]['height']//2,
            self.x + self.animations[self.state]['width']//2,
            self.y + self.animations[self.state]['height']//2
        )

    def check_projectile_collision(self, projectile, player):
        projectile_bb = (
            projectile['x'] - 30,
            projectile['y'] - 45,
            projectile['x'] + 30,
            projectile['y'] + 45
        )
        
        player_bb = player.get_bb()
        
        if (projectile_bb[0] < player_bb[2] and 
            projectile_bb[2] > player_bb[0] and 
            projectile_bb[1] < player_bb[3] and 
            projectile_bb[3] > player_bb[1]):
            
            if not player.attacking:
                player.hp -= self.projectile_damage
                return True
            
        return False