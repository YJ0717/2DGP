from pico2d import *
import gfw.image as image
import config
import time

class PlayerUI:
    def __init__(self, player):
        self.player = player
        self.ui_background = image.load('ui_background.png')
        self.hp_image = image.load('hp_bar.png')
        self.mp_image = image.load('mp_bar.png')
        self.quick_slot_image = image.load('quick_slot.png')
        self.potion_image = image.load('potion.png')

        # =============================== UI 위치 및 크기 설정 ===============================
        self.ui_x, self.ui_y = 160, 695
        self.bar_width = self.hp_image.w
        self.bar_height = self.hp_image.h

        # =============================== hp/mp 바 위치 설정 ===============================
        self.hp_x, self.hp_y = 87, 705
        self.mp_x, self.mp_y = 58, 695

        # =============================== 퀵슬롯 위치 설정 ===============================
        self.quick_slot_x, self.quick_slot_y = 160, 655

        # =============================== 포션 위치 설정 ===============================
        self.potion_x = 30
        self.potion_y = 660

        self.skill_images = {
            'wind': image.load('wind_icon.png'),
            'ice': image.load('ice_icon.png'),
            'fire': image.load('fire_icon.png'),
            'stone': image.load('stone_icon.png'),
            'blizzard': image.load('blizzard_icon.png'),
            'nuclear': image.load('nuclear_icon.png')
        }
        self.skill_positions = {
            'wind': (60, 660),
            'ice': (100, 660),
            'fire': (140, 660),
            'stone': (180, 660),
            'blizzard': (220, 660),
            'nuclear': (260, 660)
        }

#========================최대 hp에서 현재 hp 비율에 따라 줄어드는 위치 계산 ========================
    def draw(self):
        self.ui_background.draw(self.ui_x, self.ui_y)

        hp_ratio = self.player.hp / self.player.max_hp
        hp_x_offset = int(self.bar_width * (1 - hp_ratio))
        self.hp_image.clip_draw(
            hp_x_offset, 0,
            int(self.bar_width * hp_ratio), self.bar_height,
            self.hp_x - hp_x_offset//2, self.hp_y
        )

        mp_ratio = self.player.mp / self.player.max_mp
        mp_x_offset = int(self.bar_width * 0.5 * (1 - mp_ratio))
        self.mp_image.clip_draw(
            mp_x_offset, 0,
            int(self.bar_width * 0.5 * mp_ratio), self.bar_height,
            self.mp_x - mp_x_offset//2, self.mp_y
        )

        self.quick_slot_image.draw(self.quick_slot_x, self.quick_slot_y)

        # 포션 UI 그리기
        if self.player.potion_available:
            self.potion_image.draw(self.potion_x, self.potion_y)
        else:
            self.potion_image.opacify(0.5)
            self.potion_image.draw(self.potion_x, self.potion_y)
            self.potion_image.opacify(1.0)

        # 스킬 아이콘 그리기
        if self.player.weapon_equipped and self.player.weapon:
            for skill_name, pos in self.skill_positions.items():
                skill_image = self.skill_images[skill_name]
                x, y = pos
                
                # 스킬이 쿨타임 중인지 확인
                skill = getattr(self.player.weapon, f'{skill_name}_skill', None)
                if skill and time.time() - skill.last_skill_time < skill.skill_cooldown:
                    skill_image.opacify(0.5)  # 쿨타임 중이면 반투명하게
                else:
                    skill_image.opacify(1.0)  # 사용 가능하면 불투명하게
                
                skill_image.draw(x, y)

    def update(self):
        # =============================== 필요시 업데이트 로직 추가 ===============================
        pass
