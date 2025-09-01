from .tic_tac_toe import TicTacToe
from .eleven_sticks import ElevenSticks

GAME_REGISTRY = {
    TicTacToe.code: TicTacToe,
    ElevenSticks.code: ElevenSticks,
}
