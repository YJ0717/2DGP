# ================== config.py  프레임 설정
# 걷기, 점프
WALK_FRAME_WIDTH = 45
WALK_FRAME_HEIGHT = 150
WALK_RIGHT_FRAME_WIDTH = 45  # 오른쪽 걷기 프레임 너비
WALK_RIGHT_FRAME_HEIGHT = 150  # 오른쪽 걷기 프레임 높이

# 가만히 있을 때
IDLE_FRAME_WIDTH = 40
IDLE_FRAME_HEIGHT = 150

# 대쉬
DASH_DURATION = 0.3  # 대쉬 지속 시간
DASH_SPEED_MULTIPLIER = 4  # 대쉬 시 속도 배수
DASH_FRAME_COUNT = 3  # 대쉬 애니메이션 프레임 수
KEY_PRESS_INTERVAL = 0.3  # 더블 키 입력 최대 간격
DASH_FRAME_WIDTH = 40  # 대쉬 프레임 너비
DASH_FRAME_HEIGHT = 150  # 대쉬 프레임 높이

# 대쉬 프레임 각각 크기 설정
DASH_FRAME_SIZES = [
    (55, 150),  # 첫 번째 프레임 크기
    (55, 150),  # 두 번째 프레임 크기
    (45, 150)   # 세 번째 프레임 크기
]

# FPS 설정
WALK_FPS = 10
IDLE_FPS = 2
DOUBLE_JUMP_FPS = 2
DASH_FPS = 20  # 대쉬 애니메이션 FPS
PLAYER_DOUBLE_JUMP_FPS = 2

# 플레이어 초기 설정
PLAYER_START_X = 100
PLAYER_START_Y = 100
PLAYER_SPEED = 200
PLAYER_JUMP_SPEED = 10
PLAYER_GRAVITY = -0.5
PLAYER_DASH_COOLDOWN = 1.0
PLAYER_DOUBLE_JUMP_FRAME_COUNT = 2