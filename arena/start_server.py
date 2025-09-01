import uvicorn
from .logging_config import logger

def main():
    logger.info("Starting Arena with loguru logging")
    uvicorn.run(
        "arena.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_config=None,   # desativa logger padrão do uvicorn
    )

if __name__ == "__main__":
    main()
