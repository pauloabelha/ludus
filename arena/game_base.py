
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .core import State, Player, Move

class Game(ABC):
    code: str  # short identifier (e.g., "tic_tac_toe")
    name: str

    @abstractmethod
    def initial_state(self) -> State: ...
    @abstractmethod
    def legal_moves(self, state: State, player: Player) -> List[Move]: ...
    @abstractmethod
    def next_state(self, state: State, move: Move, player: Player) -> State: ...
    @abstractmethod
    def is_terminal(self, state: State) -> bool: ...
    @abstractmethod
    def winner(self, state: State) -> Optional[Player]: ...
    @abstractmethod
    def render(self, state: State) -> str: ...

    def players(self) -> List[Player]:
        return [Player.X, Player.O]

    def validate(self) -> None:
        s = self.initial_state()
        assert s.to_move in self.players(), "Invalid initial player"
