from __future__ import annotations
import os, json, datetime
from typing import Any, Dict, List
from .logging_config import logger


from .core import Result

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "arena_data"))
BOTS_DIR = os.path.join(DATA_DIR, "bots")
GAMES_DIR = os.path.join(DATA_DIR, "games")
MATCHES_DIR = os.path.join(DATA_DIR, "matches")
LEADERBOARD_PATH = os.path.join(DATA_DIR, "leaderboard.json")
BOTS_METADATA = os.path.join(BOTS_DIR, "metadata.json")


def ensure_dirs() -> None:
    for d in [DATA_DIR, BOTS_DIR, GAMES_DIR, MATCHES_DIR]:
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(LEADERBOARD_PATH):
        with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f)
        logger.info(f"Created new leaderboard file at {LEADERBOARD_PATH}")


def read_json(path: str, default: Any) -> Any:
    if not os.path.exists(path):
        logger.warning(f"JSON not found: {path}")
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to parse JSON {path}: {e}")
        return default


def write_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.success(f"Saved JSON → {path}")


def list_games() -> List[Dict[str, Any]]:
    ensure_dirs()
    games = []
    for name in os.listdir(GAMES_DIR):
        logger.debug(f"Found file in games dir: {name}")  # log every file seen
        if not name.endswith(".json"):
            logger.debug(f"Skipping non-JSON file: {name}")
            continue
        if "Zone.Identifier" in name:
            logger.debug(f"Skipping junk file: {name}")
            continue

        p = os.path.join(GAMES_DIR, name)
        logger.debug(f"Trying to load game JSON: {p}")
        meta = read_json(p, {})
        if meta:
            logger.success(f"Loaded game OK: {meta.get('code')} ({name})")
            games.append(meta)
        else:
            logger.error(f"Failed or empty JSON for: {name}")

    logger.info(f"Total games loaded: {len(games)}")
    return games

def list_bots(game_code: str) -> List[Dict[str, Any]]:
    ensure_dirs()
    logger.debug(f"Looking for bots metadata at {BOTS_METADATA}")

    if not os.path.exists(BOTS_METADATA):
        logger.warning("metadata.json not found")
        return []

    if "Zone.Identifier" in BOTS_METADATA:
        logger.warning("Ignoring Zone.Identifier metadata junk")
        return []

    logger.debug(f"Trying to load metadata.json")
    meta = read_json(BOTS_METADATA, [])
    if not meta:
        logger.error("metadata.json is empty or invalid")
        return []

    bots = [b for b in meta if b.get("game") == game_code]
    logger.info(f"Listed {len(bots)} bots for game={game_code}")
    for b in bots:
        logger.debug(f" → Bot loaded: {b.get('id')} ({b.get('name')})")
    return bots


def get_leaderboard(game_code: str) -> Dict[str, Any]:
    ensure_dirs()
    lb = read_json(LEADERBOARD_PATH, {})
    logger.debug(f"Fetched leaderboard for {game_code}")
    return lb.get(game_code, {})


def _init_stat() -> Dict[str, Any]:
    return {"wins": 0, "losses": 0, "draws": 0, "games": 0}


def update_leaderboard(game_code: str, bot_id: str, result: str) -> None:
    ensure_dirs()
    lb = read_json(LEADERBOARD_PATH, {})
    game_lb = lb.get(game_code, {})
    stats = game_lb.get(bot_id, _init_stat())

    if result == Result.WIN.value:
        stats["wins"] += 1
    elif result == Result.LOSS.value:
        stats["losses"] += 1
    else:
        stats["draws"] += 1
    stats["games"] += 1

    game_lb[bot_id] = stats
    lb[game_code] = game_lb
    write_json(LEADERBOARD_PATH, lb)

    logger.success(
        f"Updated leaderboard: game={game_code}, bot={bot_id}, "
        f"result={result}, stats={stats}"
    )


def save_match_log(payload: Dict[str, Any]) -> str:
    ensure_dirs()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = os.path.join(MATCHES_DIR, f"{payload.get('game','game')}_{ts}.json")
    write_json(path, payload)
    logger.info(
        f"Saved match log: game={payload.get('game')}, "
        f"bots={payload.get('bot0')} vs {payload.get('bot1')} → winner={payload.get('winner')}"
    )
    return path
