# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
import threading
import tkinter as tk
from tkinter import ttk

import clicker
import coordinate
import time_sync


class AppWindow:
    SLOT_COUNT = 3
    OFFSET_MIN = -2000
    OFFSET_MAX = 2000

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("네이버 타임 클릭 매크로")
        self.root.resizable(False, False)

        self._manual_offset_ms: float = 0.0
        self._coord_vars: list[tk.StringVar] = [tk.StringVar(value="미등록") for _ in range(self.SLOT_COUNT)]
        self._status_var = tk.StringVar(value="대기 중")
        self._server_time_var = tk.StringVar(value="--:--:--.---")
        self._countdown_var = tk.StringVar(value="--:--:--.---")
        self._match_var = tk.StringVar(value="0%")
        self._synced_var = tk.StringVar(value="동기화 필요")

        self._build_ui()
        coordinate.start_listener()
        self._do_sync()
        self._tick()

    # ------------------------------------------------------------------ UI 구성

    def _build_ui(self) -> None:
        pad = {"padx": 10, "pady": 6}

        # ── 1. 서버 시간 동기화 영역 ──────────────────────────────────────
        sync_frame = ttk.LabelFrame(self.root, text="서버 시간 동기화")
        sync_frame.pack(fill="x", **pad)

        row0 = tk.Frame(sync_frame)
        row0.pack(fill="x", padx=8, pady=(6, 2))
        tk.Label(row0, text="서버 시각:").pack(side="left")
        tk.Label(row0, textvariable=self._server_time_var, font=("맑은 고딕", 11, "bold"), fg="#0066cc").pack(side="left", padx=6)
        tk.Label(row0, textvariable=self._synced_var, fg="gray").pack(side="left")
        tk.Button(row0, text="재동기화", command=self._do_sync).pack(side="right")

        row1 = tk.Frame(sync_frame)
        row1.pack(fill="x", padx=8, pady=2)
        tk.Label(row1, text="오프셋 조정(ms):").pack(side="left")
        self._offset_var = tk.StringVar(value="0")
        self._offset_entry = tk.Entry(row1, textvariable=self._offset_var, width=8, justify="center")
        self._offset_entry.pack(side="left", padx=6)
        self._offset_entry.bind("<Return>", lambda e: self._apply_offset())
        self._offset_var.trace_add("write", self._on_offset_var_changed)
        tk.Button(row1, text="적용", width=5, command=self._apply_offset).pack(side="left")
        self._offset_applied_var = tk.StringVar(value="현재: 0 ms")
        tk.Label(row1, textvariable=self._offset_applied_var, fg="gray").pack(side="left", padx=6)

        row2 = tk.Frame(sync_frame)
        row2.pack(fill="x", padx=8, pady=(2, 6))
        tk.Label(row2, text="일치율:").pack(side="left")
        self._match_bar = ttk.Progressbar(row2, length=200, maximum=100)
        self._match_bar.pack(side="left", padx=6)
        tk.Label(row2, textvariable=self._match_var, width=6).pack(side="left")

        # ── 2. 목표 시각 입력 영역 ────────────────────────────────────────
        time_frame = ttk.LabelFrame(self.root, text="목표 실행 시각")
        time_frame.pack(fill="x", **pad)

        row3 = tk.Frame(time_frame)
        row3.pack(padx=8, pady=(6, 2))
        fields = [("시", 2, 23), ("분", 2, 59), ("초", 2, 59), ("ms", 3, 999)]
        self._time_vars: list[tk.StringVar] = []
        for label, width, maxval in fields:
            tk.Label(row3, text=f"{label}:").pack(side="left")
            var = tk.StringVar(value="00" if width == 2 else "000")
            vcmd = (self.root.register(lambda s, m=maxval: self._validate_int(s, m)), "%P")
            e = tk.Entry(row3, textvariable=var, width=width + 1, validate="key", validatecommand=vcmd, justify="center")
            e.pack(side="left", padx=(0, 8))
            self._time_vars.append(var)

        row4 = tk.Frame(time_frame)
        row4.pack(padx=8, pady=(2, 6))
        tk.Label(row4, text="남은 시간:").pack(side="left")
        tk.Label(row4, textvariable=self._countdown_var, font=("맑은 고딕", 11), fg="#cc4400").pack(side="left", padx=6)

        # ── 3. 좌표 등록 영역 ────────────────────────────────────────────
        coord_frame = ttk.LabelFrame(self.root, text="클릭 좌표 등록")
        coord_frame.pack(fill="x", **pad)

        self._reg_buttons: list[tk.Button] = []
        for i in range(self.SLOT_COUNT):
            row = tk.Frame(coord_frame)
            row.pack(fill="x", padx=8, pady=2)
            tk.Label(row, text=f"좌표{i + 1}:", width=5).pack(side="left")
            tk.Label(row, textvariable=self._coord_vars[i], width=16, anchor="w").pack(side="left")
            btn = tk.Button(row, text="등록", width=6, command=lambda s=i: self._begin_register(s))
            btn.pack(side="left", padx=4)
            self._reg_buttons.append(btn)

        tk.Label(coord_frame, text="  ※ 등록 버튼 클릭 후, 마우스를 원하는 위치에 놓고 Z 키를 누르세요.",
                 fg="gray", font=("맑은 고딕", 9)).pack(anchor="w", padx=8, pady=(2, 6))

        # ── 4. 매크로 시작/취소 버튼 ─────────────────────────────────────
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="x", **pad)

        self._start_btn = tk.Button(
            bottom_frame, text="매크로 시작", width=16, height=2,
            font=("맑은 고딕", 11, "bold"), bg="#0066cc", fg="white",
            command=self._on_start_cancel,
        )
        self._start_btn.pack(side="left", padx=8)

        tk.Label(bottom_frame, text="상태:").pack(side="left")
        tk.Label(bottom_frame, textvariable=self._status_var, font=("맑은 고딕", 10, "bold")).pack(side="left", padx=4)

        self._refresh_start_btn()

    # ------------------------------------------------------------------ 이벤트 핸들러

    def _do_sync(self) -> None:
        self._synced_var.set("동기화 중...")

        def run():
            _, ok = time_sync.sync()
            self._manual_offset_ms = 0.0
            self.root.after(0, lambda: self._offset_var.set("0"))
            self.root.after(0, lambda: self._offset_applied_var.set("현재: 0 ms"))
            msg = "동기화 완료" if ok else "동기화 실패 (로컬 시간 사용)"
            self.root.after(0, lambda: self._synced_var.set(msg))
            self.root.after(0, self._update_match)

        threading.Thread(target=run, daemon=True).start()

    def _on_offset_var_changed(self, *_) -> None:
        try:
            self._update_match(float(int(self._offset_var.get())))
        except ValueError:
            self._update_match()

    def _apply_offset(self) -> None:
        try:
            value = int(self._offset_var.get())
        except ValueError:
            self._offset_var.set(str(int(self._manual_offset_ms)))
            return
        value = max(self.OFFSET_MIN, min(self.OFFSET_MAX, value))
        self._offset_var.set(str(value))
        self._manual_offset_ms = float(value)
        self._offset_applied_var.set(f"현재: {value:+d} ms")
        self._update_match()

    def _update_match(self, preview_ms: float | None = None) -> None:
        ms = preview_ms if preview_ms is not None else self._manual_offset_ms
        rate = time_sync.match_rate(ms)
        self._match_bar["value"] = rate
        self._match_var.set(f"{rate:.1f}%")

def _begin_register(self, slot: int) -> None:
        if coordinate.is_registering():
            coordinate.cancel_register()
        for btn in self._reg_buttons:
            btn.config(state="normal", relief="raised")
        self._reg_buttons[slot].config(text="대기 중...", state="disabled", relief="sunken")
        coordinate.begin_register(slot, self._on_coord_registered)

    def _on_coord_registered(self, slot: int, coord: tuple[int, int]) -> None:
        self.root.after(0, lambda: self._apply_coord(slot, coord))

    def _apply_coord(self, slot: int, coord: tuple[int, int]) -> None:
        self._coord_vars[slot].set(f"({coord[0]}, {coord[1]})")
        self._reg_buttons[slot].config(text="재등록", state="normal", relief="raised")
        self._refresh_start_btn()

    def _on_start_cancel(self) -> None:
        if clicker.is_running():
            clicker.cancel()
            self._status_var.set("취소됨")
            self._start_btn.config(text="매크로 시작", bg="#0066cc")
            return

        if not coordinate.any_registered():
            self._status_var.set("좌표를 1개 이상 등록하세요")
            return

        target_ms = self._get_target_ms()
        if target_ms is None:
            self._status_var.set("시각 입력 오류")
            return

        now = time_sync.corrected_time_ms(self._manual_offset_ms)
        if target_ms <= now:
            self._status_var.set("과거 시각입니다. 다시 설정하세요.")
            return

        coords = [c for c in coordinate.get_all_coords() if c is not None]
        self._start_btn.config(text="취소", bg="#cc0000")
        self._status_var.set("실행 중...")
        clicker.start(target_ms, coords, self._manual_offset_ms, self._on_macro_done)

    def _on_macro_done(self, success: bool, message: str) -> None:
        self.root.after(0, lambda: self._apply_macro_done(success, message))

    def _apply_macro_done(self, success: bool, message: str) -> None:
        self._status_var.set(f"{'완료' if success else '실패'}: {message}")
        self._start_btn.config(text="매크로 시작", bg="#0066cc")

    # ------------------------------------------------------------------ 유틸

    def _get_target_ms(self) -> float | None:
        try:
            h = int(self._time_vars[0].get())
            m = int(self._time_vars[1].get())
            s = int(self._time_vars[2].get())
            ms = int(self._time_vars[3].get())
            now = datetime.datetime.now()
            target = now.replace(hour=h, minute=m, second=s, microsecond=ms * 1000)
            return target.timestamp() * 1000
        except Exception:
            return None

    def _validate_int(self, value: str, maxval: int) -> bool:
        if value == "":
            return True
        if not value.isdigit():
            return False
        return int(value) <= maxval

    def _refresh_start_btn(self) -> None:
        ready = coordinate.any_registered() and not clicker.is_running()
        self._start_btn.config(state="normal" if ready else "disabled")

    def _tick(self) -> None:
        try:
            now_ms = time_sync.corrected_time_ms(self._manual_offset_ms)
            now_dt = datetime.datetime.fromtimestamp(now_ms / 1000)
            self._server_time_var.set(now_dt.strftime("%H:%M:%S.") + f"{now_dt.microsecond // 1000:03d}")

            target_ms = self._get_target_ms()
            if target_ms is not None:
                remaining = (target_ms - now_ms) / 1000
                if remaining > 0:
                    td = datetime.timedelta(seconds=remaining)
                    h, rem = divmod(int(td.total_seconds()), 3600)
                    m, s = divmod(rem, 60)
                    ms_part = int((remaining % 1) * 1000)
                    self._countdown_var.set(f"{h:02d}:{m:02d}:{s:02d}.{ms_part:03d}")
                else:
                    self._countdown_var.set("00:00:00.000")
            else:
                self._countdown_var.set("--:--:--.---")
        finally:
            self.root.after(50, self._tick)
