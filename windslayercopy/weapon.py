from pico2d import *
import gfw
import config
import gfw.image as image
from attack import MagicAttack
from Skill.wind_skill import WindSkill
from Skill.ice_skill import IceSkill
from Skill.fire_skill import FireSkill
from Skill.stone_skill import StoneSkill
from Skill.blizzard_skill import BlizzardSkill
from Skill.nuclear_skill import NuclearSkill

class Weapon:
    #==============무기 이미지를 로드하고 초기 속성을 설정======================
    def __init__(self, walk_left_image_file='weapon_walk.png', idle_image_file='weapon_idle.png', dash_image_file='weapon_dash.png', jump_image_file='weapon_jump.png', double_jump_image_file='weapon_jump2.png', attack_image_file='basic_attack.png', attack_image_file2='second_attack.png'):
        self.load_images(walk_left_image_file, idle_image_file, dash_image_file, jump_image_file, double_jump_image_file, attack_image_file)
        self.init_attributes()
        self.magic_attack = MagicAttack(attack_image_file, attack_image_file2)
        self.wind_skill = WindSkill()
        self.ice_skill = IceSkill()
        self.fire_skill = FireSkill()
        self.stone_skill = StoneSkill()
        self.blizzard_skill = BlizzardSkill()
        self.nuclear_skill = NuclearSkill()

    # =============================== 무기 이미지 로드 ===============================
    def load_images(self, walk_left_image_file, idle_image_file, dash_image_file, jump_image_file, double_jump_image_file, attack_image_file):
        self.walk_left_image = image.load(walk_left_image_file)
        self.idle_image = image.load(idle_image_file)
        self.dash_image = image.load(dash_image_file)
        self.jump_image = image.load(jump_image_file)
        self.double_jump_image = image.load(double_jump_image_file)
        self.attack_image = image.load(attack_image_file)

    # =============================== 무기 초기 속성 설정 ===============================
    def init_attributes(self):
        self.current_image = self.idle_image
        self.frame = 0
        self.time = 0
        self.frame_width = config.IDLE_FRAME_WIDTH
        self.frame_height = config.IDLE_FRAME_HEIGHT
        self.is_attacking = False
        self.attack_time = 0
        self.attack_duration = config.ATTACK_DURATION

    # =============================== 공격,무기를착용했을때 행동 업데이트 ===============================
    def update(self, player):
        self.time += gfw.frame_time
        if self.magic_attack.is_attacking or self.magic_attack.is_attacking2:
            self.magic_attack.update()
            player.is_attacking = True  # 공격 중일 때 플레이어의 공격 상태 설정
        elif self.wind_skill.is_casting:
            self.wind_skill.update()
            player.is_attacking = True  # 스킬 사용 중일 때 플레이어의 공격 상태 설정
        elif self.ice_skill.is_casting:
            self.ice_skill.update()
            player.is_attacking = True
        elif self.fire_skill.is_casting:
            self.fire_skill.update()
            player.is_attacking = True
        elif self.stone_skill.is_casting:
            self.stone_skill.update()
            player.is_attacking = True
        elif self.blizzard_skill.is_casting:
            self.blizzard_skill.update()
            player.is_attacking = True
        elif self.nuclear_skill.is_casting:
            self.nuclear_skill.update()
            player.is_attacking = True
        elif player.is_dashing:
            self.update_dash(player)
        elif player.is_jumping:
            self.update_jump(player)
        else:
            self.update_movement(player)

        self.wind_skill.projectiles = [p for p in self.wind_skill.projectiles if p.update()]
        self.ice_skill.projectiles = [p for p in self.ice_skill.projectiles if p.update()]
        self.fire_skill.projectiles = [p for p in self.fire_skill.projectiles if p.update()]
        self.stone_skill.projectiles = [p for p in self.stone_skill.projectiles if p.update()]
        self.blizzard_skill.projectiles = [p for p in self.blizzard_skill.projectiles if p.update()]
        self.nuclear_skill.projectiles = [p for p in self.nuclear_skill.projectiles if p.update()]

    # =============================== 대쉬 행동 업데이트 ===============================
    def update_dash(self, player):
        self.current_image = self.dash_image
        self.frame_width = config.WEAPON_DASH_FRAME_WIDTH
        self.frame_height = config.WEAPON_DASH_FRAME_HEIGHT
        fps = config.WEAPON_DASH_FPS
        frame_count = config.WEAPON_DASH_FRAME_COUNT
        self.frame = round(self.time * fps) % frame_count

    # =============================== 이동 행동 업데이트 ===============================
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

    # =============================== 점프 행동 업데이트 ===============================
    def update_jump(self, player):
        if player.can_double_jump:
            self.current_image = self.jump_image
            self.frame_width = config.WEAPON_JUMP_FRAME_WIDTH
            self.frame_height = config.WEAPON_JUMP_FRAME_HEIGHT
            fps = config.WEAPON_JUMP_FPS
            frame_count = config.WEAPON_JUMP_FRAME_COUNT
            self.frame = round(self.time * fps) % frame_count
        else:
            self.current_image = self.double_jump_image
            self.frame_width = config.WEAPON_DOUBLE_JUMP_FRAME_WIDTH
            self.frame_height = config.WEAPON_DOUBLE_JUMP_FRAME_HEIGHT
            fps = config.WEAPON_DOUBLE_JUMP_FPS
            frame_count = config.WEAPON_DOUBLE_JUMP_FRAME_COUNT
            self.frame = round(self.time * fps) % frame_count
            
            if self.frame == 0 and self.time > 0:
                self.time = 0

    # =============================== 약한 공격 시작 ===============================
    def start_attack(self):
        if not self.magic_attack.is_attacking:
            self.magic_attack.start_attack()

    # =============================== 강한 공격 시작 ===============================
    def start_attack2(self):
        if not self.magic_attack.is_attacking2:
            self.magic_attack.start_attack2()
            
    # =============================== 바람스킬 행동 시작 ===============================
    def start_skill(self, x, y, direction):
        self.wind_skill.start_cast(x, y, direction)
            
    # =============================== 얼음스킬 행동 시작 ===============================
    def start_ice_skill(self, x, y, direction):
        self.ice_skill.start_cast(x, y, direction)

    # =============================== 불 스킬 행동 시작 ===============================
    def start_fire_skill(self, x, y, direction):
        self.fire_skill.start_cast(x, y, direction)

    # =============================== 땅 스킬 행동 시작 ===============================
    def start_stone_skill(self, x, y, direction):
        self.stone_skill.start_cast(x, y, direction)

    # =============================== 블리자드 스킬 행동 시작 ===============================
    def start_blizzard_skill(self, x, y, direction):
        self.blizzard_skill.start_cast(x, y, direction)

    # =============================== 핵 스킬 행동 시작 ===============================
    def start_nuclear_skill(self, x, y, direction):
        self.nuclear_skill.start_cast(x, y, direction)

    # =============================== 공격 이미지 그리기 ===============================
    def draw(self, x, y, flip='h'):
        if self.magic_attack.is_attacking or self.magic_attack.is_attacking2:
            self.magic_attack.draw(x, y, flip)
        elif self.wind_skill.is_casting:
            self.wind_skill.draw(x, y, flip)
        elif self.ice_skill.is_casting:
            self.ice_skill.draw(x, y, flip)
        elif self.fire_skill.is_casting:
            self.fire_skill.draw(x, y, flip)
        elif self.stone_skill.is_casting:
            self.stone_skill.draw(x, y, flip)
        elif self.blizzard_skill.is_casting:
            self.blizzard_skill.draw(x, y, flip)
        elif self.nuclear_skill.is_casting:
            self.nuclear_skill.draw(x, y, flip)
        else:
            x_offset = self.frame * self.frame_width
            self.current_image.clip_composite_draw(
                x_offset, 0, self.frame_width, self.frame_height,
                0, flip, x, y,
                self.frame_width, self.frame_height
            )

        for projectile in self.wind_skill.projectiles:
            projectile.draw()
        for projectile in self.ice_skill.projectiles:
            projectile.draw()
        for projectile in self.fire_skill.projectiles:
            projectile.draw()
        for projectile in self.stone_skill.projectiles:
            projectile.draw()
        for projectile in self.blizzard_skill.projectiles:
            projectile.draw()
        for projectile in self.nuclear_skill.projectiles:
            projectile.draw()