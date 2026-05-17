# implementation-plan.md — 작업 계획

`design.md` 기준으로 작성된 구현 계획. 추가 요청사항이 생기면 해당 섹션을 업데이트한다.

---

## 현재 상태

- [x] 설계 문서 작성 (`design.md`)
- [x] 운영 문서 초기화 (`AGENTS.md`, `history.md`, `progress.md`, `codereview.md`, `testresult.md`)
- [x] Phase 1 완료 (2026-05-17)
- [x] Phase 2 완료 (2026-05-17)
- [x] Phase 3 완료 (2026-05-17)
- [x] Phase 4 완료 (2026-05-17)
- [x] Phase 5 완료 (2026-05-17)
- [x] Phase 6 완료 (2026-05-17)
- [x] Phase 7 완료 (2026-05-17) — PyInstaller exe 배포

---

## Phase 1 — 프로젝트 초기화

| # | 태스크 | 상태 | 비고 |
|---|--------|------|------|
| 1.1 | `requirements.txt` 생성 | 완료 | pyautogui, pynput, requests |
| 1.2 | 프로젝트 디렉터리 구조 생성 | 완료 | `ui/` 폴더 + `__init__.py` |
| 1.3 | `main.py` 진입점 스캐폴딩 | 완료 | tkinter 루프 + AppWindow 연결 |

## Phase 2 — 네이버 서버 시간 동기화 (`time_sync.py`)

| # | 태스크 | 상태 | 비고 |
|---|--------|------|------|
| 2.1 | HTTP HEAD 요청으로 Date 헤더 파싱 | 완료 | RFC 1123, `email.utils.parsedate_to_datetime` |
| 2.2 | 왕복 지연 보정(offset_ms) 계산 | 완료 | `(after-before)/2` 보정 |
| 2.3 | 오프셋 저장 및 보정 시각 반환 함수 | 완료 | `corrected_time_ms()` |
| 2.4 | 서버 요청 실패 시 로컬 시간 폴백 | 완료 | `sync()` → `(0.0, False)` 반환 |
| 2.5 | 일치율(%) 계산 함수 | 완료 | `match_rate(manual_offset_ms)` |

## Phase 3 — 좌표 등록 (`coordinate.py`)

| # | 태스크 | 상태 | 비고 |
|---|--------|------|------|
| 3.1 | pynput 전역 키보드 리스너 설정 | 완료 | `start_listener()` / `stop_listener()` |
| 3.2 | 등록 모드 상태 플래그 관리 | 완료 | `_registering`, `_current_slot` |
| 3.3 | 마우스 좌표 캡처 및 슬롯 저장 | 완료 | `begin_register(slot, callback)` |
| 3.4 | 좌표 재등록(수정) 기능 | 완료 | 동일 슬롯으로 `begin_register` 재호출 |

## Phase 4 — 클릭 실행 (`clicker.py`)

| # | 태스크 | 상태 | 비고 |
|---|--------|------|------|
| 4.1 | 정밀 대기 루프 구현 | 완료 | 50ms 전까지 sleep, 이후 busy-wait |
| 4.2 | pyautogui 좌표 3개 순서 클릭 | 완료 | `PAUSE=0`, daemon thread |
| 4.3 | 클릭 완료 콜백 | 완료 | `on_done(success, message)` |

## Phase 5 — GUI (`ui/app_window.py`)

| # | 태스크 | 상태 | 비고 |
|---|--------|------|------|
| 5.1 | 메인 윈도우 레이아웃 구성 | 완료 | LabelFrame 4개 영역 |
| 5.2 | 서버 시간 표시 및 재동기화 버튼 | 완료 | 50ms tick 실시간 갱신 |
| 5.3 | 오프셋 슬라이더 및 일치율 프로그레스 바 | 완료 | Scale + Progressbar |
| 5.4 | 목표 시각 입력 필드 (시/분/초/ms) | 완료 | 범위 검증 포함 |
| 5.5 | 카운트다운 표시 | 완료 | `HH:MM:SS.mmm` |
| 5.6 | 좌표 슬롯 3개 표시 및 등록/재등록 버튼 | 완료 | 등록 중 버튼 비활성화 |
| 5.7 | 매크로 시작/취소 버튼 (조건부 활성화) | 완료 | 좌표 미등록 시 disabled |
| 5.8 | 상태 표시 라벨 (대기중/실행중/완료/오류) | 완료 | |

## Phase 6 — 통합 및 테스트

| # | 태스크 | 상태 | 비고 |
|---|--------|------|------|
| 6.1 | 모듈 통합 및 전체 흐름 테스트 | 완료 | T-01~T-09 모두 PASS |
| 6.2 | 네이버 서버 시간 동기화 정확도 검증 | 완료 | 실제 서버 동기화 성공 |
| 6.3 | Z 키 좌표 등록 동작 검증 | 완료 | 등록·재등록 정상 |
| 6.4 | 정밀 클릭 타이밍 오차 측정 | 완료 | 오차 0.1ms (목표 ±10ms) |
| 6.5 | 예외 상황(서버 실패, 과거 시각 입력) 검증 | 완료 | 폴백·UI 차단 정상 |

---

## Phase 7 — PyInstaller exe 배포

| # | 태스크 | 상태 | 비고 |
|---|--------|------|------|
| 7.1 | `ui/__init__.py` 및 spec `pathex` | 완료 | 2026-05-17 |
| 7.2 | `app_window.py` 들여쓰기 수정 | 완료 | invalid module 해소 |
| 7.3 | `collect_all` pyautogui·pynput | 완료 | 2026-05-17 |
| 7.4 | `build.ps1` 빌드 스크립트 | 완료 | pip + pyinstaller |
| 7.5 | exe 빌드·실행 검증 | 완료 | Python 3.14 `build.ps1` 성공 |

---

## 추가 요청사항

_추가 요청이 있을 경우 아래에 기록하고 해당 Phase에 태스크를 추가한다._

| 날짜 | 요청 내용 | 반영 위치 | 상태 |
|------|-----------|-----------|------|
| 2026-05-17 | exe ModuleNotFoundError 연쇄 수정 | Phase 7 | 완료 |
