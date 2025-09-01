import random

def choose_move(state, legal_moves, player, game):
    # Simply pick a random legal move
    return random.choice(legal_moves)
