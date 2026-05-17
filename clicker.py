from __future__ import annotations

import threading
import time
from typing import Callable

import pyautogui

import time_sync
from coordinate import Coord

pyautogui.PAUSE = 0

_thread: threading.Thread | None = None
_running: bool = False


def _wait_and_click(
    target_ms: float,
    coords: list[Coord],
    manual_offset_ms: float,
    on_done: Callable[[bool, str], None],
) -> None:
    global _running
    try:
        while _running:
            now = time_sync.corrected_time_ms(manual_offset_ms)
            remaining = target_ms - now
            if remaining <= 0:
                break
            if remaining > 50:
                time.sleep(0.01)
            # 50ms 이내 구간은 busy-wait으로 정밀도 확보

        if not _running:
            on_done(False, "취소됨")
            return

        for x, y in coords:
            pyautogui.click(x, y)

        on_done(True, "완료")
    except Exception as e:
        on_done(False, str(e))
    finally:
        _running = False


def start(
    target_ms: float,
    coords: list[Coord],
    manual_offset_ms: float,
    on_done: Callable[[bool, str], None],
) -> None:
    """목표 시각(ms)에 coords 순서대로 클릭한다. on_done(success, message) 콜백 호출."""
    global _thread, _running
    if _running:
        return
    _running = True
    _thread = threading.Thread(
        target=_wait_and_click,
        args=(target_ms, coords, manual_offset_ms, on_done),
        daemon=True,
    )
    _thread.start()


def cancel() -> None:
    global _running
    _running = False


def is_running() -> bool:
    return _running
