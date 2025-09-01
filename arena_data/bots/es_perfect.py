import random

def choose_move(state, legal_moves, player, game):
    # Estratégia ótima: deixar múltiplo de 4 para o adversário
    target = (state.sticks - 1) % 4
    if target == 0 or target not in legal_moves:
        return random.choice(legal_moves)
    return target
