import sys
from pathlib import Path
from loguru import logger

# Pasta de logs
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Remove qualquer configuração default
logger.remove()

# Console colorido
logger.add(
    sys.stderr,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
    level="DEBUG"  # pode trocar para INFO em produção
)

# Arquivo com rotação
logger.add(
    LOG_DIR / "arena.log",
    rotation="1 MB",
    retention="7 days",
    compression="zip",
    level="DEBUG",
    enqueue=True  # seguro para multiprocessos
)

logger.info("Logger initialized")

# Exporta o logger pronto
__all__ = ["logger"]
