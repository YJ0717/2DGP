from pico2d import *
import gfw
import config
import time
from weapon import Weapon  
from ui import PlayerUI
from attack import MagicAttack
from Skill.fire_skill import FireSkill
from Skill.stone_skill import StoneSkill
from Skill.blizzard_skill import BlizzardSkill
from enemy.enemy_01 import Enemy_01

############### 플레이어 캐릭터의 행동과 상태를 관리, Weapon 클래스를 사용하여 무기를 장착하고 공격전 행동 처리 ,MagicAttack 클래스를 통해  공격 투사체 처리#########
############################################################################################################################################################
class Player:
    #==========================================기본적인 움직임==========================================
    def __init__(self, walk_left_image_file='walk.png', walk_right_image_file='walk2.png', idle_image_file='idle.png', attack_image_file='basic_attack.png'):
        self.load_images(walk_left_image_file, walk_right_image_file, idle_image_file, attack_image_file)
        self.init_attribute()
        self.weapon = None  
        self.weapon_equipped = False  
        #============= 추후 몬스터와 충돌처리할때 스탯구성 =================    
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.exp = 0  
        #================================= UI ,공격 추가==============================
        self.ui = PlayerUI(self)
        self.magic_attack = MagicAttack()  # 공격 인스턴스 추가
        self.attack_cooldown_time = 0.5  # 공격 모션 쿨타임 ex)s를 누르고 바로d를 못누르게 하기 위해
        self.last_attack_end_time = 0  # 마지막 공격 종료 시간
        self.fire_skill = FireSkill()
        self.stone_skill = StoneSkill()
        self.blizzard_skill = BlizzardSkill()

        #========================== 몬스터한테 맞았을 때 ========================
        self.is_hit = False  
        self.invincible = False  
        self.invincible_duration = 1.5  
        self.invincible_time = 0  
        self.hit_image = gfw.image.load('player_hit.png')  
        self.hit_duration = 0.2  
        self.hit_time = 0  
        self.hit_frame_count = 1  
        self.hit_frame_width = 100  
        self.hit_frame_height = 130 
        self.hit_fps = 3
        self.hit_frame = 0 
        self.prev_hp = self.hp  

    #==========================================행동이미지 로드==========================================
    def load_images(self, walk_left_image_file, walk_right_image_file, idle_image_file, attack_image_file):
        self.walk_left_image = gfw.image.load(walk_left_image_file)
        self.walk_right_image = gfw.image.load(walk_right_image_file)
        self.idle_image = gfw.image.load(idle_image_file)
        self.attack_image = gfw.image.load(attack_image_file)  
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
        # =================================공격 추가==============================
        self.is_attacking = False  
        self.attack_time = 0
        self.attack_duration = config.ATTACK_DURATION  
        self.near_portal = False  

    #==========================================행동 업데이트==========================================
    def update(self):
        self.time += gfw.frame_time

        if self.is_hit:
            self.hit_time += gfw.frame_time
            self.hit_frame = int(self.hit_time * self.hit_fps) % self.hit_frame_count
            if self.hit_time >= self.hit_duration:
                self.is_hit = False
                self.invincible = True  
                self.invincible_time = 0
            return  

        if self.invincible:
            self.invincible_time += gfw.frame_time
            if self.invincible_time >= self.invincible_duration:
                self.invincible = False

        if self.is_dashing:
            self.update_dash()
        elif self.is_attacking:
            self.update_attack()
        else:
            self.update_movement()
            self.update_jump()

        if self.weapon_equipped and self.weapon:
            self.weapon.update(self)
        else:
            self.magic_attack.update()
        self.ui.update()

        if not self.is_jumping:
            self.velocity_y += self.gravity
            self.y += self.velocity_y

            if self.y < 0:
                self.y = 0
                self.velocity_y = 0
                self.is_jumping = False
                self.can_double_jump = True

        self.ui.update()

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

        # 플레이어 좌표 출력
        print(f"플레이어 좌표: x={self.x}, y={self.y}")

    #==========================================점프 업데이트==========================================
    def update_jump(self):
        if self.is_jumping:
            self.y += self.velocity_y
            self.velocity_y += self.gravity
            
            if self.y <= 0:  
                self.y = 0  
                self.is_jumping = False  
                self.can_double_jump = True  
                self.velocity_y = 0  
            else:
                self.start_y = self.y  

    #==========================================그리기========================================== 
    def draw(self):
        self.ui.draw()

        if self.is_hit:
            x_offset = self.hit_frame * self.hit_frame_width
            self.hit_image.clip_draw(x_offset, 0, self.hit_frame_width, self.hit_frame_height, self.x, self.y)
        else:
            if self.invincible:
                if int(self.invincible_time * 10) % 2 == 0:
                    return  

            if self.weapon_equipped and self.weapon:
                self.weapon.draw(self.x, self.y, 'h' if self.dx > 0 else '')
                half_width = config.IDLE_FRAME_WIDTH // 2
                half_height = config.IDLE_FRAME_HEIGHT // 2
                draw_rectangle(self.x - half_width, self.y - half_height,
                               self.x + half_width, self.y + half_height)
            else:
                if self.is_dashing:
                    self.draw_dash()
                elif self.is_attacking:
                    self.magic_attack.draw(self.x, self.y, 'h' if self.dx > 0 else '')
                elif self.is_jumping:
                    self.draw_jump()
                else:
                    x = self.frame * self.frame_width
                    y = self.action * self.frame_height
                    self.current_image.clip_draw(x, y, self.frame_width, self.frame_height, self.x, self.y)

                half_width = self.frame_width // 2
                half_height = self.frame_height // 2
                draw_rectangle(self.x - half_width, self.y - half_height,
                               self.x + half_width, self.y + half_height)

            self.magic_attack.draw(self.x, self.y, 'h' if self.dx > 0 else '')

    #==========================================대쉬 그리기==========================================
    def draw_dash(self):
        frame_width, frame_height = config.DASH_FRAME_SIZES[self.dash_frame]
        x = self.dash_frame * frame_width
        if self.dx > 0:
            self.dash_image_left.clip_composite_draw(
                x, 0, frame_width, frame_height,
                0, 'h',  
                self.x, self.y,
                frame_width, frame_height  
            )
        else:
            # ====왼쪽 대쉬: dash.png를 그대로 사용 ====
            self.dash_image_left.clip_draw(x, 0, frame_width, frame_height, self.x, self.y)

    # =============================== 점프 그리기 ===============================
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

    #==========================================공격 업데이트==========================================

    def update_attack(self):
        self.attack_time += gfw.frame_time
        if self.attack_time >= self.attack_duration:
            self.is_attacking = False
            self.last_attack_end_time = time.time()  
        else:
            fps = config.ATTACK_FPS  
            frame_count = config.ATTACK_FRAME_COUNT  
            self.frame = int(self.attack_time * fps) % frame_count

    def draw_attack(self):
        x = self.frame * self.frame_width
        self.attack_image.clip_draw(x, 0, self.frame_width, self.frame_height, self.x, self.y)

    #==========================================키 이벤트==========================================
    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            self.handle_keydown(e)
        elif e.type == SDL_KEYUP:
            self.handle_keyup(e)

    def handle_keydown(self, e):
        current_time = time.time()  
        if e.key in (SDLK_LEFT, SDLK_RIGHT): 
            direction = -1 if e.key == SDLK_LEFT else 1
            
            # =================대쉬 조건 =================
            if self.last_direction == direction and current_time - self.last_key_time < self.key_press_interval:
                if not self.is_jumping and current_time - self.last_dash_time >= self.dash_cooldown:
                    self.is_dashing = True  
                    self.dash_time = 0  
                    self.last_dash_time = current_time  
            
            # =================이동 방향 및 시간 업데이트=================
            self.dx = direction
            self.last_key_time = current_time  
            self.last_direction = direction  

        # =================점프 처리=================
        elif e.key == SDLK_UP:
            if self.near_portal:
                import Map.stage_2 as stage_2
                gfw.change(stage_2)
            # ============== npc 대화 키 입력 처리 ===============
            elif self.near_npc2:  
                self.talk_to_npc2 = True  
            elif not self.is_jumping:
                self.is_jumping = True
                self.velocity_y = self.jump_speed
            elif self.can_double_jump:
                self.can_double_jump = False
                self.velocity_y = self.jump_speed
                self.double_jump_time = 0

        # 아래 방향키 입력 처리
        elif e.key == SDLK_DOWN:
            self.dy = -1  # 추후 삭제 예정

        elif e.key == SDLK_LSHIFT:
            if not self.is_jumping:
                self.is_dashing = True  
                self.dash_time = 0  

        # =============================== 무기 공격 키처리 ===============================
        elif e.key == SDLK_u:  # 무기를 착용했을때만 공격 키 처리
            self.toggle_weapon()

        elif e.key == SDLK_s:  # S 키로 약한공격
            if self.weapon_equipped and self.weapon and not self.is_attacking:
                if (current_time - self.last_attack_end_time >= self.attack_cooldown_time and
                    current_time - self.weapon.magic_attack.last_attack_time >= self.weapon.magic_attack.attack_cooldown):
                    self.weapon.magic_attack.start_attack(self.x, self.y, 1 if self.dx > 0 else -1)
                    self.is_attacking = True
                    self.attack_time = 0

        elif e.key == SDLK_d:  # D 키로 강한공격
            if self.weapon_equipped and self.weapon and not self.is_attacking:
                if (current_time - self.last_attack_end_time >= self.attack_cooldown_time and
                    current_time - self.weapon.magic_attack.last_attack_time2 >= self.weapon.magic_attack.attack_cooldown2):
                    self.weapon.magic_attack.start_attack2(self.x, self.y, 1 if self.dx > 0 else -1)
                    self.is_attacking = True
                    self.attack_time = 0

        elif e.key == SDLK_2:  # 2 키로 스킬 발동
            if self.weapon_equipped and self.weapon:
                self.weapon.start_skill(self.x, self.y, 1 if self.dx > 0 else -1)

        elif e.key == SDLK_3:  # 3 키로 얼음 스킬 발동
            if self.weapon_equipped and self.weapon:
                self.weapon.start_ice_skill(self.x, self.y, 1 if self.dx > 0 else -1)

        elif e.key == SDLK_4:  # 4 키로 불 스킬 발동
            if self.weapon_equipped and self.weapon:
                self.weapon.start_fire_skill(self.x, self.y, 1 if self.dx > 0 else -1)

        elif e.key == SDLK_5:  # 5 키로 땅 스킬 발동
            if self.weapon_equipped and self.weapon:
                self.weapon.start_stone_skill(self.x, self.y, 1 if self.dx > 0 else -1)

        elif e.key == SDLK_q:  # Q 키로 블리자드 스킬 발동
            if self.weapon_equipped and self.weapon:
                self.weapon.start_blizzard_skill(self.x, self.y, 1 if self.dx > 0 else -1)

        elif e.key == SDLK_r:  # R 키로 핵 스킬 발동
            if self.weapon_equipped and self.weapon:
                self.weapon.start_nuclear_skill(self.x, self.y, 1 if self.dx > 0 else -1)

    def handle_keyup(self, e):
        if e.key == SDLK_LEFT and self.dx < 0:
            self.dx = 0
        elif e.key == SDLK_RIGHT and self.dx > 0:
            self.dx = 0
        elif e.key == SDLK_DOWN and self.dy < 0:
            self.dy = 0

    #==========================================플레이어와 적의 충돌 처리==========================================  
    def handle_collision(self, group, other):
        if self.is_hit or self.invincible:
            return

        if group == 'player:enemy':
            if isinstance(other, Enemy_01):
                self.is_hit = True
                self.hp -= other.attack_power
                self.invincible = True
                self.invincible_time = 0

#==========================================무기 착/해제 처리==========================================
    def toggle_weapon(self):
        if not self.talk_to_npc2:  # NPC2와 대화하기 전에는 무기 장착 불가
            return

        if self.weapon_equipped:
            self.weapon_equipped = False
            self.weapon = None
        else:   
            self.weapon_equipped = True
            self.weapon = Weapon()  
#==========================================플레이어 바운딩 박스 처리==========================================
    def get_bounding_box(self):
        half_width = self.frame_width // 2
        half_height = self.frame_height // 2
        return (self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height)

#============================================갹체를 생성 및  다른 코드와 상호작용역할  ========================================
class CustomPlayer(Player):
    def __init__(self, walk_left_image_file='walk.png', walk_right_image_file='walk2.png', idle_image_file='idle.png', attack_image_file='basic_attack.png', equip_weapon=False):
        super().__init__(walk_left_image_file, walk_right_image_file, idle_image_file, attack_image_file)
        self.width = config.IDLE_FRAME_WIDTH
        self.height = config.IDLE_FRAME_HEIGHT
        self.talk_to_npc2 = False
        self.near_npc2 = False
        self.near_portal = False
        
        if equip_weapon:
            self.weapon = Weapon()
            self.weapon_equipped = True
        else:
            self.weapon = None

    def get_bounding_box(self):
        half_width = self.frame_width // 2
        half_height = self.frame_height // 2
        return (self.x - half_width, self.y - half_height, self.x + half_width, self.y + half_height)

    def equip_weapon(self):
        if self.weapon is None:
            self.weapon = Weapon()  