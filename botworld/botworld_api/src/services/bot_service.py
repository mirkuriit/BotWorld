from db.tables import Bot
from schemas.bot_schema import BotCreate

from db.extensions import db
from schemas.bot_schema import BotUpdate
from sqlalchemy.orm import selectinload
from uuid import UUID

import sqlalchemy as sa


class BotService:
    def create(self, bot_schema: BotCreate) -> Bot:
        bot = Bot(**bot_schema.model_dump())
        db.session.add(bot)
        db.session.commit()
        return bot

    def get(self, id: UUID) -> Bot:
        bot = db.session.scalar(sa.select(Bot).filter_by(id=id))
        if not bot:
            return None
        return bot

    def get_list(self) -> list[Bot]:
        bot = db.session.scalars(sa.select(Bot).options(selectinload(Bot.moves)))

        return list(bot)

    def delete_by_id(self, id: UUID) -> Bot:
        bot = db.session.scalar(sa.select(Bot).filter_by(id=id))
        if not bot:
            return None
        db.session.delete(bot)
        db.session.commit()
        return bot

    def update(self, id: UUID, bot_schema: BotUpdate) -> Bot:
        bot = db.session.scalar(sa.select(Bot).filter_by(id=id))
        if not bot:
            return None

        for key, value in bot_schema.model_dump(exclude_unset=True).items():
            setattr(bot, key, value)
        db.session.commit()
        return bot


