from __future__ import annotations

from typing import Callable

from pynput import keyboard, mouse

Coord = tuple[int, int]
_SLOTS = 3

_coords: list[Coord | None] = [None] * _SLOTS
_registering: bool = False
_current_slot: int = 0
_on_registered: Callable[[int, Coord], None] | None = None

_mouse_ctrl = mouse.Controller()
_listener: keyboard.Listener | None = None


def _on_press(key: keyboard.Key | keyboard.KeyCode) -> None:
    global _registering, _current_slot
    if not _registering:
        return
    try:
        if key.char == "z":
            pos: Coord = _mouse_ctrl.position
            _coords[_current_slot] = pos
            _registering = False
            if _on_registered:
                _on_registered(_current_slot, pos)
    except AttributeError:
        pass


def start_listener() -> None:
    global _listener
    if _listener is None or not _listener.is_alive():
        _listener = keyboard.Listener(on_press=_on_press)
        _listener.daemon = True
        _listener.start()


def stop_listener() -> None:
    global _listener
    if _listener and _listener.is_alive():
        _listener.stop()
        _listener = None


def begin_register(slot: int, on_registered: Callable[[int, Coord], None]) -> None:
    """slot(0~2) 번 좌표 등록 모드를 시작한다. Z 키 입력 시 on_registered 호출."""
    global _registering, _current_slot, _on_registered
    if not (0 <= slot < _SLOTS):
        raise ValueError(f"slot must be 0~{_SLOTS - 1}")
    _current_slot = slot
    _on_registered = on_registered
    _registering = True


def cancel_register() -> None:
    global _registering
    _registering = False


def get_coord(slot: int) -> Coord | None:
    return _coords[slot]


def get_all_coords() -> list[Coord | None]:
    return list(_coords)


def all_registered() -> bool:
    return all(c is not None for c in _coords)


def any_registered() -> bool:
    return any(c is not None for c in _coords)


def is_registering() -> bool:
    return _registering
