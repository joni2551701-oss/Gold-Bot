"""
Backtesting Layer — Replay Clock (Phase 60.1: Historical Replay Engine
Foundation, TASK 3).

ReplayClock is a pure play/pause/stop/speed/seek state machine over an
integer position -- it knows nothing about candles, `RawCandleRepository`,
or `ReplayFeed` (that composition is `replay_engine.py`'s job, TASK 5).
No wall-clock timer, no background thread: this phase is a manually
stepped simulator (`advance()` is called once per `ReplayEngine.step()`),
matching CLAUDE.md's "no unnecessary refactor" -- a real-time-paced
player is not something any Phase 60.1 consumer needs yet.
"""

from backtesting.replay_models import ReplayState


class ReplayClock:
    """
    A play/pause/stop/speed/seek controller over one integer position.
    Starts at -1 ("before the first candle") -- the same convention
    `replay_feed.ReplayFeed.cursor` uses, so `replay_engine.py` can
    keep the two in lockstep without an off-by-one: after one
    `advance()` at speed=1.0, position is 0, matching a feed cursor
    that has consumed exactly one candle. `seek()`/`advance()` both
    clamp at -1, never lower.
    """

    def __init__(self, speed: float = 1.0):
        self.state: ReplayState = ReplayState.PENDING
        self.speed: float = speed
        self.position: int = -1

    def play(self) -> None:
        """Starts a PENDING clock, or resumes a PAUSED one -- same as resume()."""
        self.state = ReplayState.RUNNING

    def pause(self) -> None:
        self.state = ReplayState.PAUSED

    def resume(self) -> None:
        self.state = ReplayState.RUNNING

    def stop(self) -> None:
        self.state = ReplayState.STOPPED

    def finish(self) -> None:
        self.state = ReplayState.FINISHED

    def set_speed(self, speed: float) -> None:
        """Never negative or zero -- a non-advancing or reversed clock isn't a valid replay speed."""
        if speed <= 0:
            raise ValueError(f"speed must be > 0, got {speed}")
        self.speed = speed

    def seek(self, position: int) -> None:
        """Jumps the clock's own position directly -- replay_engine.py is responsible for keeping the paired ReplayFeed's cursor in sync after calling this."""
        self.position = max(-1, position)

    def advance(self) -> int:
        """Advances by `int(speed)` steps (minimum 1) if RUNNING; a no-op otherwise. Returns the resulting position either way."""
        if self.state == ReplayState.RUNNING:
            self.position += max(1, int(self.speed))
        return self.position

    @property
    def is_running(self) -> bool:
        return self.state == ReplayState.RUNNING

    @property
    def is_paused(self) -> bool:
        return self.state == ReplayState.PAUSED

    @property
    def is_stopped(self) -> bool:
        return self.state == ReplayState.STOPPED
