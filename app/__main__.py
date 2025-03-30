import asyncio
import logging
import app.logger as logger

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.settings import SETTINGS
from app.middlewares import *
from app.storage import get_storage, get_events_isolation
from app.routers import setup_error_handler
from app.routers import router as main_router
from app.utils.mongodb import MongoDB

logger.setup()

async def main():
    bot = Bot(SETTINGS.BOT_TOKEN.get_secret_value())
    
    # Setup database
    MongoDB.setup(
        SETTINGS.MONGODB_URL.get_secret_value(), 
        SETTINGS.MONGODB_DB.get_secret_value(),
    )

    dp = Dispatcher(
        storage=get_storage(),
        events_isolation=get_events_isolation(),
    )

    # Registering middlewares
    db_middleware = DatabaseMiddleware(MongoDB.get_database())
    dp.message.middleware(db_middleware)
    dp.callback_query.middleware(db_middleware)
    dp.chat_member.middleware(db_middleware)

    # Registering error handler
    setup_error_handler(SETTINGS.LOGGING_CHAT, bot)

    # Registering routers
    dp.include_router(main_router)

    loop = asyncio.get_running_loop()
    loop.create_task(
        dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()        
        ),
    )
    
if __name__ == "__main__":
    logging.warning("Starting bot")
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()
    logging.warning("Bot stopped")