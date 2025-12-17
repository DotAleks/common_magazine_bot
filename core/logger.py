import os
import sys
import logging
from typing import Optional
from logging.handlers import RotatingFileHandler


class Logger:
    """Singleton class for configuring and managing application logging."""
    _instance: Optional['Logger'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        
        self.logger = logging.getLogger('common_magazine_bot')
        level = logging.DEBUG
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(level)
        console.setFormatter(formatter)

        file = RotatingFileHandler(
            'logs/bot.log',
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        file.setLevel(level)
        file.setFormatter(formatter)

        self.logger.addHandler(console)
        self.logger.addHandler(file)


        self._initialized = True

    def get_logger(self) -> logging.Logger:
        """Returns the configured logger instance"""
        return self.logger

_logger_instance = Logger()
logger = _logger_instance.get_logger()