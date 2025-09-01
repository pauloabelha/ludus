
import random

CORNERS = [0, 2, 6, 8]
CENTER = 4

def choose_move(state, legal_moves, player, game):
    # Try a corner first
    opts = [m for m in legal_moves if m in CORNERS]
    if opts:
        return random.choice(opts)
    # then center
    if CENTER in legal_moves:
        return CENTER
    # otherwise random
    return random.choice(legal_moves)
