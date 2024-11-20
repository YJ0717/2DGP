from pico2d import *
import gfw
import gfw.image as image
import config
import time

class WindSkill:
    def __init__(self, cast_image_file='wind_attack.png', skill_image_file='wind_skill.png'):
        self.cast_image = image.load(cast_image_file)
        self.skill_image = image.load(skill_image_file)
        self.is_casting = False
        self.is_skill_active = False
        self.cast_time = 0
        self.skill_time = 0
        self.cast_duration = config.WIND_CAST_DURATION
        self.skill_duration = config.WIND_SKILL_DURATION
        self.frame = 0
        self.cast_frame_count = config.WIND_CAST_FRAME_COUNT
        self.skill_frame_count = config.WIND_SKILL_FRAME_COUNT
        self.cast_frame_width = config.WIND_CAST_FRAME_WIDTH
        self.skill_frame_width = config.WIND_SKILL_FRAME_WIDTH
        self.cast_frame_height = config.WIND_CAST_FRAME_HEIGHT
        self.skill_frame_height = config.WIND_SKILL_FRAME_HEIGHT
        self.cast_fps = config.WIND_CAST_FPS
        self.skill_fps = config.WIND_SKILL_FPS

    def start_cast(self, x, y, direction):
        if not self.is_casting:
            self.is_casting = True
            self.cast_time = 0
            self.frame = 0
            self.skill_x = x
            self.skill_y = y
            self.direction = direction

    def update(self):
        if self.is_casting:
            self.cast_time += gfw.frame_time
            if self.cast_time >= self.cast_duration:
                self.is_casting = False
                self.is_skill_active = True
                self.skill_time = 0
            else:
                self.frame = int(self.cast_time * self.cast_fps) % self.cast_frame_count

        if self.is_skill_active:
            self.skill_time += gfw.frame_time
            if self.skill_time >= self.skill_duration:
                self.is_skill_active = False
            else:
                self.frame = int(self.skill_time * self.skill_fps) % self.skill_frame_count
                self.skill_x += self.direction * config.WIND_SKILL_SPEED * gfw.frame_time

    def draw(self, x, y, flip='h'):
        if self.is_casting:
            x_offset = self.frame * self.cast_frame_width
            self.cast_image.clip_composite_draw(
                x_offset, 0, self.cast_frame_width, self.cast_frame_height,
                0, flip, x, y,
                self.cast_frame_width, self.cast_frame_height
            )
        elif self.is_skill_active:
            x_offset = self.frame * self.skill_frame_width
            projectile_flip = 'h' if self.direction > 0 else ''
            self.skill_image.clip_composite_draw(
                x_offset, 0, self.skill_frame_width, self.skill_frame_height,
                0, projectile_flip, self.skill_x, self.skill_y,
                self.skill_frame_width, self.skill_frame_height
            )
