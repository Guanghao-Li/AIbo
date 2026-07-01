from __future__ import annotations

import asyncio
import signal
from collections.abc import Callable
from types import FrameType
from typing import Any

import pytest

from aibo.core.app import _install_shutdown_handlers


def test_shutdown_handlers_fall_back_when_loop_signal_handlers_are_unsupported(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    shutdown = asyncio.Event()

    class UnsupportedSignalLoop:
        def add_signal_handler(self, sig: signal.Signals, callback: Callable[[], None]) -> None:
            raise NotImplementedError

        def remove_signal_handler(self, sig: signal.Signals) -> bool:
            return False

        def call_soon_threadsafe(self, callback: Callable[[], None]) -> None:
            callback()

    installed_handlers: dict[signal.Signals, Any] = {}
    restored_handlers: dict[signal.Signals, Any] = {}

    def fake_getsignal(sig: signal.Signals) -> signal.Handlers:
        return signal.SIG_DFL

    def fake_signal(
        sig: signal.Signals,
        handler: signal.Handlers | Callable[[int, FrameType | None], Any],
    ) -> signal.Handlers | Callable[[int, FrameType | None], Any]:
        installed_handlers[sig] = handler
        return signal.SIG_DFL

    monkeypatch.setattr(signal, "getsignal", fake_getsignal)
    monkeypatch.setattr(signal, "signal", fake_signal)

    restore = _install_shutdown_handlers(UnsupportedSignalLoop(), shutdown)  # type: ignore[arg-type]

    assert signal.SIGINT in installed_handlers
    installed_handlers[signal.SIGINT](signal.SIGINT, None)
    assert shutdown.is_set()

    def capture_restore(
        sig: signal.Signals,
        handler: signal.Handlers | Callable[[int, FrameType | None], Any],
    ) -> signal.Handlers | Callable[[int, FrameType | None], Any]:
        restored_handlers[sig] = handler
        return signal.SIG_DFL

    monkeypatch.setattr(signal, "signal", capture_restore)

    restore()

    assert restored_handlers == {
        signal.SIGINT: signal.SIG_DFL,
        signal.SIGTERM: signal.SIG_DFL,
    }
