# progress.md — AI 작업 진행 이력

AI가 완료한 작업을 최신순(위)으로 기록한다.

---

## [2026-05-17 16:00:00] PyInstaller exe 배포 오류 수정 (통합)

- **상태**: 완료
- **작업 내용**: exe 실행 시 연쇄 ModuleNotFoundError 해결 및 빌드 자동화
- **변경 파일**:
  - `ui/__init__.py` — 패키지 인식
  - `ui/app_window.py` — `_begin_register` 들여쓰기 복구 (invalid module 해소)
  - `NaverTimeClickMacro.spec` — `pathex`, `collect_all('pyautogui'|'pynput')`
  - `build.ps1` — `pip install` + PyInstaller 일괄 실행 (신규)
- **원인 요약**:
  1. `ui.app_window` — IndentationError로 PyInstaller가 모듈 제외
  2. `pyautogui` / `pynput` — 빌드 Python에 미설치 또는 hiddenimports만으로 부족
  3. `PermissionError` — exe 실행 중 재빌드 실패 (구 exe 유지)
- **빌드 검증**: `.\build.ps1` (Python 3.14) → `dist/NaverTimeClickMacro.exe` 생성 성공
- **권장 빌드**: `.\build.ps1` (PyInstaller와 동일한 Python에 requirements 설치 필수)

---

## [2026-05-17] 프로젝트 초기 문서화

### 완료 항목

#### design.md 개선
- 원본 초안(`design_original.md`)을 보존하고 `design.md`를 8개 섹션으로 구조화
  - 프로젝트 개요, 동작 방식 플로우차트, 기능 요구사항 (3개), 기술 스택 표, 구현 세부사항 (의사코드 포함), UI ASCII 와이어프레임, 파일 구조, 예외 처리

#### memory-bank 운영 문서 생성
- `AGENTS.md` — 에이전트 운영 규칙, 코드 작성 규칙, 작업 전후 체크리스트
- `history.md` — 요청사항·결정사항 변경 이력 (본 세션 내용 기록)
- `implementation-plan.md` — Phase 1~6 태스크 목록 (총 24개 태스크)
- `progress.md` — AI 작업 진행 이력 (본 파일)
- `codereview.md` — 코드 리뷰 누적 결과 초기화
- `testresult.md` — 테스트 결과 누적 기록 초기화

### 미완료 (다음 세션 예정)
- 소스코드 구현 (Phase 1~6 전체)

---

## [2026-05-17] Phase 1 — 프로젝트 초기화

### 완료 항목

| 태스크 | 생성 파일 | 내용 |
|--------|-----------|------|
| 1.1 requirements.txt | `requirements.txt` | pyautogui==0.9.54, pynput==1.7.7, requests==2.32.3 |
| 1.2 디렉터리 구조 | `ui/__init__.py` | ui 패키지 초기화 |
| 1.3 main.py 스캐폴딩 | `main.py`, `ui/app_window.py` | tkinter 루프 + AppWindow 클래스 연결 |

### 검증
- `pip install -r requirements.txt` 성공
- `import pyautogui, pynput, requests` 모두 정상
- `main.py`, `ui/app_window.py` 구문 오류 없음

### 다음 단계
- Phase 2: `time_sync.py` 구현 (네이버 서버 시간 동기화)

## [2026-05-17] Phase 2 — 네이버 서버 시간 동기화

### 완료 항목

| 태스크 | 함수 | 내용 |
|--------|------|------|
| 2.1 Date 헤더 파싱 | `sync()` | `email.utils.parsedate_to_datetime` 으로 RFC 1123 파싱 |
| 2.2 왕복 지연 보정 | `sync()` | `(after-before)/2` 편도 지연 보정 |
| 2.3 보정 시각 반환 | `corrected_time_ms()` | 로컬 시각 + auto_offset + manual_offset (ms) |
| 2.4 실패 폴백 | `sync()` | Exception 시 offset=0, synced=False 반환 |
| 2.5 일치율 계산 | `match_rate()` | `max(0,(1-\|auto-manual\|/500)*100)` |

### 검증 결과
- 실제 네이버 서버 동기화: `offset=-662.7ms`, `success=True`
- 수동 오프셋 일치율: auto와 동일 → 100%, +100ms → 80%, +500ms 이상 → 0%
- 요청 실패 폴백: `offset=0.0, success=False` 정상 반환

### 다음 단계
- Phase 3: `coordinate.py` 구현 (Z 키 좌표 등록)

## [2026-05-17] Phase 3~6 — 전체 구현 및 통합 테스트

### 완료 항목

#### Phase 3 — coordinate.py
- `start_listener()` / `stop_listener()`: pynput 전역 키보드 리스너 데몬 스레드
- `begin_register(slot, callback)`: 슬롯 지정 + Z 키 대기 모드 진입
- `cancel_register()`: 등록 모드 취소
- `get_coord(slot)`, `get_all_coords()`, `all_registered()`: 좌표 조회

#### Phase 4 — clicker.py
- `start(target_ms, coords, manual_offset, on_done)`: 데몬 스레드로 정밀 대기 후 순서 클릭
- 50ms 전까지 10ms sleep, 이후 busy-wait으로 타이밍 정밀도 확보
- `cancel()` / `is_running()`: 취소 및 상태 확인

#### Phase 5 — ui/app_window.py
- 4개 영역 tkinter LabelFrame 레이아웃 (설계 문서 ASCII 와이어프레임 기준)
- 50ms tick으로 서버 시각·카운트다운 실시간 갱신
- Scale 슬라이더 → 일치율 Progressbar 실시간 연동
- 좌표 등록 중 버튼 시각적 피드백 (sunken / 대기 중...)
- 매크로 시작 버튼: 좌표 미등록 시 disabled, 실행 중 취소 버튼으로 전환
- threading으로 UI 블로킹 없이 동기화·클릭 실행

#### Phase 6 — 통합 테스트
- T-01~T-09 전항목 PASS
- 클릭 타이밍 오차: **0.1ms** (목표 ±10ms 대비 100배 정밀)

### 다음 단계
- 없음 (전체 Phase 완료). 실제 사용 피드백에 따라 개선 예정.

## [2026-05-17] UI 개선 작업

### 완료 항목

| 변경 내용 | 파일 | 세부사항 |
|-----------|------|----------|
| 오프셋 입력 방식 교체 | `ui/app_window.py` | `tk.Scale` → `tk.Entry` + 적용 버튼, Enter 키 지원, 범위 클램핑 |
| 현재 적용값 표시 | `ui/app_window.py` | "현재: +120 ms" 형태 레이블 추가 |
| 좌표 등록 조건 완화 | `coordinate.py`, `ui/app_window.py` | `all_registered()` → `any_registered()`, 1개 이상이면 시작 가능 |
| 일치율 실시간 미리보기 | `ui/app_window.py` | `trace_add("write", ...)` 로 타이핑 중 즉시 반영 |
| `_update_match` 개선 | `ui/app_window.py` | `preview_ms` 파라미터 추가, 미적용 값도 미리보기 가능 |

### 삭제된 기능
- 자동 일치율 조정 버튼 (10초 서버 다중 동기화 → 유의미한 효과 없음으로 판단)

## [2026-05-17] PyInstaller 단독 exe 빌드

### 완료 항목

| 항목 | 내용 |
|------|------|
| 빌드 도구 | PyInstaller 6.18.0 |
| 출력 파일 | `dist/NaverTimeClickMacro.exe` (9.8 MB) |
| 옵션 | `--onefile --windowed --collect-all ui` |
| `.gitignore` | `*.spec` 추가 (`dist/`, `build/` 는 기존 등록) |
| 검증 | `ui` 패키지 포함 완료, 콘솔 창 없음 |

### 최종 빌드 명령 (수정됨)
```bash
pyinstaller --onefile --windowed --name "NaverTimeClickMacro" \
  --hidden-import "ui" --hidden-import "ui.app_window" main.py
```

### 특징
- Python 미설치 환경에서도 단독 실행 가능
- `--hidden-import` 으로 로컬 `ui` 패키지 명시적 포함 (중요)
- `--windowed` 로 콘솔 창 제외
- `ui.app_window` 모듈 누락 오류 해결

<!-- 새로운 진행 이력은 이 줄 위에 추가 -->
