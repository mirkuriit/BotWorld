from botworld.botworld_api.src.db.tables import Move
from botworld.botworld_api.src.schemas.move_schema import MoveCreate

from botworld.botworld_api.src.db.extensions import db
from uuid import UUID

import sqlalchemy as sa


class MoveService:
    def create(self, move_schema: MoveCreate) -> Move:
        move = Move(**move_schema.model_dump())
        db.session.add(move)
        db.session.commit()
        return move

    def get(self, id: UUID) -> Move | None:
        move = db.session.scalar(sa.select(Move).filter_by(id=id))
        if not move:
            return None
        return move

    def get_list(self) -> list[Move]:
        moves = db.session.scalars(sa.select(Move))
        return list(moves)

    def get_by_bot_id(self, id: UUID) -> list[Move]:
        moves = db.session.scalars(sa.select(Move).filter_by(bot_id=id))
        return list(moves)

    def delete_by_id(self, id: UUID) -> Move | None:
        move = db.session.scalar(sa.select(Move).filter_by(id=id))
        if not move:
            return None
        db.session.delete(move)
        db.session.commit()
        return move
