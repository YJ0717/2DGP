from pico2d import *
import gfw
import gfw.image as image
import config  
import time

class MagicAttack:
    # ========================= 약한공격 강한공격 이미지 로드 =========================
    def __init__(self, attack_image_file='basic_attack.png', attack_image_file2='second_attack.png'):
        self.attack_image = image.load(attack_image_file)
        self.attack_image2 = image.load(attack_image_file2)
        # ========================= 약한공격,강한공격 진행 중 여부확인 =========================
        self.is_attacking = False
        self.is_attacking2 = False
        self.attack_time = 0
        # ========================= 공격행동 프레임 지속시간 설정 =========================
        self.attack_duration = config.ATTACK_DURATION
        self.attack_duration2 = config.SECOND_ATTACK_DURATION
        self.frame = 0
        self.frame_count = config.ATTACK_FRAME_COUNT
        self.frame_count2 = config.SECOND_ATTACK_FRAME_COUNT
        self.frame_width = config.ATTACK_FRAME_WIDTH
        self.frame_width2 = config.SECOND_ATTACK_FRAME_WIDTH
        self.frame_height = config.ATTACK_FRAME_HEIGHT
        self.frame_height2 = config.SECOND_ATTACK_FRAME_HEIGHT
        self.fps = config.ATTACK_FPS
        self.fps2 = config.SECOND_ATTACK_FPS
        # ========================= 약한공격 강한공격 쿨타임 설정 =========================
        self.attack_cooldown = config.ATTACK_COOLDOWN
        self.attack_cooldown2 = config.SECOND_ATTACK_COOLDOWN
        self.last_attack_time = -self.attack_cooldown
        self.last_attack_time2 = -self.attack_cooldown2
        # ========================= 약한공격 강한공격 투사체  =========================
        self.b_attacks = []
        self.b_attack_image1 = image.load('b_attack1.png')
        self.b_attack_image2 = image.load('b_attack2.png')

    # ========================= 약한공격 투사체 발사  =========================
    def start_attack(self, x, y, direction):
        current_time = time.time()
        if self.is_attacking:
            return

        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.is_attacking = True
            self.attack_time = 0
            self.frame = 0
            self.last_attack_time = current_time
            self.fire_b_attack(x, y, direction, self.b_attack_image1, config.B_ATTACK1_FRAME_COUNT, config.B_ATTACK1_FRAME_WIDTH, config.B_ATTACK1_FRAME_HEIGHT, config.B_ATTACK1_FPS, config.B_ATTACK1_MAX_RANGE)

    # ========================= 강한공격 투사체 발사  =========================
    def start_attack2(self, x, y, direction):
        current_time = time.time()
        if self.is_attacking2:
            return

        if current_time - self.last_attack_time2 >= self.attack_cooldown2:
            self.is_attacking2 = True
            self.attack_time = 0
            self.frame = 0
            self.last_attack_time2 = current_time
            self.fire_b_attack(x, y, direction, self.b_attack_image2, config.B_ATTACK2_FRAME_COUNT, config.B_ATTACK2_FRAME_WIDTH, config.B_ATTACK2_FRAME_HEIGHT, config.B_ATTACK2_FPS, config.B_ATTACK2_MAX_RANGE)

    # ========================= 투사체 관련 구체적 설정 딕션어리로 데이터 관리  =========================
    def fire_b_attack(self, x, y, direction, image, frame_count, frame_width, frame_height, fps, max_range):
        b_attack = {
            'x': x + (frame_width if direction > 0 else 0), #오른쪽방향에는 오른쪽 위치에 공격좌표고정
            'y': y,
            'start_x': x,
            'direction': direction,
            'image': image,
            'frame_count': frame_count,
            'frame_width': frame_width,
            'frame_height': frame_height,
            'fps': fps,
            'current_frame': 0,
            'elapsed_time': 0,
            'speed': 300,
            'max_range': max_range
        }
        self.b_attacks.append(b_attack)

    # ========================= 투사체 업데이트  =========================
    def update(self):
        if self.is_attacking:
            self.attack_time += gfw.frame_time
            if self.attack_time >= self.attack_duration:
                self.is_attacking = False
                self.b_attacks = [b for b in self.b_attacks if b['image'] != self.b_attack_image1]
            else:
                self.frame = int(self.attack_time * self.fps) % self.frame_count

        if self.is_attacking2:
            self.attack_time += gfw.frame_time
            if self.attack_time >= self.attack_duration2:
                self.is_attacking2 = False
                # 강한 공격 애니메이션이 끝나면 관련 투사체 제거
                self.b_attacks = [b for b in self.b_attacks if b['image'] != self.b_attack_image2]
            else:
                self.frame = int(self.attack_time * self.fps2) % self.frame_count2

        for b_attack in self.b_attacks[:]:
            b_attack['x'] += b_attack['direction'] * b_attack['speed'] * gfw.frame_time
            b_attack['elapsed_time'] += gfw.frame_time
            b_attack['current_frame'] = int(b_attack['elapsed_time'] * b_attack['fps']) % b_attack['frame_count']
            
            if abs(b_attack['x'] - b_attack['start_x']) > b_attack['max_range']:
                self.b_attacks.remove(b_attack)

    # ========================= 약공 강공 투사체 이미지 그리기 =========================
    def draw(self, x, y, flip='h'):
        if self.is_attacking:
            x_offset = self.frame * self.frame_width
            self.attack_image.clip_composite_draw(
                x_offset, 0, self.frame_width, self.frame_height,
                0, flip, x, y,
                self.frame_width, self.frame_height
            )
        
        # 강한 공격 그기
        elif self.is_attacking2:
            x_offset = self.frame * self.frame_width2
            self.attack_image2.clip_composite_draw(
                x_offset, 0, self.frame_width2, self.frame_height2,
                0, flip, x, y,
                self.frame_width2, self.frame_height2
            )

        for b_attack in self.b_attacks:
            frame_x = b_attack['current_frame'] * b_attack['frame_width']
            if b_attack['direction'] > 0:
                draw_x = b_attack['x']
                flip_direction = 'h'
            else:
                draw_x = b_attack['x'] - b_attack['frame_width']
                flip_direction = ''

            b_attack['image'].clip_composite_draw(
                frame_x, 0, b_attack['frame_width'], b_attack['frame_height'],
                0, flip_direction, draw_x, b_attack['y'],
                b_attack['frame_width'], b_attack['frame_height']
            )
            left, bottom, right, top = self.get_bounding_box(b_attack)
            draw_rectangle(left, bottom, right, top)

    def get_bounding_box(self, b_attack):
        if b_attack['direction'] > 0:
            x = b_attack['x']
        else:
            x = b_attack['x'] - b_attack['frame_width']
        
        y = b_attack['y']
        width = b_attack['frame_width']
        height = b_attack['frame_height']
        
        return (x, y - height//2, x + width, y + height//2)