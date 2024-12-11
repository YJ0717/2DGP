from pico2d import *
import gfw.image as image

class PlayerUI:
    def __init__(self, player):
        self.player = player
        self.ui_background = image.load('ui_background.png')
        self.hp_image = image.load('hp_bar.png')
        self.mp_image = image.load('mp_bar.png')
        self.quick_slot_image = image.load('quick_slot.png')

        # =============================== UI 위치 및 크기 설정 ===============================
        self.ui_x, self.ui_y = 160, 695
        self.bar_width = self.hp_image.w
        self.bar_height = self.hp_image.h

        # =============================== hp/mp 바 위치 설정 ===============================
        self.hp_x, self.hp_y = 87, 705
        self.mp_x, self.mp_y = 58, 695

        # =============================== 퀵슬롯 위치 설정 ===============================
        self.quick_slot_x, self.quick_slot_y = 160, 655

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

    def update(self):
        # =============================== 필요시 업데이트 로직 추가 ===============================
        pass
