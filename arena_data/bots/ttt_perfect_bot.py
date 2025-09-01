# Perfect Tic-Tac-Toe Bot using minimax
# Will always win if possible, otherwise draw

from math import inf

def choose_move(state, legal_moves, player, game):
    # state.board is a list of 9 strings: "X", "O", or ""
    best_score = -inf
    best_move = None
    for move in legal_moves:
        score = minimax(game.next_state(state, move, player), False, player, game)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


def minimax(state, maximizing, bot_player, game):
    # Terminal state check
    if game.is_terminal(state):
        winner = game.winner(state)
        if winner == bot_player:
            return 1   # win
        elif winner is None:
            return 0   # draw
        else:
            return -1  # loss

    player = state.to_move
    legal = game.legal_moves(state, player)

    if maximizing:
        value = -inf
        for m in legal:
            ns = game.next_state(state, m, player)
            value = max(value, minimax(ns, False, bot_player, game))
        return value
    else:
        value = inf
        for m in legal:
            ns = game.next_state(state, m, player)
            value = min(value, minimax(ns, True, bot_player, game))
        return value
