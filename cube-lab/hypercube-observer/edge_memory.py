from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple

Edge = Tuple[int, int]


class EdgeMode(str, Enum):
    PERSIST = "persist"
    DECAY = "decay"
    HYBRID = "hybrid"


@dataclass
class EdgeMemory:
    """
    Hybrid edge memory:
      - fast: decays quickly (recent morphing texture)
      - slow: consolidated backbone (long-lived structure)
    """

    num_regions: int
    mode: EdgeMode = EdgeMode.HYBRID
    edge_decay: float = 0.995
    fast_decay: float = 0.990
    slow_decay: float = 0.9995
    consolidate_threshold: float = 8.0
    consolidate_amount: float = 4.0

    def __post_init__(self) -> None:
        if self.num_regions <= 0:
            raise ValueError("num_regions must be > 0")
        self.fast: Dict[Edge, float] = {}
        self.slow: Dict[Edge, float] = {}

    def step_decay(self) -> None:
        if self.mode == EdgeMode.PERSIST:
            return
        if self.mode == EdgeMode.DECAY:
            self._decay_dict(self.fast, self.edge_decay)
            return
        self._decay_dict(self.fast, self.fast_decay)
        self._decay_dict(self.slow, self.slow_decay)

    def add(self, src: int, dst: int, amount: float = 1.0) -> None:
        if not (0 <= src < self.num_regions and 0 <= dst < self.num_regions):
            raise ValueError("region index out of range")
        e = (src, dst)

        if self.mode == EdgeMode.PERSIST:
            self.fast[e] = self.fast.get(e, 0.0) + amount
            return

        self.fast[e] = self.fast.get(e, 0.0) + amount

        if self.mode == EdgeMode.HYBRID:
            fw = self.fast[e]
            if fw >= self.consolidate_threshold:
                moved = min(self.consolidate_amount, fw)
                self.fast[e] = fw - moved
                self.slow[e] = self.slow.get(e, 0.0) + moved

    @staticmethod
    def _decay_dict(d: Dict[Edge, float], decay: float) -> None:
        if not (0.0 < decay <= 1.0):
            raise ValueError("decay must be in (0, 1]")
        to_del: list[Edge] = []
        for e, w in d.items():
            w *= decay
            if w < 1e-6:
                to_del.append(e)
            else:
                d[e] = w
        for e in to_del:
            del d[e]
