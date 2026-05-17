# history.md — 요청사항 및 결정사항 변경 이력

변경 이력은 최신순(위)으로 기록한다.

---

## 📅 2026-05-17 16:00:00 (KST)

### 사용자 프롬프트
> memory-bank 업데이트 확인

### AI 처리 결과 요약 (3줄)
1. memory-bank 6종 점검 — `architecture.md` 신규 생성, 누락·순서 문제 보완
2. `progress.md` PyInstaller 수정 이력 통합·최상단 배치, `implementation-plan` Phase 7 추가
3. `codereview`·`testresult`에 exe 빌드 검증(`build.ps1` 성공) 기록 반영

---

## 📅 2026-05-17 15:00:00 (KST)

### 사용자 프롬프트
> ModuleNotFoundError: No module named 'pyautogui' (exe 실행 시)

### AI 처리 결과 요약 (3줄)
1. 빌드 환경(Python 3.13)에 `pyautogui`·`pynput` 미설치로 exe에 미포함된 것이 원인
2. `NaverTimeClickMacro.spec`에 `collect_all` 적용, `build.ps1`로 pip install + 빌드 자동화
3. `pip install -r requirements.txt` 후 재빌드하면 해결

---

## 📅 2026-05-17 14:00:00 (KST)

### 사용자 프롬프트
> 동일한 문제가 발생하고 있어 다시 확인해줘

### AI 처리 결과 요약 (3줄)
1. 빌드 로그·`warn-NaverTimeClickMacro.txt`에서 `ui.app_window`가 **invalid module**로 제외된 것 확인
2. `ui/app_window.py` 166행 `_begin_register` 들여쓰기 오류 수정 (IndentationError)
3. exe 실행 중 빌드 실패(`PermissionError`) 안내 — 종료 후 `pyinstaller NaverTimeClickMacro.spec` 재빌드 필요

---

## 📅 2026-05-17 12:00:00 (KST)

### 사용자 프롬프트
> exe 파일 실행하면 이미지와 같이 계속 에러난다 해결해줘  
> (`No module named 'ui.app_window'`)

### AI 처리 결과 요약 (3줄)
1. `ui/`에 `__init__.py`를 추가해 Python·PyInstaller가 `ui`를 패키지로 인식하도록 수정
2. `NaverTimeClickMacro.spec`에 `pathex`·`collect_submodules('ui')` 및 루트 모듈 hiddenimports 보강
3. `pyinstaller NaverTimeClickMacro.spec`으로 재빌드하면 exe에 `ui.app_window`가 포함됨

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

## [2026-05-17] UI 개선 — 오프셋 입력 방식 변경 및 기능 수정

### 요청사항
1. 오프셋 조정을 슬라이더 대신 숫자 입력 + 버튼 방식으로 변경
2. 클릭 좌표 1개만 등록해도 매크로 시작 버튼 활성화
3. 오프셋 입력 시 일치율 실시간 업데이트
4. 자동 일치율 조정 버튼 추가 → 의미 없다고 판단하여 삭제

### 결정사항
- 슬라이더(`tk.Scale`) 제거, `tk.Entry` + 적용 버튼으로 교체
- Enter 키로도 적용 가능
- 범위 초과 입력 시 자동 클램핑 (-2000~+2000)
- `coordinate.any_registered()` 함수 추가, 기존 `all_registered()` 조건 대체
- `_offset_var.trace_add("write", ...)` 로 타이핑 중 일치율 미리보기

### 변경된 파일
- `ui/app_window.py` — 슬라이더 → 입력 방식 전환, `any_registered()` 적용, 실시간 일치율 미리보기
- `coordinate.py` — `any_registered()` 함수 추가

## [2026-05-17] PyInstaller 배포 설정

### 요청사항
- PyInstaller를 이용한 단독 exe 파일 생성

### 결정사항 (수정됨)
- 초기 빌드: `--onefile --windowed --collect-all ui` → **실패** (`ui.app_window` 모듈 누락)
- 수정된 빌드: `--onefile --windowed --hidden-import "ui" --hidden-import "ui.app_window"` → **성공**
- 로컬 패키지는 `--collect-all` 보다 `--hidden-import` 가 더 확실함
- 콘솔 창 미표시 (`--windowed`)
- 빌드 산출물: `dist/`, `build/`, `*.spec` 을 `.gitignore`에 등록

### 변경된 파일
- `CLAUDE.md` — 배포 섹션 추가 및 수정
- `.gitignore` — `*.spec` 추가
- `dist/NaverTimeClickMacro.exe` — 신규 생성 (9.8 MB, 모듈 완전 포함)

<!-- 새로운 이력은 이 줄 위에 추가 -->
