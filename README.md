# 2DGP


## 1.게임의 간단한 소개 (카피의 경우 원작에 대한 언급)

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

중급 사냥터 → 상급 사냥터:<br/>
중급 사냥터에 상급 사냥터로 가는 포탈이 있으며, 중급 사냥터 몬스터 박멸시 중급사냥터 포탈이 열립니다.<br/>

보스 사냥터:<br/>
보스 사냥터에서 보스 몬스터를 처치하면 포탈을통해 마을로 돌아가는 전환이 이루어집니다.<br/>

### 3-2: 각 Scene 에 등장하는 GameObject 의 종류 및 구성, 상호작용 <br/>

플레이어: 이동, 점프, 대쉬, 스킬 사용, 장비 변경 가능이 있습니다. <br/>

마을의 NPC: 기본적인 장비 제공, 1차 스킬 제공합니다. <br/>

1차,2차 스테이지 몬스터: 각 사냥터에 스테이지에 맞는 hp 공격력을 설정할 예정입니다. <br/>

보스 스테이지 몬스터: 보스 몬스터의 행동패턴을 추가할 예정입니다. <br/>

스킬창 및 장비창: 스킬 확인 및 장비 변경 기능 추가할 예정입니다. <br/>

포탈: 스테이지를 넘어갈 수 있는 오브젝트입니다. <br/>

### 3-3: 모든 class 에 대한 언급 <br/>

Player: 이동, 스킬, 장비 변경 기능을 포함하고 있습니다.<br/>

Monster: 체력, 공격 패턴을 포함하고 있습니다. <br/>

NPC: 대화 및 기본아이템 지급 기능을 하고있습니다. <br/>

Item: 회복, 장비 등 소유자 관리할 수 있는 아이템 클래스 입니다. <br/>

UI: 체력바,스킬 및 장비창 표시할 수 있는 클래스 입니다. <br/>

Skill: 플레이어 스킬 종류와 스킬 쿨타임을 알 수 있는 클래스입니다. <br/>

Equipment: 장비창에서 플레이어의 장비 상태를 볼 수 있는 클래스입니다. <br/>

GameController: 장면 전환 및 게임 상태 제어 클래스 입니다. <br/>

PhysicsController: 캐릭터와 환경 간 충돌 관리 클래스 입니다. <br/>

SoundController: 효과음 및 배경음 관리를 할 수 있는 클래스입니다.  <br/>

### 3-4: 생김새를 간단한 문장으로 표현  <br/>

기본적인 플레이어는 3등분으로 캐릭터이며 맵은 산업화된 강철 도시 느낌의 맵이고 몬스터 컨셉 역시 철처럼 외형이 단단하게 보이도록 만들 예정입니다. <br/>

### 3-5: 화면에 보이지 않는 Controller 객체들에 대한 언급 <br/>

GameController: 장면 전환, 게임 상태 제어가 있습니다. <br/>

PhysicsController: 캐릭터와 환경 간 충돌 관리를 할 예정입니다. <br/>

SoundController: 효과음 및 배경음 관리가 있습니다. <br/>

GFW: 기본적인 게임 루프, 이벤트 처리, 리소스 로딩을 포함하여 게임 전반적인 흐름을 관리를 할 예정입니다. <br/>

### 3-6: 함수 단위의 설명 (1차발표때는 아직 알 수 없을 것이므로, 2차발표때 추가),사용한/사용할 개발 기법들에 대한 간단한 소개 <br/>

### 3-7: 사용한/사용할 개발 기법들에 대한 간단한 소개 <br/>

상태 패턴: 게임 상태 관리  <br/>

객체 지향 설계: Scene, GameObject 클래스별 분리  <br/>

리소스 캐싱: 이미지, 사운드 캐싱  <br/>

### 3-8: 각 개발 요소들을 정량적으로 제시할 것<br/>

Scene 수: 5개 <br/>

GameObject 종류: 7가지 (Player, Monster, NPC, Item, UI, Skill, Equipment) <br/>

플레이어 스킬: 5개 이상 (1차, 2차 스킬) <br/>

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

사운드 처라 및 장비 ui로 예상됩니다.<br/>

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


    
    
  
