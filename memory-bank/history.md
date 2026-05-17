# history.md — 요청사항 및 결정사항 변경 이력

변경 이력은 최신순(위)으로 기록한다.

---

## [2026-05-17] 프로젝트 초기 설정

### 요청사항
- `design.md` 파일 리뷰 및 구조화
- `design_original.md` 에 원본 보존
- memory-bank 하위 운영 문서 6종 생성
  - `AGENTS.md`, `history.md`, `implementation-plan.md`, `progress.md`, `codereview.md`, `testresult.md`

### 결정사항
- 기술 스택: Python 3.10+, tkinter, pyautogui, pynput, requests (design.md 기준 확정)
- 모듈 분리: `main.py`, `time_sync.py`, `coordinate.py`, `clicker.py`, `ui/app_window.py`
- Z 키 전역 감지에 `pynput` 사용 (포커스 무관)
- 정밀 대기 전략: 목표 시각 50ms 전까지 sleep, 이후 busy-wait

### 변경된 파일
- `memory-bank/design.md` — 초안 → 구조화된 설계 문서로 개선
- `memory-bank/design_original.md` — 원본 초안 보존 (신규 생성)
- `memory-bank/AGENTS.md` — 신규 생성
- `memory-bank/history.md` — 신규 생성 (본 파일)
- `memory-bank/implementation-plan.md` — 신규 생성
- `memory-bank/progress.md` — 신규 생성
- `memory-bank/codereview.md` — 신규 생성
- `memory-bank/testresult.md` — 신규 생성

---

## [2026-05-17] GitHub 저장소 및 PR 생성

### 요청사항
- GitHub 퍼블릭 저장소 생성 및 코드 push
- develop → main PR 생성 (Draft)

### 결정사항
- 저장소: https://github.com/rorabeat/NaverTimeClickMacro (Public)
- 브랜치 전략: `main` (안정) ← `develop` (개발) ← `feature/*` (기능)
- `.gitignore`: `__pycache__/`, `.claude/`, `.venv/` 등 제외

### 변경된 파일
- `.gitignore` — 신규 생성
- `memory-bank/history.md` — 본 항목 추가

<!-- 새로운 이력은 이 줄 위에 추가 -->
