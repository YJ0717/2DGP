# ================== 각종 애니메이션 프레임처리 ================== 
# 걷기
WALK_FRAME_WIDTH = 45
WALK_FRAME_HEIGHT = 150
WALK_RIGHT_FRAME_WIDTH = 45
WALK_RIGHT_FRAME_HEIGHT = 150

# 가만히 있을 때
IDLE_FRAME_WIDTH = 40
IDLE_FRAME_HEIGHT = 150

# 대쉬 프레임 조절
DASH_DURATION = 0.3
DASH_SPEED_MULTIPLIER = 4
DASH_FRAME_COUNT = 3
KEY_PRESS_INTERVAL = 0.3
DASH_FRAME_WIDTH = 40
DASH_FRAME_HEIGHT = 150

# 대쉬 프레임 각각 크기 설정
DASH_FRAME_SIZES = [
    (55, 150),
    (55, 150),
    (45, 150)
]

# ========================= FPS 설정 =========================
WALK_FPS = 10
IDLE_FPS = 2
DOUBLE_JUMP_FPS = 2
DASH_FPS = 20
PLAYER_DOUBLE_JUMP_FPS = 2

# ========================= 공격 애니메이션 설정 =========================
ATTACK_FPS = 10
ATTACK_FRAME_COUNT = 4
ATTACK_FRAME_WIDTH = 101
ATTACK_FRAME_HEIGHT = 200
ATTACK_DURATION = 0.3
ATTACK_COOLDOWN = 1

# ========================= 두 번째 공격 애니메이션 설정 =========================
SECOND_ATTACK_FPS = 4
SECOND_ATTACK_FRAME_COUNT = 4
SECOND_ATTACK_FRAME_WIDTH = 101
SECOND_ATTACK_FRAME_HEIGHT = 200
SECOND_ATTACK_DURATION = 0.5
SECOND_ATTACK_COOLDOWN = 1.5

# ========================= 플레이어 속성 설정 =========================
PLAYER_START_X = 100
PLAYER_START_Y = 400 # y값 수정
PLAYER_SPEED = 200
PLAYER_JUMP_SPEED = 10
PLAYER_GRAVITY = -0.5
PLAYER_DASH_COOLDOWN = 1.0
PLAYER_DOUBLE_JUMP_FRAME_COUNT = 2

# ========================= S를 누를때 약한공격 애니메이션 설정 =========================
B_ATTACK1_FRAME_COUNT = 15
B_ATTACK1_FRAME_WIDTH = 60
B_ATTACK1_FRAME_HEIGHT = 150
B_ATTACK1_FPS = 10
B_ATTACK1_MAX_RANGE = 150 #공격사거리

# ========================= D를 누를때 강한공격 애니메이션 설정 =========================
B_ATTACK2_FRAME_COUNT = 13
B_ATTACK2_FRAME_WIDTH = 60
B_ATTACK2_FRAME_HEIGHT = 150
B_ATTACK2_FPS = 6
B_ATTACK2_MAX_RANGE = 200


# ========================= 무기 착용 시 프레임 크기 설정 =========================

# =======왼쪽 걷기====================
WEAPON_WALK_FRAME_WIDTH = 85
WEAPON_WALK_FRAME_HEIGHT = 180
WEAPON_WALK_FPS = 8
WEAPON_WALK_FRAME_COUNT = 5

# =======가만히 있을 때 ==========
WEAPON_IDLE_FRAME_WIDTH = 173
WEAPON_IDLE_FRAME_HEIGHT = 150
WEAPON_IDLE_FPS = 2
WEAPON_IDLE_FRAME_COUNT = 2

# =======대쉬====================
WEAPON_DASH_FRAME_WIDTH = 85
WEAPON_DASH_FRAME_HEIGHT = 180
WEAPON_DASH_FPS = 20
WEAPON_DASH_FRAME_COUNT = 6

# =======점프====================
WEAPON_JUMP_FRAME_WIDTH = 140
WEAPON_JUMP_FRAME_HEIGHT = 240
WEAPON_JUMP_FPS = 1
WEAPON_JUMP_FRAME_COUNT = 1

# 더블 점프 관련 설정
WEAPON_DOUBLE_JUMP_FRAME_WIDTH = 53
WEAPON_DOUBLE_JUMP_FRAME_HEIGHT = 150
WEAPON_DOUBLE_JUMP_FPS = 2
WEAPON_DOUBLE_JUMP_FRAME_COUNT = 2

#===================================================스킬 시전 설정===================================================


# ========================= 바람 스킬시전 행동  =========================
WIND_CAST_FRAME_COUNT = 4
WIND_CAST_FRAME_WIDTH = 140
WIND_CAST_FRAME_HEIGHT = 230
WIND_CAST_FPS = 8
WIND_CAST_DURATION = 0.5
#============= 바람 스킬 투사체 관련 설정 =========================
WIND_SKILL_FRAME_COUNT = 3
WIND_SKILL_FRAME_WIDTH = 105
WIND_SKILL_FRAME_HEIGHT = 140
WIND_SKILL_FPS = 3
WIND_SKILL_DURATION = 3
WIND_SKILL_SPEED = 600
WIND_SKILL_MAX_RANGE = 400  #바람스킬 최대 사거리
WIND_SKILL_COOLDOWN = 2.0  #바람스킬 쿨타임

# ========================= 얼음 스킬 시전 설정 =========================
ICE_CAST_FRAME_COUNT = 4
ICE_CAST_FRAME_WIDTH = 140
ICE_CAST_FRAME_HEIGHT = 230
ICE_CAST_FPS = 8
ICE_CAST_DURATION = 0.5

# ============= 얼음 스킬 투사체 관련 설정 =========================
ICE_SKILL_FRAME_COUNT = 1
ICE_SKILL_FRAME_WIDTH = 57
ICE_SKILL_FRAME_HEIGHT = 67
ICE_SKILL_FPS = 3
ICE_SKILL_SPEED = 600
ICE_SKILL_MAX_RANGE = 400
ICE_SKILL_COOLDOWN = 2.0



