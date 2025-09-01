from __future__ import annotations
from typing import List, Optional
from ..game_base import Game
from ..core import State, Player, Move

class ElevenSticks(Game):
    code = "eleven_sticks"
    name = "11 Palitos"

    def initial_state(self) -> State:
        # use board[0] to store the count of sticks
        return State(
            board=[11],              # <-- hack: board[0] = number of sticks
            to_move=Player.X,
            winner=None,
            moves_played=0,
            winning_line=None,
        )

    def _get_sticks(self, state: State) -> int:
        return state.board[0]

    def _set_sticks(self, state: State, value: int) -> None:
        state.board[0] = value

    def legal_moves(self, state: State, player: Player) -> List[Move]:
        sticks = self._get_sticks(state)
        if self.is_terminal(state):
            return []
        return [i for i in [1, 2, 3] if i <= sticks]

    def next_state(self, state: State, move: Move, player: Player) -> State:
        ns = state.copy()
        sticks = self._get_sticks(ns)
        if move < 1 or move > 3 or move > sticks:
            raise ValueError("Illegal move")
        self._set_sticks(ns, sticks - move)
        ns.moves_played += 1

        if self._get_sticks(ns) == 0:
            # player who just played loses → next player wins
            ns.winner = player.other
        else:
            ns.to_move = player.other
        return ns

    def is_terminal(self, state: State) -> bool:
        return self._get_sticks(state) == 0 or state.winner is not None

    def winner(self, state: State) -> Optional[Player]:
        return state.winner

    def render(self, state: State) -> str:
        return "|" * self._get_sticks(state)
