"""
Token vesting simulator.
Supports a cliff + linear vesting after cliff.
Timestamps are seconds since epoch.
"""

from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class VestingSchedule:
    total_amount: float
    start_time: int         # epoch seconds
    cliff_seconds: int      # seconds until cliff
    duration_seconds: int   # total duration (including cliff) for full vesting

    def vested_at(self, t: Optional[int] = None) -> float:
        """
        Return how many tokens are vested (unlocked) at time t.
        """
        if t is None:
            t = int(time.time())
        if t < self.start_time + self.cliff_seconds:
            return 0.0
        if t >= self.start_time + self.duration_seconds:
            return float(self.total_amount)
        # linear after cliff: proportion of (t - (start+cliff)) over (duration - cliff)
        effective = t - (self.start_time + self.cliff_seconds)
        total_linear = max(1, self.duration_seconds - self.cliff_seconds)
        proportion = effective / total_linear
        return float(self.total_amount) * proportion

    def locked_at(self, t: Optional[int] = None) -> float:
      return float(self.total_amount) - self.vested_at(t)
