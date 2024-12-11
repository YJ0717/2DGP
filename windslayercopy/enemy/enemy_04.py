from pico2d import *
import gfw
import gfw.image as image
import enemy.enemy_config as enemy_config
from enemy.enemy_01 import Enemy_01
import time

class Enemy_04(Enemy_01):
    def __init__(self, x, y, player=None):
        super().__init__(x, y)
        self.target_player = player
        self.load_enemy04_images()
        self.init_enemy04_attributes()
        self.target_x = x
        self.projectiles = []
        self.projectile_image = image.load('enemy04_projectile.png')
        self.projectile_speed = 200
        self.projectile_damage = 15
        self.projectile_frame_count = 3  
        self.projectile_fps = 5  
        self.projectile_width = self.projectile_image.w // self.projectile_frame_count
        self.projectile_height = self.projectile_image.h
        self.attack_frame = 0  

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
            'y': self.y ,
            'direction': self.direction,
            'time': 0,
            'active': True,
            'frame': 0,
            'frame_time': 0
        }
        self.projectiles.append(projectile)

    def get_projectile_damage(self):
        return 10

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
            
            x = screen_x + offset_x
            y = projectile['y'] - offset_y
            draw_rectangle(
                x - self.projectile_width//2, 
                y - self.projectile_height//2,
                x + self.projectile_width//2, 
                y + self.projectile_height//2
            )

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
    


#=================================================================================

# 기존 적코드를 가져오는경우는 모든 몬스터들이 world에 등록이 되어잇어서 
# world에서 자동으로 충돌처리를 해주었는데 투사체 같은 경우는 데이터일 뿐이라서 
#월드자체에서 충돌처리를 해주지 않는다
#이를 해결하기위해 직접적으로 플레이어에게 데미지를 주도록 설정
#근데? 의존성 주입문제
#의존성 주입이란?: 필요한 객체를 외부에서 넣어주는 방식 즉 이걸 한동안 못찾음
#    def __init__(self, x, y): -> def __init__(self, x, y, player): 

#=================================================================================