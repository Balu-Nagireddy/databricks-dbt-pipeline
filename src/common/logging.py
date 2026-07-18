import os
import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger with clean, structured layout.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger is already configured
    if logger.handlers:
        return logger

    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
