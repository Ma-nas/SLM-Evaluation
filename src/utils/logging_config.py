"""
SLM Evaluation Harness — Logging Configuration
"""
import logging
import sys
from src.config.settings import LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger for the given module name.
    
    Usage:
        from src.utils.logging_config import get_logger
        logger = get_logger(__name__)
        logger.info("Starting benchmark run")
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    
    return logger
