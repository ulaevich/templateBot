import logging
import asyncio

from bson import ObjectId
from typing import Iterable

from datetime import datetime
from pydantic import BaseModel, Field
from pymongo.database import Database
from motor.motor_asyncio import AsyncIOMotorClient

from app.utils.pydantic_objectid import PydanticObjectId


class MongoObject(BaseModel):
    _id: PydanticObjectId

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._id = kwargs.get("_id")

    def model_dump(self, include_id: bool = False, **kwargs):
        dump = super().model_dump(**kwargs)
        if include_id:
            dump["_id"] = str(self._id)
        return dump


class User(MongoObject):
    _id: PydanticObjectId
    tg_id: int
    username: str
    first_name: str
    last_name: str | None
    reg_date: datetime = Field(default_factory=lambda: datetime.now())
    last_update: datetime = Field(default_factory=lambda: datetime.now())
    role: str = Field(default_factory=lambda: "user")
    banned: bool = Field(default_factory=lambda: False)
    subscription: dict | None = Field(default_factory=lambda: None)


class Chat(MongoObject):
    _id: PydanticObjectId
    chat_id: int
    chat_type: str
    is_member: bool
    added_by: int
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class MongoDB:
    client: AsyncIOMotorClient  # type: ignore
    db: Database

    @classmethod
    def setup(cls, mongodb_url: str, mongodb_db: str) -> None:
        cls.client = AsyncIOMotorClient(mongodb_url)
        cls.db = cls.client.get_database(mongodb_db)

        try:
            cls.client.admin.command("ping")
            logging.info("Connected to MongoDB")
        except Exception as e:
            logging.error(f"Exception while connecting to MongoDB: {e}")

    @classmethod
    async def update_field(
        cls, collection: str, _id: ObjectId, path: Iterable[str], value: any
    ):
        """
        {a: {b: True} }\n
        path to `b`: ('a', 'b')
        """
        path_str = ".".join(path)
        collection = MongoDB.db.get_collection(collection)
        await collection.update_one(
            filter={"_id": _id}, update={"$set": {path_str: value}}
        )

    @classmethod
    def get_database(cls) -> Database:
        return cls.db
