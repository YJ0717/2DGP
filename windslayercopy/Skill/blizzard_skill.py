from pico2d import *
import gfw
import gfw.image as image
import config
import time

class BlizzardSkill:
    def __init__(self, cast_image_file='blizzard_attack.png', skill_image_file='blizzard_skill.png'):
        self.cast_image = image.load(cast_image_file)
        self.skill_image = image.load(skill_image_file)
        self.is_casting = False
        self.cast_time = 0
        self.cast_duration = config.BLIZZARD_CAST_DURATION
        self.frame = 0
        self.cast_frame_count = config.BLIZZARD_CAST_FRAME_COUNT
        self.cast_frame_width = config.BLIZZARD_CAST_FRAME_WIDTH
        self.cast_frame_height = config.BLIZZARD_CAST_FRAME_HEIGHT
        self.cast_fps = config.BLIZZARD_CAST_FPS
        self.projectiles = []
        self.skill_cooldown = config.BLIZZARD_SKILL_COOLDOWN
        self.last_skill_time = -self.skill_cooldown
        self.spawn_offset_x = config.BLIZZARD_SKILL_SPAWN_OFFSET_X

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

    def update(self):
        if self.is_casting:
            self.cast_time += gfw.frame_time
            if self.cast_time >= self.cast_duration:
                self.is_casting = False
                self.projectiles.append(Projectile(self.skill_x, self.skill_y, self.direction, self.skill_image))
            else:
                self.frame = int(self.cast_time * self.cast_fps) % self.cast_frame_count

        self.projectiles = [p for p in self.projectiles if p.update()]

    def draw(self, x, y, flip='h'):
        if self.is_casting:
            x_offset = self.frame * self.cast_frame_width
            self.cast_image.clip_composite_draw(
                x_offset, 0, self.cast_frame_width, self.cast_frame_height,
                0, flip, x, y,
                self.cast_frame_width, self.cast_frame_height
            )
        for projectile in self.projectiles:
            projectile.draw()

class Projectile:
    def __init__(self, x, y, direction, image):
        self.x = x
        self.y = y + 100
        self.direction = direction
        self.image = image
        self.frame = 0
        self.frame_count = config.BLIZZARD_SKILL_FRAME_COUNT
        self.frame_width = config.BLIZZARD_SKILL_FRAME_WIDTH
        self.frame_height = config.BLIZZARD_SKILL_FRAME_HEIGHT
        self.fps = config.BLIZZARD_SKILL_FPS
        self.elapsed_time = 0
        self.duration = config.BLIZZARD_SKILL_DURATION

    def update(self):
        self.elapsed_time += gfw.frame_time
        self.frame = int(self.elapsed_time * self.fps) % self.frame_count

        if self.elapsed_time > self.duration:
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
        # 바운딩 박스 그리기
        left, bottom, right, top = self.get_bounding_box()
        draw_rectangle(left, bottom, right, top)

    def get_bounding_box(self):
        x, y = self.x, self.y
        width, height = self.frame_width, self.frame_height
        return (x - width // 2, y - height // 2, x + width // 2, y + height // 2)
