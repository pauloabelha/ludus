def choose_move(state, legal_moves, player, game):
    # Sempre tenta pegar 3 se possível
    if 3 in legal_moves:
        return 3
    return max(legal_moves)
