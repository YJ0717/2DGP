# 2DGP


## 0. 게임 시연 동영상 <br/>
https://youtu.be/tv40mm3bO9A <br/>


## 1.게임의 간단한 소개 (카피의 경우 원작에 대한 언급) <br/>

### 1-A: 윈드슬레이어 (윈드슬레이어 게임(서비스 종료) 모작)<br/>
게임컨셉<br/>
빠른 움직임, 무기와 스킬 간의 절묘한 타이밍이 묘미인 2D 횡스크롤 액션 RPG 게임입니다.<br/>
다양한 퀘스트를 수행하고 일반 몬스터나 보스 몬스터를 잡아 성장하는 게임입니다.
    
### 핵심 메카닉 제시 <br/>
기본적으로 이동,점프,대쉬가 구현되어 있으며 각 클래스는 전사,궁수,무도가,도적,사제가 있습니다.<br/>
스킬은 기본적으로 바람,불,얼음 속성으로 구성되어있으며 각 클래스 마다 1차 전직 2차전직을 통해 속성스킬 외의 클래스에 맞는 전문 기술을 습득할 수 있습니다. 
    
![2](https://github.com/user-attachments/assets/def48069-9c5d-4355-b4c9-1e1f3f72c2c3) 

ㄴ기본적인 공격 방식은 스킬외의 약한공격,강한공격,막기,잡아 밀치기가 존재합니다

![1](https://github.com/user-attachments/assets/f6721fd4-08f1-4775-a31c-5093bc997f43)  

ㄴ기본적인 1차스킬인  바람,불,얼음스킬이 있으며 2차전직을 통해 얻을 수 있는 전문 직업스킬이 있습니다. 

![3](https://github.com/user-attachments/assets/770fbfdd-6b8c-45a6-818f-be0643e17e95)

ㄴ기본적인 조작키 가이드입니다.

![4](https://github.com/user-attachments/assets/251f8250-24b3-4e16-8c6f-1edf92744c46)

ㄴ게임 UI 및 보스몬스터(빨간색) 및 일반몬스터가 존재합니다.

## 2.예상 게임 실행 흐름(간단히 스케치한 그림 사용,게임이 어떤 식으로 진행되는지 직관적으로 알 수 있도록 구성)
2-A:![5](https://github.com/user-attachments/assets/fb9e2914-fb59-47de-973a-b61c07afbe2c)

## 3.개발 내용
    Scene 의 종류 및 구성, 전환 규칙
    각 Scene 에 등장하는 GameObject 의 종류 및 구성, 상호작용
    모든 class 에 대한 언급, 각 클래스의 역할을 나열
    생김새를 간단한 문장으로 표현
    화면에 보이지 않는 Controller 객체들에 대한 언급
    함수 단위의 설명 (1차발표때는 아직 알 수 없을 것이므로, 2차발표때 추가)
    사용한/사용할 개발 기법들에 대한 간단한 소개
    각 개발 요소들을 정량적으로 제시할 것
    프레임워크에서 지원되는 기능들 중 어떤 것을 사용할 것인지
    아직 배우지 않았거나 다루지 않을 항목이 있는지

### 3-1: Scene의 종류 및 구성, 전환 규칙<br/>

시작 화면 → 마을: 시작 화면에서 게임 시작을 선택하면 마을로 이동합니다.<br/>

마을 → 초급 사냥터:<br/>
마을 우측 끝쪽에 초급 사냥터로 가는 포탈이 배치되어 있어, 플레이어가 포탈에 접근하고 상호작용(키 입력) 시 초급 사냥터로 이동합니다.<br/>

초급 사냥터 → 중급 사냥터:<br/>
초급 사냥터에 중급 사냥터로 가는 포탈이 있으며, 초급 사냥터 몬스터 박멸시 중급사냥터 포탈이 열립니다.<br/>

중급 사냥터 → 보스 사냥터:<br/>
중급 사냥터에 보스 사냥터로 가는 포탈이 있으며, 중급 사냥터 몬스터 박멸시 보스 사냥터 포탈이 열립니다.<br/>

보스 사냥터:<br/>
보스 사냥터에서 보스 몬스터를 처치하면 포탈을통해 마을로 돌아가는 전환이 이루어집니다.<br/>

## 3-2: 각 Scene 에 등장하는 GameObject 의 종류 및 구성, 상호작용 <br/>

Main Scene <br/>

###종류 및 구성<br/>

Player: <br/>
플레이어 캐릭터의 이동, 점프, 대쉬, 공격 등의 행동을 관리합니다. <br/>
CustomPlayer는 Player를 상속받아 추가적인 기능을 제공할 수 있습니다. <br/>
Weapon과 MagicAttack을 통해 무기와 마법 공격을 관리합니다. <br/>

Background: <br/>
Background 클래스는 게임의 배경 이미지를 관리합니다. <br/>
배경 이미지를 로드하고, 플레이어의 움직임에 따라 배경을 업데이트합니다. <br/>

MagicAttack: <br/>
MagicAttack 클래스는 플레이어의 마법 공격을 관리합니다. <br/>
공격 이미지 로드, 공격 상태 관리, 투사체 발사 및 업데이트, 그리기 기능을 포함합니다. <br/>

Weapon: <br/>
Weapon 클래스는 플레이어가 장착할 수 있는 무기를 관리합니다. <br/>
무기 이미지 로드, 무기 상태 업데이트, 공격 시작 및 그리기 기능을 포함합니다. <br/>

PlayerUI: <br/>
PlayerUI 클래스는 플레이어의 상태(HP, MP 등)를 화면에 표시합니다. <br/>
UI 요소(HP 바, MP 바, 퀵슬롯 등)를 로드하고 그립니다. <br/>

TileMap: <br/>
게임의 타일맵을 관리 우선적으로 메인 scene에 스테이지 1타일 구현완료 <br/>

WindSkill: <br/>
바람 스킬의 시전 및 투사체를 관리기능을 합니다. <br/>

Projectile: <br/>
스킬 투사체의 위치, 방향, 애니메이션 프레임을 업데이트하고 그립니다..<br/>




###상호작용 <br/>

플레이어와 배경 <br/>
배경은 플레이어의 위치를 기준으로 움직여 시각적 스크롤 효과를 제공합니다. <br/>

플레이어와 무기/마법 공격 <br/>
플레이어는 무기를 장착하거나 마법 공격을 사용하여 적을 공격할 수 있습니다. <br/>
무기와 마법 공격은 플레이어의 입력에 따라 활성화되며, 적과의 충돌을 처리할 수 있습니다. <br/>

플레이어와 UI <br/>
플레이어의 상태 변화(예: HP 감소)에 따라 UI가 업데이트됩니다. <br/>
UI는 플레이어의 현재 상태를 시각적으로 표시합니다. <br/>

플레이어와 타일맵: <br/>
타일맵은 플레이어의 위치를 기준으로 충돌을 감지하여 플레이어의 y축 위치를 조정합니다. <br/>

플레이어와 스킬: <br/>
플레이어는 스킬을 시전하여 투사체를 발사할 수 있습니다. <br/>
스킬은 일정 쿨타임 후에 다시 사용할 수 있으며, 스킬 시전 중에는 다른 행동이 제한될 수 있습니다. <br/>

플레이어와 투사체: <br/>
투사체는 방향에 따라 이동하며, 사거리를 초과하면 제거됩니다. <br/>


1차,2차 스테이지 몬스터: 각 사냥터에 스테이지에 맞는 hp 공격력을 을 만들었습니다. <br/>

보스 스테이지 몬스터: 보스 몬스터의 행동패턴을 추가했습니다. <br/>

스킬창 및 장비창: 스킬 확인 및 장비 변경 기능 추가했습니다. <br/>

포탈: 스테이지를 넘어갈 수 있는 오브젝트입니다. <br/>


### 3-3: 모든 class 에 대한 언급 <br/>

Player:  플레이어 캐릭터의 행동과 상태를 관리하는 클래스입니다. 이동, 점프, 대쉬, 공격 등의 행동을 처리하며, 무기 장착 및 공격 투사체를 관리합니다.<br/>

Monster: 체력, 공격 패턴을 포함하고 있습니다. <br/> 

NPC: 대화 및 기본아이템 지급 기능을 하고있습니다.<br/>

Item: 회복, 장비 등 소유자 관리할 수 있는 아이템 클래스 입니다.  <br/>

PlayerUI : 플레이어의 UI를 관리하는 클래스입니다. HP, MP 바와 퀵슬롯을 그리며, 플레이어의 상태에 따라 UI를 업데이트합니다. <br/>

WindSkill: 바람 스킬의 시전 및 투사체를 관리하는 클래스입니다. <br/>

Weapon: 무기와 관련된 행동을 관리하는 클래스입니다. 무기 이미지 로드, 무기 상태 업데이트, 공격 시작 및 그리기 기능을 포함합니다. <br/>

GameController: 장면 전환 및 게임 상태 제어 클래스 입니다. <br/>

PhysicsController: 캐릭터와 환경 간 충돌 관리 클래스 입니다. <br/>

SoundController: 효과음 및 배경음 관리를 할 수 있는 클래스입니다.  <br/>

CustomPlayer: Player 클래스를 상속받아 커스텀 플레이어를 정의하는 클래스입니다. 기본 Player 클래스의 기능을 확장하거나 수정할 수 있습니다. <br/>

World: 게임 월드를 관리하는 클래스입니다. 여러 레이어로 구성된 객체들을 관리하며, 각 객체의 업데이트와 그리기를 처리합니다. <br/>

AnimSprite:  애니메이션 스프라이트를 관리하는 클래스입니다. 주어진 이미지 파일을 로드하고, 프레임 단위로 애니메이션을 그립니다. <br/>

MagicAttack: 마법 공격을 관리하는 클래스입니다. 공격 이미지 로드, 공격 상태 관리, 투사체 발사 및 업데이트, 그리기 기능을 포함합니다. <br/>

Background: 게임의 배경을 관리하는 클래스입니다. 배경 이미지를 로드하고, 플레이어의 움직임에 따라 배경을 업데이트하고 그립니다. <br/>

Projectile: 스킬의 투사체를 관리하는 클래스입니다.<br/>

World:게임 월드를 관리하는 클래스입니다. 여러 레이어로 구성된 객체들을 관리하며, 각 객체의 업데이트와 그리기를 처리합니다. <br/>

TileMap: 타일맵을 관리하는 클래스입니다. 타일 이미지 로드, 타일 데이터 관리, 충돌 처리 및 타일 그리기 기능을 포함합니다. <br/>

Image: 이미지 캐싱 및 로드를 관리하는 모듈입니다. <br/>

GFW:게임 프레임워크의 핵심 기능을 제공하는 모듈입니다. <br/>



### 3-4: 생김새를 간단한 문장으로 표현  <br/>

기본적인 플레이어는 3등분으로 캐릭터이며 맵은 산업화된 강철 도시 느낌의 맵이고 몬스터 컨셉 역시 철처럼 외형이 단단하게 보이도록 만들 예정입니다. <br/>

### 3-5: 화면에 보이지 않는 Controller 객체들에 대한 언급 <br/>

GameController: 장면 전환, 게임 상태 제어가 있습니다. <br/>

PhysicsController: 캐릭터와 환경 간 충돌 관리를 할 예정입니다. <br/>

SoundController: 효과음 및 배경음 관리가 있습니다. <br/>

GFW: 기본적인 게임 루프, 이벤트 처리, 리소스 로딩을 포함하여 게임 전반적인 흐름을 관리를 할 예정입니다. <br/>

World: 게임 내 객체들을 레이어별로 관리하고, 각 객체의 업데이트와 그리기를 처리합니다. 이는 게임의 상태를 유지하고, 객체 간의 상호작용을 조정하는 역할을 합니다. <br/>

MagicAttack: 공격의 상태와 투사체의 발사를 관리합니다. 공격이 시작되고 끝나는 시점, 투사체의 이동 및 사거리 체크 등을 제어합니다. <br/>

Weapon: 무기 장착 시 플레이어의 공격 행동을 제어합니다. <br/>


## 3-6: 함수 단위의 설명 (1차발표때는 아직 알 수 없을 것이므로, 2차발표때 추가),사용한/사용할 개발 기법들에 대한 간단한 소개 <br/>

### 핵심 함수 단위 설명<br/>

Player 클래스의 handle_event 함수: <br/>
기본적으로 플레이어의 입력 이벤트를 처리하는 함수입니다. <br/>

TileMap 클래스의 check_collision 함수: <br/>
플레이어의 위치를 기준으로 충돌을 감지하여 플레이어의 y축 위치를 조정합니다. <br/>

MagicAttack 클래스의 start_attack 및 start_attack2 함수: <br/>
각각 약한 공격과 강한 공격을 시작하는 함수입니다. 공격 쿨타임을 확인하고, 투사체를 발사합니다. <br/>

WindSkill 클래스의 start_cast 함수: <br/>
바람 스킬의 시전을 시작하는 함수입니다. 스킬 쿨타임을 확인하고, 시전 애니메이션을 시작합니다. <br/>

### 3-7: 사용한/사용할 개발 기법들에 대한 간단한 소개 <br/>

상태 패턴: 게임 상태 관리  <br/>

객체 지향 설계: Player, Weapon, MagicAttack 등의 클래스는 각각의 역할과 책임을 명확히 하여 코드의 유지보수성을 향상시킵니다.  <br/>

리소스 캐싱: 이미지, 사운드 캐싱  <br/>

이벤트 기반 프로그래밍: handle_event 메서드를 통해 키 입력을 처리하고 이에따라 플레이어 행동을 업데이트 합니다. <br/>

게임 루프: gfw 모듈의 start 함수에서 이 루프를 구현하여 게임이 끊임없이 진행되도록 합니다. <br/>

상태 관리: 게임 객체의 상태(예: 플레이어의 이동, 공격 상태)를 관리하여 다양한 행동을 구현합니다. <br/>

모듈화 및 레이어링: gfw.World 클래스와 같은 구조를 사용하여 게임 객체를 레이어별로 관리합니다. <br/>

애니메이션 스프라이트: AnimSprite 클래스를 사용하여 애니메이션을 구현합니다. <br/>

리소스 관리:  gfw.image 모듈에서 이미지 캐싱을 통해 로드가 중복되는 것을 막습니다. <br/>

충돌 처리: TileMap 클래스에서 플레이어와 타일 간의 충돌을 감지하고 처리합니다. <br/>

스킬 및 투사체 관리: WindSkill 클래스와 Projectile 클래스가 추가되어, 스킬 시전과 투사체의 생성, 업데이트, 그리기를 관리합니다. <br/>

상태 및 쿨타임 관리: 스킬과 공격의 쿨타임을 관리하여, 일정 시간 후에 다시 사용할 수 있도록 하는 로직이 추가되었습니다. <br/>

UI 업데이트: 플레이어의 HP와 MP를 시각적으로 표시하도록 하였습니다. <br/>



### 사용할 핵심 개발 기법: 씬 전환 , 몬스터 행동패턴 <br/>


### 3-8: 각 개발 요소들을 정량적으로 제시할 것<br/>

2024/11/11 기준 <br>

클래스 수: 8개 MagicAttack ,Background ,Player ,CustomPlayer, PlayerUI, World, AnimSprite ,Weapon 

총 파일 수: 10개

함수 및 메서드 수: (MagicAttack: 7개), (Background: 3개), (Player: 15개), (CustomPlayer: 1개), (PlayerUI: 3개), (World: 10개 ), (AnimSprite: 2개), (Weapon: 9개)

2024/11/21 기준 <br/>

클래스 수 12개:  MagicAttack,Background,Player,CustomPlayer,PlayerUI,World,AnimSprite,Weapon,WindSkill,Projectile,TileMap,gfw <br/>

총 파일 수 : 11개 

함수 및 매서드 수 : (MagicAttack: 7개), (Background: 3개), (Player: 15개), (CustomPlayer: 1개), (PlayerUI: 3개), (World: 10개), (AnimSprite: 2개), (Weapon: 9개), (WindSkill: 4개), (Projectile: 3개), (TileMap: 4개)

플레이어 스킬: 5개 이상 (2차 스킬) <br/>

NPC 수: 1명 이상 <br/>

몬스터 종류: 3단계 (초급, 중급, 상급/보스) <br/>

장비 슬롯: 무기, 방어구 등 1개 슬롯 <br/>

### 3-9: 프레임워크에서 지원되는 기능들 중 어떤 것을 사용할 것인지 <br/>

게임 루프 관리:<br/>
업데이트 및 렌더링을 효율적으로 처리하기 위해 사용될 것으로 예상됩니다. <br/>

이벤트 처리:<br/>
키 입력, 마우스 클릭 등의 이벤트를 관리하여 플레이어의 조작에 즉각적으로 반응하고 플레이어의 방향키, 대시, 스킬 사용 등의 입력을 처리하는 데 사용될 것 같습니다. <br/>

리소스 로딩:<br/>
이미지, 사운드등 게임에서 사용할 리소스를 쉽게 로딩하고 관리할 거 같습니다. 플레이어 캐릭터의 스프라이트, 배경 이미지, 효과음을 로딩하는 데 활용될 거 같습니다. <br/>

씬 관리:<br/>
여러 씬(마을 등)간의 전환을 쉽게 처리하기 위해 사용될 거 같습니다. 포탈을 통해 씬 간 전환 시, GFW의 씬 관리 기능을 통해 구현하겠습니다. <br/>

충돌 처리: <br/>
GFW는 기본적인 충돌 감지 기능을 제공하기 때문에 캐릭터와 환경 간의 상호작용 효율적으로 처리할 수 있을 거 같습니다.<br/>

애니메이션 관리:<br/>
캐릭터와 몬스터의 애니메이션을 간편하게 관리할 수 있는 기능을 제공하여, 움직임에 따라 적절한 애니메이션을 적용할 수 있게 하겠습니다. <br/>

### 3-10: 아직 배우지 않았거나 다루지 않을 항목이 있는지 <br/>

사운드 처라 및 장비 ui로 예상됩니다. -> 사운드 온라인  수업을 통해 해결 완료 <br/>

## 4.일정 (1차 발표 전까지 수정 가능)<br/>
      10/28 이전에 준비할 사항들을 나열해 본다
      10/28 부터 7주(6.5주)간의 개발 계획을 수립한다
      다른 수업이나 과제, 시험 등을 고려하여 현실적인 계획을 짠다
      수시로 변경되는 것을 수정하며 수정 사유를 함께 기입한다.
      일정 대비 진행 상황을 발표 이후 매주 업데이트한다.
      
### 4-1: 10/28 이전에 준비할 사항들을 나열해 본다 <br/>
리소스 구하기,time.h로 대쉬기능 구현해보기,개발전 임시 설계 작성해보기 <br/>

### 4-2: 개발 계획<br/>
![55555](https://github.com/user-attachments/assets/3d284538-5414-40be-958a-5f4c599f1611)

변경사항: 3주차에 있는 스킬 사용시 충돌처리를 5주차에 있는 몬스터(적) 구현이 완료되면 동시에 진행할 예정 4주차에있는 타일을 이용한 맵 및 1 스테이지로 3주차 구현 대체 즉 앞당김 <br/>

1주차 구현완료 100% <br/>

2주차 스킬과 hud 연동 구현 을 제외한 2주차 전부 구현 100% <br/>

3주차 1차스킬 및 쿨타임 구현완료 2차스킬 및 충돌처리 미구현 충돌처리는 몬스터 구현할때 동시에 진행할 예정  100% <br/>

4주차 1스테이지 구현 완료 사냥터인 2~4스테이지 및 마을 npc 및 대화 구현 100% <br/>

5주차 초급 및 중급몬스터 구현완료 몬스터 행동패턴 구현완료 100% <br/>

6주차 상급몬스터 및 보스몬스터 스테이지 구현완료 100% <br/>

7주차 각 스테이지 전투 및 타이틀 ui 및 게임오버ui 구현완료 사운드 미구현 90% <br/>



##  5.  발표 영상 YouTube link, 1차 발표 전까지의 활동 정리 <br/>

### 5-1: 발표 영상 YouTube link <br/>

1차 발표 <br/>
https://www.youtube.com/watch?v=ph-2jX2EVIM  <br/>

2차 발표 <br/>
https://youtu.be/BgfFkPlnLAM <br/>

3차 발표 <br/>
https://youtu.be/FLh1eqKm5XI <br/>

### 5-2: 1차 발표 전까지의 활동 정리<br/>

리소스 구하기 완료 <br/>

time.h로 대쉬기능 구현해보기 완료 <br/>

개발전 임시 설계 작성해보기 완료 <br/>
    
## 6. 주별 commit 수를 주차별 표로 만들어 포함할 것 <br/>
![20241121_215510](https://github.com/user-attachments/assets/37aa4f1a-682b-459c-a677-fbb01d15959a) <br/>
![insight-commit](https://github.com/user-attachments/assets/d8fb4701-a0a9-4276-86cf-d7f9ae8a459b) <br/>
![commit](https://github.com/user-attachments/assets/77240c3d-8594-4a2a-8063-5284d89a921d) <br/>

## 7. 구현하면서 특히 어려웠던/어려운 부분, 수업에서 추가로 다루었으면 하는 것 <br/>

스킬 구현과 타일 충돌 처리 부분은 예상보다 복잡하고 버그가 많아 어려움을 겪었습니다. 하지만, 이 부분을 성공적으로 구현했기 때문에 앞으로는 스킬 추가나 맵 구현을 보다 빠르게 진행할 수 있을 것 같습니다. <br/>

수업 시간에 기회가 된다면, 장비 착용 시스템에 대해 배우고 싶습니다. 특히, 플레이어 인벤토리에 있는 장비(예: 투구)를 리소스를 하나하나 추가하는 방식이 아닌, 즉각적으로 플레이어 이미지에 장비가 착용되는 기능에 대해 배우고 싶습니다. <br/>


## 1주차 활동정리(10/28~11/3)
플레이어 기본움직임,2단점프,점프,대쉬 구현완료 구현한 내용 애니메이션 적용 완료 <br/>
  
## 2주차 활동정리(11/04~11/10)
플레이어 움직임에 무기 이미지 추가 완료 <br/>
hp,mp 관련 ui추가 퀵슬롯 ui추가 완료 <br/>
s를 누르면 약한공격, d를 누르면 강한공격 행동 애니메이션 추가 완료 <br/>
각 기본공격 투사체 애니메이션 설정 완료 <br/>

## 3주차 활동정리 (11/11~11/17)
타일 및 백그라운드 생성 테스트 완료 기본공격 투사체 버그 수정 완료 <br/>
1차 스킬 구현 완료 <br/>

## 4주차 활동정리 (11/18 ~ 11/25)
맵스테이지 구현 1단계 2단계 마을 및 사냥터 구현완료 <br/>

## 5주차 활동정리 (11/26 ~ 12/2)
초급 몬스터 중급몬스터 구현완료 각 몬스터 행동설정 완료 <br/>

## 6주차 활동정리 (12/03 ~ 12/10)
상급 몬스터 및 보스몬스터 5스테이지 구현완료 보스행동패턴 구현완료 <br/>

## 7주차 활동정리 (12/11 ~ 12/12)
버그 수정 및 ui 도입 완료 <br/>


# 3차발표 

## 게임에 대한 간단한 소개 <br/>

윈드슬레이어는 2D 횡스크롤 MMORPG로, 캐릭터를 조작해 몬스터를 사냥하고 스킬을 사용하며 다양한 스테이지를 클리어하는 게임입니다. <br/>
메이플스토리와 비슷한 스타일이지만, 더 빠른 전투 템포와 아기자기한 그래픽이 특징입니다. <br/>


## 개발 계획/일정/실제 진행 <br/>

![커밋](https://github.com/user-attachments/assets/6624974a-9e30-4600-9b7d-3aab9f74acb7) <br/>

![커밋2](https://github.com/user-attachments/assets/58db4b0d-dd3a-47d0-8197-62c99f48eb1f) <br/>

 4-2: 개발 계획<br/>
![55555](https://github.com/user-attachments/assets/3d284538-5414-40be-958a-5f4c599f1611)

1주차 구현완료 100% <br/>

2주차 스킬과 hud 연동 구현 을 제외한 2주차 전부 구현 100% <br/>

3주차 1차스킬 및 쿨타임 구현완료 2차스킬 및 충돌처리 미구현 충돌처리는 몬스터 구현할때 동시에 진행할 예정  100% <br/>

4주차 1스테이지 구현 완료 사냥터인 2~4스테이지 및 마을 npc 및 대화 구현 100% <br/>

5주차 초급 및 중급몬스터 구현완료 몬스터 행동패턴 구현완료 100% <br/>

6주차 상급몬스터 및 보스몬스터 스테이지 구현완료 100% <br/>

7주차 각 스테이지 전투 및 타이틀 ui 및 게임오버ui 구현완료 사운드 미구현 90% <br/>

### 1주차 활동정리(10/28~11/3)
플레이어 기본움직임,2단점프,점프,대쉬 구현완료 구현한 내용 애니메이션 적용 완료 <br/>
  
### 2주차 활동정리(11/04~11/10)
플레이어 움직임에 무기 이미지 추가 완료 <br/>
hp,mp 관련 ui추가 퀵슬롯 ui추가 완료 <br/>
s를 누르면 약한공격, d를 누르면 강한공격 행동 애니메이션 추가 완료 <br/>
각 기본공격 투사체 애니메이션 설정 완료 <br/>

### 3주차 활동정리 (11/11~11/17)
타일 및 백그라운드 생성 테스트 완료 기본공격 투사체 버그 수정 완료 <br/>
1차 스킬 구현 완료 <br/>

### 4주차 활동정리 (11/18 ~ 11/25)
맵스테이지 구현 1단계 2단계 마을 및 사냥터 구현완료 <br/>

### 5주차 활동정리 (11/26 ~ 12/2)
초급 몬스터 중급몬스터 구현완료 각 몬스터 행동설정 완료 <br/>

### 6주차 활동정리 (12/03 ~ 12/10)
상급 몬스터 및 보스몬스터 5스테이지 구현완료 보스행동패턴 구현완료 <br/>

### 7주차 활동정리 (12/11 ~ 12/12)
버그 수정 및 ui 도입 완료 <br/>

## 사용된 기술 <br/>
객체지향 프로그래밍(OOP) <br/>

상속을 통한 코드 재사용 <br/>

캡슐화를 통한 데이터 은닉과 접근 제어 <br/>

다형성을 활용한 인터페이스 구현 <br/>

상태 패턴 <br/>

캐릭터의 상태를 열거형으로 관리 (IDLE, WALK, ATTACK, HIT, DEAD) <br/>

각 상태별 애니메이션과 동작 구현 <br/>

충돌 감지 시스템 <br/>

AABB충돌 검사 구현 <br/>

타일맵 충돌, 적 충돌, 투사체 충돌 등 다양한 충돌 처리 <br/>

프레임워크 설계 <br/>

gfw 모듈을 통한 게임 프레임워크 구현 <br/>

월드 객체를 통한 게임 오브젝트 관리 <br/>

레이어 시스템을 통한 렌더링 순서 제어 <br/>

리소스 관리 <br/>

## 참고한 것들 <br/>

파이썬 게임 프로그래밍 기법 (pico2d) <br/>

스프라이트 기반 애니메이션 <br/>

이벤트 처리 시스템 <br/>

타일맵 시스템 <br/>

타일 충돌 처리 <br/>

## 수업내용에서 차용한 것 <br/>

게임 프레임워크 (gfw) <br/>

이미지 캐싱 시스템 <br/>

게임 상태 관리 <br/>

씬 전환 시스템 <br/>

게임 루프 구조 <br/>

update/draw 분리 <br/>

이벤트 처리 시스템 <br/>

충돌 처리 시스템 <br/>

AABB 충돌 박스 구현 <br/>

충돌 이벤트 처리 <br/>

레이어 시스템 <br/>

월드 객체를 통한 게임 오브젝트 관리 <br/>

## 직접 개발한 것 <br/>

스킬 시스템 <br/>

각 스킬별 고유한 투사체와 이펙트 <br/>

스킬 쿨타임 시스템 <br/>

스킬별 상태이상 효과 (빙결, 화상 등) <br/>

몬스터 행동 패턴 <br/>

기본 몬스터부터 보스까지 5가지 타입 구현 <br/>

몬스터별 고유한 공격 패턴 (원거리 근거리) <br/>

플레이어 추적 및 공격 범위 설정 <br/>

피격 및 사망 처리 <br/>

UI 시스템 <br/>

HP/MP바 구현 <br/>

스킬 쿨타임 표시 <br/>

포션 시스템 <br/>

퀵슬롯 구현 <br/>

스테이지 시스템 <br/>

5개의 스테이지 맵 디자인(포탈을 통한 스테이지 이동) <br/>

NPC 대화 시스템 <br/>

전투 시스템 (기본 공격과 스킬 공격 구현) <br/>

데미지 계산 시스템(히트박스 및 충돌 처리) <br/>

무적 시간 구현 <br/>

캐릭터 시스템 (이동, 점프, 대시 구현) <br/>

애니메이션 상태 관리 <br/>

무기 장착 시스템 <br/>

포션 회복 시스템 <br/>

 
## 아쉬운 것 <br/>
사운드를 못넣은게 아쉽습니다 <br/>
보스의 행동 패턴을 더 확장하지 못한게 아쉽습니다. <br/>

## 하고 싶었지만 못 한 것들 <br/>

행렬 변환을 통한 장비 렌더링 시스템 <br/>
pico2d는 clip_composite_draw() 함수만 제공하여 복잡한 행렬 변환 구현이 어렵다고 느꼈습니다. <br/>

더 정확한 충돌처리: 바운딩 박스를 여러 개의 작은 박스로 깎아서 더 정확한 충돌 영역을 만드는 작업에 많은 시간이 소요될 것으로 예상되어 하지 못했습니다. <br/>

## (앱을 스토어에 판다면) 팔기 위해 보충할 것들 <br/>

멀티 플레이 지원 ,  다양한 직업군 선택, 아바타 꾸미기 <br/>

## 기말 프로젝트를 하면서 겪은 어려움 <br/>

투사체 충돌 처리 시스템을 구현하면서 의존성 주입 문제를 겪었습니다. <br/>

기존 몬스터들(근접공격)은 world에 등록되어 자동으로 충돌 처리가 되었지만, 투사체는 단순 데이터로 존재하여 world에서 충돌 처리가 되지 않았습니다. <br/>

이를 해결하기 위해 의존성 주입(객체를 외부에서 주입하는 방식)을 사용해야 했는데, 성급한 마음과 코드를 꼼꼼하게 읽지 못해 상당한 시간이 소요되었습니다. <br/>

## 수업에 대한 내용 <br/>
### 이번 수업에서 기대한 것  <br/>

파이썬을 활용한 게임 개발 경험 <br/>

### 얻은 것 <br/> 

게임 프레임워크의 구조와 작동 원리 이해 <br/>

객체지향 프로그래밍의 실전 적용 경험 <br/>

### 얻지 못한 것 <br/>

이전 프로젝트보다 하드코딩을 줄이고 싶었으나, 후반부에 갈 수록 시간이 없어 하드코딩이을 많이 했습니다. <br/>

## 지인평점 <br/>
9/10  <br/>


## 후기 <br/>

게임 개발 계획을 구체적으로 세우는 것은 성공적인 프로젝트를 위한 중요한 단계이다. <br/>

실제로 내가 게임 개발을 진행할 때, 스킬이나 공격 모션을 먼저 개발하는 대신 몬스터를 먼저 제작했더라면 시간을 좀 더 절약할 수 있었을 것이다. <br/>

이렇게 했다면 장비 장착과 같은 게임의 재미 요소를 추가할 여유가 생겼을 텐데, 이를 놓친 것이 아쉽다. <br/>

하지만 이번 경험을 통해 더 효율적인 개발 방식을 배웠으니, 앞으로의 프로젝트에서는 더욱 나은 결과를 기대할 수 있을 것이다. <br/>

## exe파일 생성 <br/>

윈s 모작파일 다운 후 exe파일 실행 <br/>