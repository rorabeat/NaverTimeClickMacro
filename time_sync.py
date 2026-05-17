import time
from email.utils import parsedate_to_datetime

import requests

NAVER_URL = "https://www.naver.com"
MATCH_TOLERANCE_MS = 500.0

_auto_offset_ms: float = 0.0
_synced: bool = False


def sync() -> tuple[float, bool]:
    """네이버 서버 시간과 동기화하여 offset_ms를 반환한다.

    Returns:
        (offset_ms, success) — 실패 시 offset_ms=0, success=False
    """
    global _auto_offset_ms, _synced
    try:
        before = time.time()
        resp = requests.head(NAVER_URL, timeout=5)
        after = time.time()

        date_str = resp.headers.get("Date", "")
        server_dt = parsedate_to_datetime(date_str)
        server_ts = server_dt.timestamp()

        # 왕복 지연의 절반을 편도 지연으로 보정
        estimated_arrival = before + (after - before) / 2
        _auto_offset_ms = (server_ts - estimated_arrival) * 1000
        _synced = True
    except Exception:
        _auto_offset_ms = 0.0
        _synced = False

    return _auto_offset_ms, _synced


def get_auto_offset_ms() -> float:
    return _auto_offset_ms


def corrected_time_ms(manual_offset_ms: float = 0.0) -> float:
    """현재 로컬 시각에 오프셋을 더한 보정 서버 시각(ms)을 반환한다."""
    return time.time() * 1000 + _auto_offset_ms + manual_offset_ms


def match_rate(manual_offset_ms: float) -> float:
    """수동 오프셋과 자동 오프셋의 일치율(%)을 반환한다.

    공식: max(0, (1 - |auto - manual| / TOLERANCE) * 100)
    """
    diff = abs(_auto_offset_ms - manual_offset_ms)
    return max(0.0, (1 - diff / MATCH_TOLERANCE_MS) * 100)


def is_synced() -> bool:
    return _synced
