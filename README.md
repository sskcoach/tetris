# Tetris

Gemini CLI 강의 실습 프로젝트 - 터미널 기반 테트리스 게임

## 강의 정보

이 프로젝트는 Gemini CLI 강의의 실습 예제입니다.

**강의 링크**: [https://inf.run/bQJ6F](https://inf.run/bQJ6F)

**개발 히스토리**: [HISTORY.md](./HISTORY.md)

## 실행 방법

```bash
python3 tetris.py
```

## 조작법

| 키 | 동작 |
|-----|--------|
| ← → | 좌우 이동 |
| ↑ | 회전 |
| ↓ | 소프트 드롭 |
| Space | 하드 드롭 |
| Q | 메뉴로 |

## 요구 사항

- Python 3.x

### 플랫폼별 BGM 재생

| 플랫폼 | 재생 방식 | 비고 |
|--------|----------|------|
| macOS | `afplay` | 기본 설치됨 |
| Windows | `winsound` | Python 내장 모듈 |
| Linux | `aplay` / `paplay` | ALSA 또는 PulseAudio 필요 |

## 프로젝트 구조

```
src/
├── tetris.py           # 메인 게임
├── leaderboard.txt     # 점수 기록
├── music/
│   ├── __init__.py
│   └── tetris_bgm.py   # BGM 모듈 (Korobeiniki 테마)
└── README.md
```

## BGM

게임 플레이 중 자동으로 배경음악이 재생됩니다.

### 독립 실행

```bash
# 기본 재생
python3 music/tetris_bgm.py

# 베이스 라인 포함
python3 music/tetris_bgm.py --bass

# 루프 재생
python3 music/tetris_bgm.py --loop

# 시각화
python3 music/tetris_bgm.py --visual --bass
```

`q` 키로 재생 중지.

### Windows 참고사항

- `winsound` 모듈 사용 (Python 기본 내장)
- WAV 파일 생성 후 재생
- 임시 파일 위치: `%TEMP%\tetris_*.wav`

## Credits

- BGM: [NXT_tunes/tetris](https://github.com/lambdaloop/NXT_tunes/tree/master/tetris)
