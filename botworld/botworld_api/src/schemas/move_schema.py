from pydantic import BaseModel, ConfigDict
from pydantic import constr
from uuid import UUID
from datetime import datetime


class MoveBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    move: constr(min_length=1, max_length=200)




class MoveCreate(MoveBase):
    bot_id: UUID


class MoveGet(MoveBase):
    bot_id: UUID
    created: datetime

