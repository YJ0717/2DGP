from pico2d import *
import gfw
import gfw.image as image
import config
import time

#=================== 스킬시전 클래스와 투사체 클래스를 분류하여 기존에 있던 버그 수정 해결 ===================



#============== 바람스킬시전 업데이트 및 그리기 기능 ==================================================
class WindSkill:
    def __init__(self, cast_image_file='wind_attack.png', skill_image_file='wind_skill.png'):
        self.cast_image = image.load(cast_image_file)
        self.skill_image = image.load(skill_image_file)
        self.is_casting = False
        self.cast_time = 0
        self.cast_duration = config.WIND_CAST_DURATION
        self.frame = 0
        self.cast_frame_count = config.WIND_CAST_FRAME_COUNT
        self.cast_frame_width = config.WIND_CAST_FRAME_WIDTH
        self.cast_frame_height = config.WIND_CAST_FRAME_HEIGHT
        self.cast_fps = config.WIND_CAST_FPS
        self.projectiles = []  
        self.skill_cooldown = config.WIND_SKILL_COOLDOWN
        self.last_skill_time = -self.skill_cooldown
#==================== 스킬 시전 중인지 아닌지 확인하고 투사체클래스에게 정보 전달================   
    def start_cast(self, x, y, direction):
        current_time = time.time()
        if self.is_casting or current_time - self.last_skill_time < self.skill_cooldown:
            return

        self.is_casting = True
        self.cast_time = 0
        self.frame = 0
        self.skill_x = x
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
                projectile = Projectile(self.skill_x, self.skill_y, self.direction, self.skill_image)
                self.projectiles.append(projectile)
            else:
                self.frame = int(self.cast_time * self.cast_fps) % self.cast_frame_count

        for projectile in self.projectiles:
            projectile.update()
# ==================== 스킬 시전 애니메이션 그리기 기능 ==================================================
    def draw(self, x, y, flip='h'):
        if self.is_casting:
            x_offset = self.frame * self.cast_frame_width
            self.cast_image.clip_composite_draw(
                x_offset, 0, self.cast_frame_width, self.cast_frame_height,
                0, flip, x, y+30,
                self.cast_frame_width, self.cast_frame_height
            )
             #원래는 여기에 바람스킬 말고 다른 스킬투사체를 넣을려고 생각해봤는데 그냥 새로운 .py를 만드는게 더 좋다고 판단됨 
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
        self.frame_count = config.WIND_SKILL_FRAME_COUNT
        self.frame_width = config.WIND_SKILL_FRAME_WIDTH
        self.frame_height = config.WIND_SKILL_FRAME_HEIGHT
        self.fps = config.WIND_SKILL_FPS
        self.max_range = config.WIND_SKILL_MAX_RANGE
        self.start_x = x
        self.elapsed_time = 0
# ==================== 투사체 업데이트 기능 ==================================================
    def update(self):
        self.elapsed_time += gfw.frame_time
        self.frame = int(self.elapsed_time * self.fps) % self.frame_count
        self.x += self.direction * config.WIND_SKILL_SPEED * gfw.frame_time
# =========== 발사체 범위 설정 기능 ==================================================
        if abs(self.x - self.start_x) > self.max_range:
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
