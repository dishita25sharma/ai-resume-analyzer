"""
Logger Configuration Module
Provides structured logging for the entire application
"""

import logging
import logging.handlers
from datetime import datetime
from pathlib import Path


class AppLogger:
    """
    Centralized logging configuration for the AI Resume Analyzer
    """

    _logger = None

    @classmethod
    def get_logger(cls, name: str = "ai_resume_analyzer") -> logging.Logger:
        """
        Get or create a configured logger instance.

        Args:
            name: Logger name (usually __name__)

        Returns:
            Configured logger instance
        """
        if cls._logger is not None:
            return logging.getLogger(name)

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # Define log format
        log_format = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler (INFO and above)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        # File handler (all levels)
        file_handler = logging.handlers.RotatingFileHandler(
            filename=logs_dir / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        # Error file handler (ERROR and above)
        error_handler = logging.handlers.RotatingFileHandler(
            filename=logs_dir / "error.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(log_format)
        logger.addHandler(error_handler)

        cls._logger = logger
        return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Convenience function to get a logger instance.

    Usage:
        from utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Message")

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    return AppLogger.get_logger(name)
