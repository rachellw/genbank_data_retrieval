import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os
import sys

def create_logger(name: str = "genbank_data", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:  # avoid double handlers on re-imports
        return logger
    logger.setLevel(level)

    # Format
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Always have a console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # Prefer project logs/ dir next to genbank_data_code
    project_root = Path(__file__).resolve().parents[1]  # .../genbank_data_code
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logfile = log_dir / "genbank_data.log"

    # Try file handler; if it fails, fall back to ~/.cache/<name>/logs
    try:
        fh = RotatingFileHandler(logfile, maxBytes=5_000_000, backupCount=5, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        logger.debug(f"Logging to {logfile}")
    except Exception as e:
        # Fallback to user-writable cache dir
        fallback_dir = Path(os.path.expanduser(f"~/.cache/{name}/logs"))
        fallback_dir.mkdir(parents=True, exist_ok=True)
        fallback_file = fallback_dir / "genbank_data.log"
        fh = RotatingFileHandler(fallback_file, maxBytes=5_000_000, backupCount=5, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        logger.warning(f"Could not use {logfile} ({e}); using {fallback_file} instead.")

    return logger

logger = create_logger()