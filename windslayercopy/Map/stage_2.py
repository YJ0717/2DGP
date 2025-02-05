from pico2d import *
import gfw
from player import CustomPlayer
import config
from enemy.enemy_01 import Enemy_01

world = gfw.World(['background', 'tile', 'enemy', 'player'])

class Background:
    def __init__(self):
        self.image = gfw.image.load('background.png')
        self.x = 0
        self.y = 0

    def update(self):
        global player
        self.x = -player.x * 0.5
        self.y = -player.y * 0.1

    def draw(self):
        self.image.draw_to_origin(self.x, self.y, 3000, 1250)

def enter():
    global player, background, tile_map, enemies
    player = CustomPlayer(equip_weapon=True)
    player.x = config.PLAYER_START_X
    player.y = config.PLAYER_START_Y 
    player.velocity_y = 0
    
    # ===== 적들 위치 설정 =====
    enemies = [
        Enemy_01(600, 900),  
        Enemy_01(800, 400),  
        Enemy_01(1200, 400)  
    ]
    
    background = Background()
    tile_images, tile_map_data = get_tile_map()
    tile_map = TileMap(tile_images, tile_map_data, 32, player)
    
    for enemy in enemies:
        tile_map.check_enemy_collision(enemy)
    
    world.append(background, world.layer.background)
    world.append(tile_map, world.layer.tile)
    
    for enemy in enemies:
        world.append(enemy, world.layer.enemy)
    
    world.append(player, world.layer.player)

def exit():
    player = world.objects[world.layer.player][0]
    config.PLAYER_CURRENT_HP = player.hp
    config.PLAYER_CURRENT_MP = player.mp
    world.clear()

def handle_event(e):
    global tile_map, player
    if e.type == SDL_KEYDOWN and e.key == SDLK_UP:
        if tile_map.player.near_portal:
            import Map.stage_3 as stage_3
            gfw.change(stage_3)
            return True
    return player.handle_event(e)

def update():
    world.update()
    check_collisions()

def draw():
    world.draw()

def get_tile_map():
    tile_images = [
        gfw.image.load('tile0.png'),  #투명
        gfw.image.load('tile1.png'),  #두거운블럭
        gfw.image.load('tile2.png'),  #다리
        gfw.image.load('tile3.png')   #얇은블럭
    ]

    tile_map_data = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    return tile_images, tile_map_data

class TileMap:
    def __init__(self, tile_images, tile_map_data, tile_size, player):
        self.tile_images = tile_images
        self.tile_map_data = tile_map_data
        self.tile_size = tile_size
        self.x_offset = 0
        self.y_offset = 0
        self.player = player
        self.portal_image = gfw.image.load('portal.png')  
        self.portal_animation_frame = 0  
        self.portal_animation_speed = 10  

    def update(self):
        self.x_offset = -self.player.x
        self.y_offset = self.player.y - get_canvas_height() // 2
        self.check_collision()
        
        for enemy in world.objects[world.layer.enemy]:
            enemy.x = enemy.x 
            enemy.y = enemy.y  
            self.check_enemy_collision(enemy)
        
        self.update_portal_animation()

    def update_portal_animation(self):
        self.portal_animation_frame += gfw.frame_time * self.portal_animation_speed
        if self.portal_animation_frame >= 4:
            self.portal_animation_frame = 0

#========================== 타일 충돌처리 ==========================================
    def check_collision(self):
        player_x = self.player.x
        player_y = self.player.y
        player_half_width = self.player.width // 2
        player_half_height = self.player.height // 2

        for y in range(len(self.tile_map_data)):
            row = self.tile_map_data[y]
            for x in range(len(row)):
                tile_index = row[x]
                if tile_index == 1:  
                    tile_x = x * self.tile_size + self.tile_size // 2 + self.x_offset
                    tile_y = y * int(self.tile_size) + int(self.tile_size // 2) - self.y_offset
                    half_width = 762 // 2  
                    half_height = 281 // 2  

                    if (player_x - player_half_width < tile_x + half_width and
                        player_x + player_half_width > tile_x - half_width and
                        player_y - player_half_height < tile_y + half_height and
                        player_y + player_half_height > tile_y - half_height):
                        if self.player.velocity_y <= 0:
                            self.player.y = tile_y + half_height + player_half_height
                            self.player.velocity_y = 0
                            self.player.can_move = True
                            self.player.can_double_jump = True
                            self.player.is_jumping = False
                            self.player.current_image = self.player.idle_image

                elif tile_index == 2:  
                    tile_x = x * self.tile_size + self.tile_size // 2 + self.x_offset
                    tile_y = int(y * self.tile_size + self.tile_size // 2) - self.y_offset
                    half_width = 240 // 2  
                    half_height = 26 // 2  #

                    if (player_x - player_half_width < tile_x + half_width and
                        player_x + player_half_width > tile_x - half_width and
                        player_y - player_half_height < tile_y + half_height and
                        player_y + player_half_height > tile_y - half_height):
                        if self.player.velocity_y <= 0:
                            self.player.y = tile_y + half_height + player_half_height
                            self.player.velocity_y = 0
                            self.player.can_move = True
                            self.player.can_double_jump = True
                            self.player.is_jumping = False
                            self.player.current_image = self.player.idle_image

                elif tile_index == 3:  
                    tile_x = x * self.tile_size + self.tile_size // 2 + self.x_offset
                    tile_y = int(y * self.tile_size + self.tile_size // 2) - self.y_offset
                    half_width = 400 // 2  
                    half_height = 32 // 2  

                    if (player_x - player_half_width < tile_x + half_width and
                        player_x + player_half_width > tile_x - half_width and
                        player_y - player_half_height < tile_y + half_height and
                        player_y + player_half_height > tile_y - half_height):
                        if self.player.velocity_y <= 0:
                            self.player.y = tile_y + half_height + player_half_height
                            self.player.velocity_y = 0
                            self.player.can_move = True
                            self.player.can_double_jump = True
                            self.player.is_jumping = False
                            self.player.current_image = self.player.idle_image

        portal_x = 2400 + self.x_offset
        portal_y = 230 - self.y_offset
        half_width = self.portal_image.w // 8
        half_height = self.portal_image.h // 2

        if (player_x - player_half_width < portal_x + half_width and
            player_x + player_half_width > portal_x - half_width and
            player_y - player_half_height < portal_y + half_height and
            player_y + player_half_height > portal_y - half_height):
            self.player.near_portal = True
        else:
            self.player.near_portal = False

#========================== 타일 그리기 ==========================================
    def draw(self):
        for y in range(len(self.tile_map_data)):
            row = self.tile_map_data[y]
            for x in range(len(row)):
                tile_index = row[x]
                if tile_index >= 0:
                    tile_image = self.tile_images[tile_index]
                    tile_x = x * self.tile_size + self.tile_size // 2 + self.x_offset
                    tile_y = int(y * self.tile_size + self.tile_size // 2 - self.y_offset)
                    tile_image.draw(tile_x, tile_y)

        portal_x = 2400 + self.x_offset
        portal_y = int(230 - self.y_offset)
        half_width = self.portal_image.w // 8
        half_height = self.portal_image.h // 2
        self.portal_image.clip_draw(
            int(self.portal_animation_frame) * self.portal_image.w // 4, 0,
            self.portal_image.w // 4, self.portal_image.h,
            portal_x, portal_y
        )

        draw_rectangle(portal_x - half_width, portal_y - half_height,
                       portal_x + half_width, portal_y + half_height)

# ==========================================몬스터와 타일간의 충돌처리   ==========================================
    def check_enemy_collision(self, enemy):
        enemy_x = enemy.x
        enemy_y = enemy.y
        enemy_half_width = enemy.animations[enemy.state]['width'] // 2
        enemy_half_height = enemy.animations[enemy.state]['height'] // 2

        for y in range(len(self.tile_map_data)):
            row = self.tile_map_data[y]
            for x in range(len(row)):
                tile_index = row[x]
                if tile_index == 1:
                    tile_x = x * self.tile_size + self.tile_size // 2
                    tile_y = y * self.tile_size + self.tile_size // 2
                    half_width = 762 // 2
                    half_height = 281 // 2

                    if (enemy_x - enemy_half_width < tile_x + half_width and
                        enemy_x + enemy_half_width > tile_x - half_width and
                        enemy_y - enemy_half_height < tile_y + half_height and
                        enemy_y + enemy_half_height > tile_y - half_height):
                        if enemy.velocity_y <= 0:
                            enemy.y = tile_y + half_height + enemy_half_height
                            enemy.velocity_y = 0

                elif tile_index == 2:  # 다리
                    tile_x = x * self.tile_size + self.tile_size // 2
                    tile_y = y * self.tile_size + self.tile_size // 2
                    half_width = 240 // 2
                    half_height = 26 // 2

                    if (enemy_x - enemy_half_width < tile_x + half_width and
                        enemy_x + enemy_half_width > tile_x - half_width and
                        enemy_y - enemy_half_height < tile_y + half_height and
                        enemy_y + enemy_half_height > tile_y - half_height):
                        if enemy.velocity_y <= 0:
                            enemy.y = tile_y + half_height + enemy_half_height
                            enemy.velocity_y = 0

                elif tile_index == 3:
                    tile_x = x * self.tile_size + self.tile_size // 2
                    tile_y = y * self.tile_size + self.tile_size // 2
                    half_width = 400 // 2
                    half_height = 32 // 2

                    if (enemy_x - enemy_half_width < tile_x + half_width and
                        enemy_x + enemy_half_width > tile_x - half_width and
                        enemy_y - enemy_half_height < tile_y + half_height and
                        enemy_y + enemy_half_height > tile_y - half_height):
                        if enemy.velocity_y <= 0:
                            enemy.y = tile_y + half_height + enemy_half_height
                            enemy.velocity_y = 0
                            return True
        return False
        
#========================== 포탈 충돌처리 ==========================================
    def check_portal_collision(self):
        portal_screen_x = self.portal_x + self.x_offset
        
        player_box = self.player.get_bounding_box()
        portal_box = (
            portal_screen_x - 25,  #l
            self.portal_y - 50,    #b
            portal_screen_x + 25,  #r  
            self.portal_y + 50     #t
        )

        # 충돌 검사
        if (player_box[0] < portal_box[2] and
            player_box[2] > portal_box[0] and
            player_box[1] < portal_box[3] and
            player_box[3] > portal_box[1]):
            self.player.near_portal = True
        else:
            self.player.near_portal = False

def check_collisions():
    for enemy in world.objects[world.layer.enemy]:
        tile_map.check_enemy_collision(enemy)
