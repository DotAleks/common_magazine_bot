import asyncio
from aiohttp import web

from redis.asyncio import Redis

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from core.config import config
from core.logger import logger
from bot.handlers import routers
from database import Database


async def on_startup(bot: Bot) -> None:
    """Create webhook"""
    try:
        await bot.set_webhook(
            url=config.WEBHOOK_URL
        )
        logger.info('The webhook has been installed successfully.')
    except Exception as error:
        logger.error(f'Error installing webhook: {error}')

async def on_shutdown(bot: Bot) -> None:
    """Delete webhook"""
    try:
        await bot.delete_webhook()
        logger.info('The webhook has been successfully removed.')
    except Exception as error:
        logger.error(f'Error deleting webhook: {error}')

def get_app(bot: Bot, dp: Dispatcher) -> web.Application:
    """Create aiohttp application"""
    try:
        
        webhook = SimpleRequestHandler(
            bot=bot,
            dispatcher=dp
        )

        app =  web.Application()

        webhook.register(app,path=config.WEBHOOK_PATH)

        async def health(request: web.Request) -> web.Response:
            return web.Response(text='OK')
        
        app.router.add_get('/health',health)

        app.on_startup.append(lambda _: on_startup(bot))
        app.on_shutdown.append(lambda _: on_shutdown(bot))
        logger.info('Application created successfully')
        return app
    except Exception as error:
        logger.error(f'Error while creating application: {error}')
        raise

async def main() -> None:
    """Running a bot"""
    try:
        logger.info('Running a bot...')
        bot = Bot(token=config.BOT_TOKEN)

        try:
            redis=Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            decode_responses=False
            )
            storage = RedisStorage(redis)
            logger.info('Redis storage is initialized')
        except Exception as error:
            logger.error(f'Failed to create Redis connection: {error}')
        
        dp = Dispatcher(storage=storage)

        try:
            database = Database(config.DB_URL)
            logger.info('Database is initialized')
        except Exception as error:
            logger.critical(f'Failed to create database connection: {error}')
            raise
        dp['database'] = database
        await database.create_all_tables()


        dp.include_routers(*routers)
        app = get_app(bot,dp)

        # web.run_app(app, host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)
        await dp.start_polling(bot)#TODO: Для разработки
        logger.info(f'The server is running on {config.WEBAPP_HOST}:{config.WEBAPP_PORT}')
    except Exception as error:
        logger.critical(f'Error starting the bot: {error}')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as error:
        logger.critical(f'An unexpected error occurred while starting the bot: {error}')