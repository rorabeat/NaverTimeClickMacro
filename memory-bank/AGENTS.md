# AGENTS.md — AI 에이전트 운영 지침

이 파일은 Claude Code 등 AI 에이전트가 NaverTimeClickMacro 프로젝트를 작업할 때 반드시 따라야 할 규칙과 컨텍스트를 정의한다.

---

## 프로젝트 요약

네이버 서버 시간 기준으로 사용자가 지정한 시각에 미리 등록한 3개의 화면 좌표를 자동 클릭하는 Python 매크로 프로그램.

---

## 핵심 파일 위치

| 파일 | 역할 |
|------|------|
| `memory-bank/design.md` | 설계 문서 (요구사항·기술스택·UI·구조) — 모든 구현의 기준 |
| `memory-bank/AGENTS.md` | 본 파일 — 에이전트 운영 규칙 |
| `memory-bank/implementation-plan.md` | 작업 계획 및 태스크 목록 |
| `memory-bank/progress.md` | AI가 완료한 작업 이력 |
| `memory-bank/history.md` | 요청사항·결정사항 변경 이력 |
| `memory-bank/codereview.md` | 코드 리뷰 누적 결과 |
| `memory-bank/testresult.md` | 테스트 결과 누적 기록 |

---

## 기술 스택 (변경 금지)

- **언어:** Python 3.10+
- **GUI:** `tkinter` (표준 라이브러리)
- **마우스 클릭:** `pyautogui`
- **키보드 감지:** `pynput`
- **HTTP 요청:** `requests`
- **시간 처리:** `datetime`, `time`

---

## 모듈 구조 (변경 전 반드시 확인)

```
NaverTimeClickMacro/
├── main.py              # 진입점, tkinter 메인 루프
├── time_sync.py         # 네이버 서버 시간 동기화
├── coordinate.py        # 좌표 등록 및 pynput 리스너
├── clicker.py           # pyautogui 클릭 및 정밀 대기
├── ui/
│   └── app_window.py    # tkinter UI 레이아웃
└── requirements.txt
```

---

## 에이전트 행동 규칙

### 작업 시작 전
1. `memory-bank/implementation-plan.md` 를 읽어 현재 태스크와 우선순위를 확인한다.
2. `memory-bank/progress.md` 를 읽어 이미 완료된 작업과 중복되지 않는지 확인한다.
3. `memory-bank/design.md` 를 기준으로 요구사항을 재확인한다.

### 코드 작성 규칙
- 주석은 WHY가 불명확한 경우에만 작성한다. WHAT 설명 주석은 금지.
- 함수·변수명은 한국어 프로젝트이므로 영어 snake_case를 사용한다.
- 오류 처리는 시스템 경계(HTTP 요청, 파일 I/O)에서만 추가한다.
- 불필요한 추상화·helper 함수를 만들지 않는다.

### 작업 완료 후 (반드시 수행)
1. `memory-bank/progress.md` 에 완료 내용을 추가한다.
2. 코드를 작성하거나 수정했다면 `memory-bank/codereview.md` 에 셀프 리뷰를 추가한다.
3. 테스트를 실행했다면 `memory-bank/testresult.md` 에 결과를 추가한다.
4. 요구사항이 변경됐다면 `memory-bank/history.md` 에 기록하고 `memory-bank/implementation-plan.md` 를 갱신한다.

### 금지 사항
- `design.md` 의 기술 스택을 임의로 변경하지 않는다.
- 사용자 확인 없이 파일을 삭제하지 않는다.
- `pyautogui.FAILSAFE = False` 를 코드에 추가하지 않는다 (안전 기능 유지).
- 구현되지 않은 기능을 구현된 것처럼 progress.md 에 기록하지 않는다.

---

## 네이버 서버 시간 동기화 핵심 로직 (참고)

```python
before = time.time()
response = requests.head("https://www.naver.com")
after = time.time()
server_time = parse_http_date(response.headers["Date"])
offset_ms = (server_time - after + (after - before) / 2) * 1000
```

## 일치율 계산 공식 (참고)

```
일치율(%) = max(0, (1 - |자동오프셋 - 수동오프셋| / 500) × 100)
```
