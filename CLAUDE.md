# CLAUDE.md — NaverTimeClickMacro 프로젝트 지침

## 필수 참고 문서

**모든 작업 시작 전에 반드시 아래 파일을 읽어야 한다.**

- [`memory-bank/AGENTS.md`](memory-bank/AGENTS.md) — 코드 작성 규칙, 기술 스택, 모듈 구조, 작업 전후 체크리스트

## 작업 완료 후 필수 체크리스트

**코드를 수정하거나 기능을 변경했다면 응답 전에 반드시 수행한다.**

1. `memory-bank/progress.md` — 완료 내용 추가
2. `memory-bank/history.md` — 요구사항·결정사항 변경 시 기록
3. `memory-bank/codereview.md` — 코드 셀프 리뷰 추가
4. `memory-bank/testresult.md` — 테스트를 실행했다면 결과 기록

## 배포 (PyInstaller)

단독 exe 파일로 빌드 (로컬 `ui` 패키지 포함):
```bash
pyinstaller --onefile --windowed --name "NaverTimeClickMacro" \
  --hidden-import "ui" --hidden-import "ui.app_window" main.py
```

출력 파일: `dist/NaverTimeClickMacro.exe` (약 10 MB)  
Python 미설치 환경에서도 실행 가능

**주의:** 로컬 패키지는 `--hidden-import` 로 명시해야 PyInstaller가 인식함

## memory-bank 문서 구조

| 파일 | 용도 |
|------|------|
| `memory-bank/design.md` | 설계 문서 (요구사항·UI·구현 기준) |
| `memory-bank/AGENTS.md` | **에이전트 운영 규칙 — 반드시 참고** |
| `memory-bank/implementation-plan.md` | 작업 계획 및 태스크 목록 |
| `memory-bank/progress.md` | AI가 완료한 작업 이력 |
| `memory-bank/history.md` | 요청사항·결정사항 변경 이력 |
| `memory-bank/codereview.md` | 코드 리뷰 누적 결과 |
| `memory-bank/testresult.md` | 테스트 결과 누적 기록 |
