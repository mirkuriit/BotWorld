from pydantic import BaseModel, ConfigDict
from pydantic import HttpUrl, constr
from uuid import UUID
from datetime import datetime

from schemas.move_schema import MoveGet

from typing import Optional

class BotBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BotCreate(BotBase):
    llm_full_name: str

    llm_api_link: str
    llm_source_link: str
    llm_api_token: str


class BotUpdate(BotBase):
    llm_full_name: Optional[str] = None

    llm_api_link: Optional[str] = None
    llm_source_link: Optional[str] = None
    llm_api_token: Optional[str] = None


class BotGet(BotBase):
    id: UUID
    created: datetime
    updated: datetime

    llm_full_name: str

    llm_api_link: str
    llm_source_link: str
    llm_api_token: str | None
    #moves: list[MoveGet]





