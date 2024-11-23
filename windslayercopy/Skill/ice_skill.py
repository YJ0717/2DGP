from pico2d import *
import gfw
import gfw.image as image
import config
import time

# ========================== wind_skill.py 와 동일한 클래스 구조 재활용  ======================================================

class IceSkill:
    def __init__(self, cast_image_file='ice_attack.png', skill_image_file='ice_skill.png'):
        self.cast_image = image.load(cast_image_file)
        self.skill_image = image.load(skill_image_file)
        self.is_casting = False
        self.cast_time = 0
        self.cast_duration = config.ICE_CAST_DURATION
        self.frame = 0
        self.cast_frame_count = config.ICE_CAST_FRAME_COUNT
        self.cast_frame_width = config.ICE_CAST_FRAME_WIDTH
        self.cast_frame_height = config.ICE_CAST_FRAME_HEIGHT
        self.cast_fps = config.ICE_CAST_FPS
        self.projectiles = []
        self.skill_cooldown = config.ICE_SKILL_COOLDOWN
        self.last_skill_time = -self.skill_cooldown

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

    def update(self):
        if self.is_casting:
            self.cast_time += gfw.frame_time
            if self.cast_time >= self.cast_duration:
                self.is_casting = False
                projectile = IceProjectile(self.skill_x, self.skill_y, self.direction, self.skill_image)
                self.projectiles.append(projectile)
            else:
                self.frame = int(self.cast_time * self.cast_fps) % self.cast_frame_count

        for projectile in self.projectiles:
            projectile.update()

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

class IceProjectile:
    def __init__(self, x, y, direction, image):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = image
        self.frame = 0
        self.frame_count = config.ICE_SKILL_FRAME_COUNT
        self.frame_width = config.ICE_SKILL_FRAME_WIDTH
        self.frame_height = config.ICE_SKILL_FRAME_HEIGHT
        self.fps = config.ICE_SKILL_FPS
        self.max_range = config.ICE_SKILL_MAX_RANGE
        self.start_x = x
        self.elapsed_time = 0

    def update(self):
        self.elapsed_time += gfw.frame_time
        self.frame = int(self.elapsed_time * self.fps) % self.frame_count
        self.x += self.direction * config.ICE_SKILL_SPEED * gfw.frame_time

        if abs(self.x - self.start_x) > self.max_range:
            return False
        return True

    def draw(self):
        x_offset = self.frame * self.frame_width
        flip = 'h' if self.direction > 0 else ''
        self.image.clip_composite_draw(
            x_offset, 0, self.frame_width, self.frame_height,
            0, flip, self.x, self.y,
            self.frame_width, self.frame_height
        )
