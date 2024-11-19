import gfw.image as image
from pico2d import draw_rectangle
from player import Player

#===============================타일클래스 도입==========================================
class TileMap:
    def __init__(self, tile_images, tile_map_data, tile_size, player):
        self.tile_images = tile_images
        self.tile_map_data = tile_map_data
        self.tile_size = tile_size
        self.x_offset = 0
        self.player = player
# ====================충돌처리를 위한 업데이트 ================
    def update(self):
        self.x_offset = -self.player.x
        self.check_collision()

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
                if tile_index == 1:  # 타일1 일때 
                    tile_x = x * self.tile_size + self.tile_size // 2 + self.x_offset
                    tile_y = y * self.tile_size + self.tile_size // 2
                    half_width = 763 // 2
                    half_height = 320 // 2

                    # 충돌 체크
                    if (player_x - player_half_width < tile_x + half_width and
                        player_x + player_half_width > tile_x - half_width and
                        player_y - player_half_height < tile_y + half_height and
                        player_y + player_half_height > tile_y - half_height):
                        print("충돌 발생!")  # 우선 메세지로 잘되나 확인

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

                    # 타일1에 바운딩 박스 그리기
                    if tile_index == 1:
                        half_width = 763 // 2
                        half_height = 320 // 2
                        draw_rectangle(tile_x - half_width, tile_y - half_height,
                                       tile_x + half_width, tile_y + half_height)

def get_tile_map():
    # 타일 이미지 로드
    tile_images = [
        image.load('tile0.png'),  # 투명블럭
        image.load('tile1.png')   # tile1.png
    ]

    
    tile_map_data = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # (9, 0): 타일1
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],   # (9, 0): 타일1
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]   # (9, 0): 타일1
    ]

    return tile_images, tile_map_data