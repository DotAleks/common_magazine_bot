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
        self.WEBHOOK_HOST: int = int(self._get_required('WEBHOOK_HOST'))
        self.WEBHOOK_PORT: int = int(self._get_required('WEBHOOK_PORT'))
        self.WEBHOOK_PATH: str = os.getenv('WEBHOOK_PATH','/webhook')

        self.WEBAPP_HOST: str = self._get_required('WEBAPP_HOST')
        self.WEBAPP_PORT: int = int(self._get_required('WEBAPP_PORT'))

        self.DB_DRIVER = self._get_required('DB_DRIVER')
        self.DB_HOST = self._get_required('DB_HOST')
        self.DB_PORT = self._get_required('DB_PORT')
        self.DB_NAME = self._get_required('DB_NAME')
        self.DB_USER = self._get_required('DB_USER')
        self.DB_PASSWD = self._get_required('DB_PASSWD')

        self.REDIS_SCHEME = self._get_required('REDIS_SCHEME')
        self.REDIS_USER = self._get_required('REDIS_USER')
        self.REDIS_HOST = self._get_required('REDIS_HOST')
        self.REDIS_PORT = int(self._get_required('REDIS_PORT'))
        self.REDIS_PASSWD = self._get_required('REDIS_PASSWD')
        self.REDIS_DB = self._get_required('REDIS_DB')
        
        self._initialized = True
        logger.info('Configuration loaded successfully')

    @property
    def WEBHOOK_URL(self) -> str:
        """Full webhook url"""
        return f'http://{self.WEBHOOK_HOST}:{self.WEBHOOK_PORT}/{self.WEBHOOK_PATH}'
    
    @property
    def DB_URL(self) -> str:
        """Full databse url"""
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    @property
    def REDIS_URL(self) -> str:
        """Full redis url"""
        if self.REDIS_SCHEME == 'unix':
            return f'{self.REDIS_SCHEME}://{self.REDIS_HOST}?db={self.REDIS_DB}'

        return f'{self.REDIS_SCHEME}://{self.REDIS_USER}:{self.REDIS_PASSWD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'
        


config = Config()