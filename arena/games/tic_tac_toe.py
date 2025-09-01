
from __future__ import annotations
from typing import List, Optional
from ..game_base import Game
from ..core import State, Player, Move, render_board

WIN_LINES = [
    [0,1,2],[3,4,5],[6,7,8],  # rows
    [0,3,6],[1,4,7],[2,5,8],  # cols
    [0,4,8],[2,4,6]           # diagonals
]

class TicTacToe(Game):
    code = "tic_tac_toe"
    name = "Tic-Tac-Toe"

    def initial_state(self) -> State:
        return State(board=[""]*9, to_move=Player.X, winner=None, moves_played=0, winning_line=None)

    def legal_moves(self, state: State, player: Player) -> List[Move]:
        if self.is_terminal(state):
            return []
        return [i for i, v in enumerate(state.board) if v == ""]

    def _check_winner(self, board: List[str]) -> Optional[Player]:
        for line in WIN_LINES:
            a,b,c = line
            if board[a] and board[a] == board[b] == board[c]:
                return Player(board[a])
        return None

    def _winning_line(self, board: List[str]) -> Optional[List[int]]:
        for line in WIN_LINES:
            a,b,c = line
            if board[a] and board[a] == board[b] == board[c]:
                return line
        return None

    def next_state(self, state: State, move: Move, player: Player) -> State:
        ns = state.copy()
        if ns.board[move] != "":
            raise ValueError("Illegal move")
        ns.board[move] = player.value
        ns.moves_played += 1
        w = self._check_winner(ns.board)
        if w:
            ns.winner = w
            ns.winning_line = self._winning_line(ns.board)
        elif ns.moves_played >= 9:
            ns.winner = None  # draw
        else:
            ns.to_move = player.other
        return ns

    def is_terminal(self, state: State) -> bool:
        if state.winner is not None:
            return True
        if state.moves_played >= 9:
            return True
        return False

    def winner(self, state: State) -> Optional[Player]:
        return state.winner

    def render(self, state: State) -> str:
        return render_board(state.board)
