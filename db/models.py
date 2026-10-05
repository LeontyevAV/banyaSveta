from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Bot(BaseRow):
    id: int
    guid: UUID | None = None
    name: str
    ext_bot_id: int | None = None


class UserTelegram(BaseRow):
    id: int
    guid: UUID | None = None
    user_telegram_id: int
    username: str
    is_bot: bool | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    photo_id: int | None = None
    created_at: datetime
    updated_at: datetime
    bot_id: int
    status: str | None = None


class UserEventType(BaseRow):
    id: int
    guid: UUID | None = None
    name: str


class UserEvent(BaseRow):
    id: int
    guid: UUID | None = None
    ext_id: str
    user_telegram_id: int
    text: str
    user_event_type_id: int
    created_at: datetime
    updated_at: datetime
    date: datetime


class Session(BaseRow):
    id: int
    guid: UUID | None = None
    user_telegram_id: int
    session: str
    created_at: datetime
