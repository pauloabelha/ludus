from __future__ import annotations
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .logging_config import logger
from .controllers import MatchController, load_bot_callable
from .filestorage import (
    list_games, list_bots, get_leaderboard,
    update_leaderboard, save_match_log, BOTS_DIR
)
from .core import Player, Result

# Import available games into a registry
from .games.tic_tac_toe import TicTacToe
from .games.eleven_sticks import ElevenSticks

GAME_REGISTRY = {
    TicTacToe.code: TicTacToe,
    ElevenSticks.code: ElevenSticks,
}

APP_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = APP_DIR / "frontend"

# ---------- Logging setup ----------
LOG_DIR = APP_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ---------- FastAPI app ----------
app = FastAPI(title="Arena API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend
if FRONTEND_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
async def root():
    index_path = FRONTEND_DIR / "index.html"
    logger.debug("Serving index.html")
    return FileResponse(index_path)


@app.get("/games")
async def games():
    games = list_games()
    logger.info(f"Loaded {len(games)} games")
    return JSONResponse(games)


@app.get("/bots")
async def bots(game: str = Query(...)):
    bots = list_bots(game)
    logger.info(f"Listed {len(bots)} bots for game={game}")
    return JSONResponse(bots)


@app.get("/leaderboard")
async def leaderboard(game: str = Query(...)):
    lb = get_leaderboard(game)
    logger.info(f"Leaderboard request for game={game}")
    return JSONResponse(lb)


@app.get("/play")
async def play(
    game: str = Query(...),
    bot0: str = Query(...),
    bot1: str = Query(...)
) -> Dict[str, Any]:
    logger.info(f"New match: {game} | {bot0} (X) vs {bot1} (O)")

    GameClass = GAME_REGISTRY.get(game)
    if not GameClass:
        logger.error(f"Unsupported game requested: {game}")
        return JSONResponse({"error": f"Game {game} not supported"}, status_code=400)

    bots_meta = list_bots(game)
    meta_by_id = {b["id"]: b for b in bots_meta}
    if bot0 not in meta_by_id or bot1 not in meta_by_id:
        logger.error(f"Unknown bot id: {bot0} or {bot1}")
        return JSONResponse({"error": "Unknown bot id."}, status_code=400)

    bot0_fn = load_bot_callable(BOTS_DIR, meta_by_id[bot0]["file"])
    bot1_fn = load_bot_callable(BOTS_DIR, meta_by_id[bot1]["file"])

    game_impl = GameClass()
    controller = MatchController(game_impl, bot0_fn, bot1_fn, time_limit=0.5)
    result = controller.run()

    winner = result["winner"]
    logger.success(f"Match finished: Winner={winner}")

    # update leaderboard
    if winner == "draw":
        update_leaderboard(game, bot0, Result.DRAW.value)
        update_leaderboard(game, bot1, Result.DRAW.value)
    elif winner == Player.X.value:
        update_leaderboard(game, bot0, Result.WIN.value)
        update_leaderboard(game, bot1, Result.LOSS.value)
    else:
        update_leaderboard(game, bot1, Result.WIN.value)
        update_leaderboard(game, bot0, Result.LOSS.value)

    payload = {
        "game": game,
        "bot0": bot0,
        "bot1": bot1,
        "winner": winner,
        "moves": result["moves"],
        "final_board": result["final_state"].board,
        "winning_line": result.get("winning_line", []),
    }
    log_path = save_match_log(payload)
    logger.debug(f"Match log saved to {log_path}")

    return JSONResponse(payload)


@app.get("/backup")
def download_backup():
    tmpdir = tempfile.mkdtemp()
    zip_path = Path(tmpdir) / "arena_backup.zip"
    shutil.make_archive(str(zip_path).replace(".zip", ""), "zip", APP_DIR / "arena_data")
    logger.info("Backup created and ready for download")
    return FileResponse(zip_path, filename="arena_backup.zip", media_type="application/zip")
