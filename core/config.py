import os
from typing import Optional

from dotenv import load_dotenv

from core.logger import logger


class Config:
    """Singleton class for setting environment variables"""
    _instance: Optional['Config'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _get_required(self, var_name: str) -> str:
        """Getting a required environment variable"""
        value = os.getenv(var_name)
        if value is None:
            logger.critical(f'Required enviroment variable {var_name} not set!')
            raise
        return value.strip()
    
    def __init__(self):
        if getattr(self, '_initialized', False):
            return

        load_dotenv()
        
        self.BOT_TOKEN: str = self._get_required('BOT_TOKEN')

        self._initialized = True
        logger.info('Configuration loaded successfully')

    


config = Config()