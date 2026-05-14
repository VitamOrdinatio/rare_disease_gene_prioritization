"""Logging helpers for RDGP v1."""
from __future__ import annotations
from pathlib import Path
import logging

def setup_logger(log_path:str|Path)->logging.Logger:
    log_path=Path(log_path)
    log_path.parent.mkdir(parents=True,exist_ok=True)
    logger=logging.getLogger(f"rdgp.{log_path.stem}")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter=logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler=logging.FileHandler(log_path,encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler=logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate=False
    return logger
