
from __future__ import annotations
import importlib.util
import os
import threading
import queue
import time
from typing import Callable, Dict, Any, List, Optional
from .core import State, Player, Move
from .game_base import Game

def load_bot_callable(bots_dir: str, file_name: str) -> Callable[[State, List[Move], Player, Game], Move]:
    path = os.path.join(bots_dir, file_name)
    spec = importlib.util.spec_from_file_location("arena_bot_" + os.path.splitext(file_name)[0], path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load bot from {file_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    if not hasattr(module, "choose_move"):
        raise RuntimeError(f"Bot {file_name} must define choose_move(state, legal_moves, player, game)")
    return getattr(module, "choose_move")

class MatchController:
    def __init__(self, game: Game, bot0_fn: Callable, bot1_fn: Callable, time_limit: float = 0.5):
        self.game = game
        self.bot_fns = {Player.X: bot0_fn, Player.O: bot1_fn}
        self.time_limit = time_limit

    def _call_with_timeout(self, fn: Callable, args: tuple, legal_moves: List[Move]) -> Move:
        q: "queue.Queue[Optional[Move]]" = queue.Queue()

        def target():
            try:
                mv = fn(*args)
                q.put(mv)
            except Exception:
                q.put(None)

        t = threading.Thread(target=target, daemon=True)
        t.start()
        t.join(self.time_limit)
        if t.is_alive():
            return legal_moves[0]  # fallback: first legal move
        result = q.get()
        if result is None or result not in legal_moves:
            return legal_moves[0]  # fallback on invalid result
        return result

    def run(self) -> Dict[str, Any]:
        state = self.game.initial_state()
        moves: List[Dict[str, Any]] = []

        while not self.game.is_terminal(state):
            player = state.to_move
            legal = self.game.legal_moves(state, player)
            if not legal:
                break
            fn = self.bot_fns[player]
            move = self._call_with_timeout(fn, (state.copy(), legal.copy(), player, self.game), legal)
            state = self.game.next_state(state, move, player)
            moves.append({"player": player.value, "move": move})

        winner = self.game.winner(state)
        return {
            "final_state": state,
            "moves": moves,
            "winner": winner.value if winner else "draw",
            "winning_line": state.winning_line or []
        }
