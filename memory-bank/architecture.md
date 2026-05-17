# 아키텍처 문서

> 최종 업데이트: 2026-05-17 16:00:00 (KST)

---

## 디렉터리 구조

```
NaverTimeClickMacro/
├── memory-bank/              # 운영·설계 문서
├── main.py                   # 진입점 (tkinter mainloop)
├── time_sync.py              # 네이버 서버 시간 동기화
├── coordinate.py             # Z 키 좌표 등록 (pynput)
├── clicker.py                # 정밀 대기 + pyautogui 클릭
├── ui/
│   ├── __init__.py
│   └── app_window.py         # tkinter UI
├── requirements.txt
├── NaverTimeClickMacro.spec  # PyInstaller 빌드 정의
├── build.ps1                 # pip install + pyinstaller
├── dist/                     # 빌드 산출물 (exe)
└── build/                    # PyInstaller 중간 산출물
```

## 파일별 역할

| 파일 | 역할 |
|------|------|
| `main.py` | `AppWindow` 생성 및 tkinter 이벤트 루프 |
| `time_sync.py` | HTTP Date 헤더 기반 offset_ms, 일치율 계산 |
| `coordinate.py` | 슬롯별 좌표 저장, pynput Z 키·마우스 리스너 |
| `clicker.py` | 목표 시각 busy-wait 후 순차 클릭 |
| `ui/app_window.py` | UI 레이아웃, 스레드·콜백 연동 |
| `NaverTimeClickMacro.spec` | `collect_all`로 pyautogui·pynput 번들 |
| `build.ps1` | 빌드용 Python에 의존성 설치 후 exe 생성 |

---

## 아키텍처 통찰 (Insights)

### 2026-05-17 — PyInstaller 빌드 환경 일치

exe 오류 대부분은 **소스 실행 Python**과 **PyInstaller 빌드 Python**이 달라 패키지·모듈 수집 결과가 어긋난 경우였다. `build.ps1`은 PATH의 `python`을 사용하므로, 개발·빌드·실행에 동일 인터프리터를 쓰는 것이 안전하다. `collect_all('pyautogui')`, `collect_all('pynput')`는 hiddenimports만 쓸 때보다 의존 모듈 누락을 줄인다.

### 2026-05-17 — ui.app_window invalid module

`app_window.py` 문법 오류(들여쓰기) 시 PyInstaller가 `invalid module named ui.app_window`로 표시하며 번들에서 제외한다. hiddenimports만 추가해도 소스가 import 불가하면 exe에 포함되지 않는다.

---
