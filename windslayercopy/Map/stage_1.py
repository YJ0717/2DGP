from pico2d import *  
import gfw
import gfw.image as image
from pico2d import draw_rectangle
from player import Player

bb_width = 763
bb_height = 280

#===============================타일클래스 도입==========================================
class TileMap:
    def __init__(self, tile_images, tile_map_data, tile_size, player):
        self.tile_images = tile_images
        self.tile_map_data = tile_map_data
        self.tile_size = tile_size
        self.x_offset = 0
        self.player = player
        #===============================포탈 도입==========================================
        self.portal_image = image.load('portal.png')  
        self.portal_animation_frame = 0  
        self.portal_animation_speed = 10  
        #===============================NPC 도입==========================================
        self.npc_image = image.load('npc_01.png')  # NPC 이미지 로드
        self.npc_x = 1000  # 실제 게임상의 좌표에서는 500  x_offset을 더하기때문에 
        self.npc_y = 250  
        self.npc_frame = 0
        self.npc_frame_count = 3  
        self.npc_frame_width = 50  
        self.npc_frame_height = 180  
        self.npc_fps = 2 
        self.npc_time = 0

        
        self.npc_collision_x = 500
        self.npc_collision_y = 232  

        self.talk_image = image.load('npc_talk1.png')

        #===============================두 번째 NPC 도입==========================================
        self.npc2_image = image.load('npc_02.png')  # 두 번째 NPC 이미지 로드
        self.npc2_x = 2000  # 두 번째 NPC의 x 좌표
        self.npc2_y = 250  # 두 번째 NPC의 y 좌표
        self.npc2_frame = 0
        self.npc2_frame_count = 3
        self.npc2_frame_width = 87
        self.npc2_frame_height = 160
        self.npc2_fps = 2
        self.npc2_time = 0

        self.npc2_collision_x = 1000
        self.npc2_collision_y = 232

        self.talk2_image = image.load('npc_talk2.png')  # 두 번째 NPC의 말풍선 이미지 로드

# ====================충돌처리 및 애니메이션을 위한 업데이트 ================
    def update(self):
        self.x_offset = -self.player.x  
        self.check_collision()
        self.update_portal_animation()  
        self.update_npc_animation()
        self.update_npc2_animation()

    def update_portal_animation(self):
        self.portal_animation_frame += gfw.frame_time * self.portal_animation_speed
        if self.portal_animation_frame >= 4:  # 애니메션 프레임 수에 따라 조정
            self.portal_animation_frame = 0

    def update_npc_animation(self):
        self.npc_time += gfw.frame_time
        self.npc_frame = int(self.npc_time * self.npc_fps) % self.npc_frame_count

    def update_npc2_animation(self):
        self.npc2_time += gfw.frame_time
        self.npc2_frame = int(self.npc2_time * self.npc2_fps) % self.npc2_frame_count

#======================== 충돌처리 ======================
    def check_collision(self):
        player_x = self.player.x
        player_y = self.player.y
        player_half_width = self.player.width // 2
        player_half_height = self.player.height // 2

        for y in range(len(self.tile_map_data)):
            row = self.tile_map_data[y]
            for x in range(len(row)):
                tile_index = row[x]
                if tile_index == 1:  #타일 1이미지 
                    tile_x = x * self.tile_size + self.tile_size // 2 + self.x_offset
                    tile_y = y * self.tile_size + self.tile_size // 2
                    half_width = bb_width // 2
                    half_height = bb_height // 2

                    # 충돌 체크
                    if (player_x - player_half_width < tile_x + half_width and
                        player_x + player_half_width > tile_x - half_width and
                        player_y - player_half_height < tile_y + half_height and
                        player_y + player_half_height > tile_y - half_height):
                        # 플레이어가 타일 위에 서 있도록 위치 조정

                        if self.player.velocity_y <= 0:  
                            self.player.y = tile_y + half_height + player_half_height  
                            self.player.velocity_y = 0  
                            
                        #================ player.py의 변수를 가져와서 행동을 유지하도록 함================
                            self.player.can_move = True  
                            self.player.can_double_jump = True  
                            self.player.is_jumping = False  
                            self.player.current_image = self.player.idle_image  

        # 포탈 근처에 있는지 확인
        portal_x = 2400 + self.x_offset
        portal_y = 230
        half_width = self.portal_image.w // 8
        half_height = self.portal_image.h // 2

        if (player_x - player_half_width < portal_x + half_width and
            player_x + player_half_width > portal_x - half_width and
            player_y - player_half_height < portal_y + half_height and
            player_y + player_half_height > portal_y - half_height):

            if self.player.weapon_equipped:  # 무기를 장착했을때만 포탈이동 
                self.player.near_portal = True
            else:
                self.player.near_portal = False
        else:
            self.player.near_portal = False

        # ================== NPC와의 충돌 체크 =======================
        npc_half_width = self.npc_frame_width // 2
        npc_half_height = self.npc_frame_height // 2
        if (player_x - player_half_width < self.npc_collision_x + npc_half_width and
            player_x + player_half_width > self.npc_collision_x - npc_half_width and
            player_y - player_half_height < self.npc_collision_y + npc_half_height and
            player_y + player_half_height > self.npc_collision_y - npc_half_height):
            self.player.near_npc = True
        else:
            self.player.near_npc = False

        # ================== 두 번째 NPC와의 충돌 체크 =======================
        npc2_half_width = self.npc2_frame_width // 2
        npc2_half_height = self.npc2_frame_height // 2
        if (player_x - player_half_width < self.npc2_collision_x + npc2_half_width and
            player_x + player_half_width > self.npc2_collision_x - npc2_half_width and
            player_y - player_half_height < self.npc2_collision_y + npc2_half_height and
            player_y + player_half_height > self.npc2_collision_y - npc2_half_height):
            self.player.near_npc2 = True
        else:
            self.player.near_npc2 = False

#======================== 타일 그리기 ======================
    def draw(self):
        for y in range(len(self.tile_map_data)):
            row = self.tile_map_data[y]
            for x in range(len(row)):
                tile_index = row[x]
                if tile_index >= 0:
                    tile_image = self.tile_images[tile_index]
                    tile_x = x * self.tile_size + self.tile_size // 2 + self.x_offset
                    tile_y = y * self.tile_size + self.tile_size // 2
                    tile_image.draw(tile_x, tile_y)

        
        portal_x = 2400 + self.x_offset  # 플레이어의 x_offset을 추가야만 포탈이 고정된 위치에 존재
        portal_y = 230   
        self.portal_image.clip_draw(
            int(self.portal_animation_frame) * self.portal_image.w // 4, 0,
            self.portal_image.w // 4, self.portal_image.h,
            portal_x, portal_y
        )

        # ==========================포탈 바운딩 박스 그리기==========================
        half_width = self.portal_image.w // 8 
        half_height = self.portal_image.h // 2 
        draw_rectangle(portal_x - half_width, portal_y - half_height,
                       portal_x + half_width, portal_y + half_height)  

        npc_x_offset = self.npc_frame * self.npc_frame_width
        self.npc_image.clip_draw(npc_x_offset, 0, self.npc_frame_width, self.npc_frame_height,
                                 self.npc_x + self.x_offset, self.npc_y)

        # 말풍선 
        if self.player.near_npc:
            self.talk_image.draw(self.npc_x + self.x_offset, self.npc_y + self.npc_frame_height + 20)

        npc2_x_offset = self.npc2_frame * self.npc2_frame_width
        self.npc2_image.clip_draw(npc2_x_offset, 0, self.npc2_frame_width, self.npc2_frame_height,
                                  self.npc2_x + self.x_offset, self.npc2_y)

        # 두 번째 NPC의 말풍선
        if self.player.talk_to_npc2:
            self.talk2_image.draw(self.npc2_x + self.x_offset, self.npc2_y + self.npc2_frame_height + 20)

def get_tile_map():
    # 타일 이미지 로드
    tile_images = [
        image.load('tile0.png'),  # 투명블럭
        image.load('tile1.png')   # tile1.png
    ]

    
    tile_map_data = [
        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]
    ]

    return tile_images, tile_map_data