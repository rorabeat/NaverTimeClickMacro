# codereview.md — 코드 리뷰 누적 결과

코드 리뷰는 최신순(위)으로 기록한다. 각 항목은 파일·함수 단위로 작성한다.

---

## [2026-05-17] PyInstaller 배포 — exe 연쇄 ModuleNotFoundError (통합)

### 리뷰어
- AI 셀프 리뷰

### 대상
- `ui/app_window.py`, `NaverTimeClickMacro.spec`, `build.ps1`, 빌드 환경

### 발견 사항
| 구분 | 위치 | 내용 | 심각도 |
|------|------|------|--------|
| 버그 | `ui/app_window.py` L166 | `_begin_register` 들여쓰기 깨짐 → `invalid module ui.app_window` | 높음 |
| 버그 | 빌드 Python 3.13 | `pyautogui`·`pynput` 미설치 → warn에 missing module | 높음 |
| 운영 | `dist/*.exe` | exe 실행 중 재빌드 시 `PermissionError` | 중간 |
| 개선 | `NaverTimeClickMacro.spec` | `collect_all('pyautogui'|'pynput')` 적용 | — |
| 개선 | `build.ps1` | pip install + pyinstaller 일괄화 | — |

### 조치
- [x] `ui/__init__.py` 추가
- [x] `app_window.py` 들여쓰기 복구
- [x] spec `collect_all` + `build.ps1`
- [x] `build.ps1` (Python 3.14) 빌드 성공 확인

---

## [2026-05-17] PyInstaller 배포 — exe ModuleNotFoundError (1차)

### 리뷰어
- AI 셀프 리뷰

### 대상
- `ui/` 패키지, `NaverTimeClickMacro.spec`

### 발견 사항
| 구분 | 위치 | 내용 | 심각도 |
|------|------|------|--------|
| 버그 | `ui/` | `__init__.py` 없음 → PyInstaller가 `ui.app_window` 미수집 | 높음 |
| 개선 | `NaverTimeClickMacro.spec` | `pathex`·hiddenimports 보강 | — |

### 조치
- `ui/__init__.py` 추가 (후속: 들여쓰기·collect_all 추가 수정)

---

## 리뷰 템플릿

```
## [날짜] 파일명 — 리뷰 대상

### 리뷰어
- AI 셀프 리뷰 / 사용자 리뷰

### 대상 함수/범위
- 함수명 또는 범위 설명

### 발견 사항
| 구분 | 위치 | 내용 | 심각도 |
|------|------|------|--------|
| 버그 | line N | 설명 | 높음/중간/낮음 |
| 개선 | line N | 설명 | — |

### 조치 결과
- [ ] 수정 필요
- [x] 수정 완료 (커밋: xxxxxx)
- [ ] 다음 세션에서 처리
```

---

## 리뷰 이력

_소스코드 구현 후 리뷰 내용이 추가됩니다._

## [2026-05-17] time_sync.py — 셀프 리뷰

### 리뷰어
AI 셀프 리뷰

### 대상 범위
`time_sync.py` 전체 (5개 함수)

### 발견 사항
| 구분 | 위치 | 내용 | 심각도 |
|------|------|------|--------|
| 양호 | `sync()` | 왕복 지연 절반 보정으로 정밀도 확보 | — |
| 양호 | `sync()` | Exception 포괄 처리로 어떤 네트워크 오류도 폴백됨 | — |
| 양호 | `match_rate()` | `max(0,...)` 으로 음수 방지 | — |
| 참고 | 모듈 수준 전역 변수 | `_auto_offset_ms`, `_synced` 를 모듈 전역으로 관리 — 단일 인스턴스 앱이므로 문제없음 | — |

### 조치 결과
- 이슈 없음

## [2026-05-17] coordinate.py / clicker.py / ui/app_window.py — 셀프 리뷰

### 리뷰어
AI 셀프 리뷰

### 발견 사항
| 구분 | 위치 | 내용 | 심각도 |
|------|------|------|--------|
| 양호 | coordinate.py | pynput 리스너를 daemon=True 로 설정해 앱 종료 시 자동 정리 | — |
| 양호 | clicker.py | 클릭 스레드도 daemon=True, cancel() 플래그로 안전 종료 | — |
| 양호 | app_window.py | 모든 모듈 콜백을 `root.after(0, ...)` 로 UI 스레드에 위임 | — |
| 참고 | app_window.py `_tick` | 50ms 주기 재귀 호출 — try/finally 로 예외 시에도 tick 유지 | — |
| 참고 | app_window.py `_get_target_ms` | 날짜를 오늘로 고정 — 자정 넘김 시나리오는 미지원 (설계 범위 외) | — |

### 조치 결과
- 이슈 없음

<!-- 새로운 리뷰는 이 줄 위에 추가 -->
