"""Logging configuration"""
import logging
import sys
from typing import Any

# Configure logging format
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        },
        "json": {
            "format": '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}',
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "app.log",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "uvicorn": {"level": "INFO"},
        "fastapi": {"level": "INFO"},
        "sqlalchemy": {"level": "WARNING"},
    },
}


def setup_logging(level: str = "INFO"):
    """Setup logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger().setLevel(level)


class Logger:
    """Structured logger wrapper"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def info(self, message: str, **kwargs: Any):
        self.logger.info(self._format(message, kwargs))
    
    def warning(self, message: str, **kwargs: Any):
        self.logger.warning(self._format(message, kwargs))
    
    def error(self, message: str, **kwargs: Any):
        self.logger.error(self._format(message, kwargs))
    
    def debug(self, message: str, **kwargs: Any):
        self.logger.debug(self._format(message, kwargs))
    
    @staticmethod
    def _format(message: str, context: dict) -> str:
        if context:
            context_str = " | ".join(f"{k}={v}" for k, v in context.items())
            return f"{message} | {context_str}"
        return message


# Create logger instances
logger = Logger("ai-education")