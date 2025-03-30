import re
import asyncio
import logging

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject, or_f, and_f
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    JOIN_TRANSITION,
    LEAVE_TRANSITION,
)
from aiogram.filters.command import CommandStart, Command
from aiogram.types import ChatMemberUpdated, Message
from app.utils.mongodb import MongoDB


from app.utils.mongodb import MongoDB, Chat
from app.settings import SETTINGS

router = Router()


###
### Start Command Callback
###
@router.message(Command(commands={"start"}), F.chat.type == "private")
async def start_command_handler(message: Message, command: CommandObject) -> None:
    await message.answer("👋 Привет!")


# ###
# ### Added to chat callback
# ###
# @router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
# async def on_bot_added_to_chat(event: ChatMemberUpdated):
#     logging.info(f"Bot has been added to chat {event.chat.id}")
#     chat = await MongoDB.db.chats.find_one({"chat_id": event.chat.id})
#     if chat is None:
#         chat_data = Chat(
#             is_member=True,
#             chat_id=event.chat.id,
#             chat_type=event.chat.type,
#             added_by=event.from_user.id,
#             name=event.chat.title
#         )
#         inserted = await MongoDB.db.chats.insert_one(chat_data.model_dump())
#         chat_data._id = inserted.inserted_id
#     else:
#         chat_data = Chat(**chat)
#         chat_data.is_member = True
#         chat_data.added_by = event.from_user.id
#         chat_data.chat_type = event.chat.type
#         chat_data.name = event.chat.title
#         await MongoDB.db.chats.update_one(
#             {"_id": chat_data._id},
#             {"$set": chat_data.model_dump()}
#         )

#     msg = f"""
# Привет 👋
# chat_id: <code>{event.chat.id}</code>
# """
#     await event.bot.send_message(chat_id=event.chat.id, text=msg, parse_mode="HTML")

# ###
# ### Removed from chat callback
# ###
# @router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
# async def on_bot_removed_from_chat(event: ChatMemberUpdated):
#     logging.info(f"Bot has been removed from chat {event.chat.id}")
#     chat = await MongoDB.db.chats.find_one({"chat_id": event.chat.id})
#     if chat is None:
#         chat_data = Chat(
#             is_member=False,
#             chat_id=event.chat.id,
#             chat_type=event.chat.type,
#             added_by=event.from_user.id,
#             name=event.chat.title,
#         )
#         inserted = await MongoDB.db.chats.insert_one(chat_data.model_dump())
#         chat_data._id = inserted.inserted_id
#     else:
#         chat_data = Chat(**chat)
#         chat_data.is_member = False
#         chat_data.chat_type = event.chat.type
#         chat_data.name = event.chat.title
#         await MongoDB.db.chats.update_one(
#             {"_id": chat_data._id},
#             {"$set": chat_data.model_dump()}
#         )
