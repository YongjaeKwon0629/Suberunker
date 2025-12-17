# 💩 똥피하기 (PoopDodge) - SUBERUNKER Style

---
추억의 플래시 게임 졸라맨 똥피하기(SUBERUNKER)를 완벽하게 재해석한 파이썬 기반 아케이드 게임입니다.
하늘에서 비처럼 쏟아지는 똥을 피하고 최대한 오래 살아남으세요!
---

## 🎮 게임 특징 (Features)

*   **🕹️ 쫄깃한 조작감**: 졸라맨 특유의 미끄러지는 듯한 관성(Friction) 이동 완벽 구현
*   **💩 장인정신 비주얼**: 단순 동그라미가 아닌, 코드로 직접 그린 **3단 또아리 똥** 그래픽
*   **🔥 4단계 난이도 시스템**:
    *   **Easy**: 초보자를 위한 산책 모드
    *   **Normal**: 적당한 긴장감
    *   **Hard**: 빠른 속도의 도전 모드
    *   **HELL**: **지옥 모드** (극한의 탄막 슈팅 경험)
*   **⚡ Standalone EXE**: 파이썬이 없는 컴퓨터에서도 즉시 실행 가능
---
## 🛠️ 기술 스택 (Tech Stack)

*   **Language**: Python 3.12
*   **Engine**: PyGame 2.6.1
*   **Build Tool**: PyInstaller (for .exe generation)
*   
---
## 🚀 실행 방법 (How to Run)

### 방법 1. 실행 파일로 즐기기 (추천)
별도의 설치 과정 없이 바로 게임을 즐길 수 있습니다.
1. `dist` 폴더로 이동합니다.
2. **`PoopDodge.exe`** 파일을 더블 클릭합니다.

### 방법 2. 소스 코드로 실행하기 (개발자용)
파이썬 환경이 설치되어 있다면 코드를 직접 수정하고 실행할 수 있습니다.

```bash
# 1. 필수 라이브러리 설치
pip install pygame

# 2. 게임 실행
python game.py
```

### 방법 3. 직접 빌드하기 (EXE 만들기)
소스를 수정한 후 다시 EXE 파일로 만들고 싶다면:

```bash
# PyInstaller 설치
pip install pyinstaller

# 빌드 명령어
python -m PyInstaller --onefile --noconsole --name "PoopDodge" game.py
```

----
## 🕹️ 조작법 (Controls)

| 키 (Key) | 동작 (Action) |
| :---: | :--- |
| **← (Left Arrow)** | 왼쪽으로 이동 (계속 누르면 가속) |
| **→ (Right Arrow)** | 오른쪽으로 이동 (계속 누르면 가속) |
| **마우스 클릭** | 메뉴 선택 (난이도, 재시작) |
---
## 📦 프로젝트 구조 (Directory Structure)

```
main/
├── game.py            # 게임 메인 소스 코드 (All-in-One)
├── README.md          # 프로젝트 설명서
└── dist/
    └── PoopDodge.exe  # 배포용 실행 파일
```
*Created with ❤️ using Python & PyGame*
---

## 민첩한 하루 되세요~!
