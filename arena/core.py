
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Any

class Player(str, Enum):
    X = "X"
    O = "O"

    @property
    def other(self) -> "Player":
        return Player.O if self == Player.X else Player.X

Move = int  # for TicTacToe: 0..8

@dataclass
class State:
    board: List[str]          # "X", "O" or ""
    to_move: Player
    winner: Optional[Player] = None
    moves_played: int = 0
    winning_line: Optional[List[int]] = None

    def copy(self) -> "State":
        return State(board=self.board.copy(), to_move=self.to_move, winner=self.winner, moves_played=self.moves_played, winning_line=list(self.winning_line) if self.winning_line else None)

@dataclass
class BotSpec:
    id: str
    name: str
    file: str           # path to python file (relative to arena_data/bots)
    game: str           # e.g., "tic_tac_toe"
    description: str = ""

class Result(str, Enum):
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"

def render_board(board: List[str]) -> str:
    rows = []
    for r in range(3):
        row = board[r*3:(r+1)*3]
        rows.append(" | ".join(c or " " for c in row))
    return "\n-----\n".join(rows)
