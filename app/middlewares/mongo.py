from datetime import datetime
from datetime import timedelta
from typing import Callable, Any, Awaitable, Dict

from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.types import Message
from aiogram import BaseMiddleware

from pymongo.database import Database
from app.utils.mongodb import MongoDB, User

class DatabaseMiddleware(BaseMiddleware):
    db: Database

    def __init__(
            self, 
            db: Database
        ) -> None:
        self.db = db

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        message = event.message if not hasattr(event, 'chat') else event
        user = event.from_user

        user_data = None
        user_raw_data = await MongoDB.db.users.find_one({"tg_id": user.id})

        if user_raw_data is None:
            user_data = User(
                tg_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            inserted = await MongoDB.db.users.insert_one(user_data.model_dump())
            user_data._id = inserted.inserted_id
        else:
            user_data = User(**user_raw_data)
            print(type(user_data._id))        
            
        data['user_data'] = user_data 
        return await handler(event, data)