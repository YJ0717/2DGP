from pico2d import *
import gfw
import gfw.image as image
import config
import time

#=================== 스킬시전 클래스와 투사체 클래스를 분류하여 기존에 있던 버그 수정 해결 ===================

#============== 땅스킬시전 업데이트 및 그리기 기능 ==================================================
class StoneSkill:
    def __init__(self, cast_image_file='stone_attack.png', skill_image_file='stone_skill.png'):
        self.cast_image = image.load(cast_image_file)
        self.skill_image = image.load(skill_image_file)
        self.is_casting = False
        self.cast_time = 0
        self.cast_duration = config.STONE_CAST_DURATION
        self.frame = 0
        self.cast_frame_count = config.STONE_CAST_FRAME_COUNT
        self.cast_frame_width = config.STONE_CAST_FRAME_WIDTH
        self.cast_frame_height = config.STONE_CAST_FRAME_HEIGHT
        self.cast_fps = config.STONE_CAST_FPS
        self.projectiles = []  
        self.skill_cooldown = config.STONE_SKILL_COOLDOWN
        self.last_skill_time = -self.skill_cooldown
        self.spawn_offset_x = config.STONE_SKILL_SPAWN_OFFSET_X  # 스킬 소환 x축 오프셋

    #==================== 스킬 시전 중인지 아닌지 확인하고 투사체클래스에게 정보 전달================   
    def start_cast(self, x, y, direction):
        current_time = time.time()
        if self.is_casting or current_time - self.last_skill_time < self.skill_cooldown:
            return

        self.is_casting = True
        self.cast_time = 0
        self.frame = 0
        self.skill_x = x + (self.spawn_offset_x * direction)
        self.skill_y = y
        self.direction = direction
        self.last_skill_time = current_time

        return True

    # ==================== 스킬 시전 애니메이션이 나오면 투사체 나오도록 업데이트 설정 =======================
    def update(self):
        if self.is_casting:
            self.cast_time += gfw.frame_time
            if self.cast_time >= self.cast_duration:
                self.is_casting = False
                self.projectiles.append(Projectile(self.skill_x, self.skill_y, self.direction, self.skill_image))
            else:
                self.frame = int(self.cast_time * self.cast_fps) % self.cast_frame_count

        # 투사체이기때문에 x범위로 사라지는것이 아닌 지속시간으로 삭제
        self.projectiles = [p for p in self.projectiles if p.update()]

    # ==================== 스킬 시전 애니메이션 그리기 기능 ==================================================
    def draw(self, x, y, flip='h'):
        if self.is_casting:
            x_offset = self.frame * self.cast_frame_width
            self.cast_image.clip_composite_draw(
                x_offset, 0, self.cast_frame_width, self.cast_frame_height,
                0, flip, x, y+30,
                self.cast_frame_width, self.cast_frame_height
            )
        for projectile in self.projectiles:
            projectile.draw()

# ==================== 투사체 클래스 설정 ==================================================
class Projectile:
    def __init__(self, x, y, direction, image):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = image
        self.frame = 0
        self.frame_count = config.STONE_SKILL_FRAME_COUNT
        self.frame_width = config.STONE_SKILL_FRAME_WIDTH
        self.frame_height = config.STONE_SKILL_FRAME_HEIGHT
        self.fps = config.STONE_SKILL_FPS
        self.elapsed_time = 0
        self.duration = config.STONE_SKILL_DURATION  # 지속시간 설정

    # ==================== 투사체 업데이트 기능 ==================================================
    def update(self):
        self.elapsed_time += gfw.frame_time
        self.frame = int(self.elapsed_time * self.fps) % self.frame_count

        if self.elapsed_time > self.duration:
            return False  
        return True

    # ==================== 투사체 그리기 기능 ==================================================
    def draw(self):
        x_offset = self.frame * self.frame_width
        flip = 'h' if self.direction > 0 else ''
        self.image.clip_composite_draw(
            x_offset, 0, self.frame_width, self.frame_height,
            0, flip, self.x, self.y,
            self.frame_width, self.frame_height
        )