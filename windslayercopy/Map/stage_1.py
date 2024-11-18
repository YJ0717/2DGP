import gfw.image as image

def get_tile_map():
    
    tile_images = [
        image.load('tile0.png'),  
        image.load('tile1.png'),  # 타일 테스트
        image.load('tile2.png')   
    ]

    tile_map_data = [
        [0, 1, 1, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 1, 1, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    return tile_images, tile_map_data