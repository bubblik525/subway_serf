"""Controller interface for a future learned temporal action readout.

The observation contract is defined here; policy inference remains unimplemented.
No random action or heuristic is substituted for a trained controller.
"""
from dataclasses import dataclass
from enum import IntEnum
import numpy as np


class Action(IntEnum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    JUMP = 3
    ROLL = 4


@dataclass(frozen=True)
class ControllerConfig:
    area_count: int = 65
    history_frames: int = 8
    action_count: int = len(Action)


class Controller:
    """Consumes chronological area states, never raw gameplay frames."""

    def __init__(self, config: ControllerConfig = ControllerConfig()):
        self.config = config

    def predict(self, history: np.ndarray) -> Action:
        expected = (self.config.history_frames, self.config.area_count)
        if history.shape != expected or not np.isfinite(history).all():
            raise ValueError(f'Expected finite chronological area states: {expected}')
        # TODO: load a versioned trained checkpoint and apply its temporal readout.
        # TODO: return the policy action; execution cooldowns belong in the game adapter.
        raise NotImplementedError('Controller inference requires a trained checkpoint and readout implementation.')
