from flask import Blueprint
from flask import request, jsonify

from uuid import UUID

from botworld.botworld_api.src.services.move_service import MoveService
from botworld.botworld_api.src.db.tables import Move
from botworld.botworld_api.src.schemas.move_schema import MoveGet, MoveCreate
from botworld.botworld_api.src.errors.errors import MoveNotFoundError



move_router = Blueprint('move', import_name=__name__, url_prefix="/bot-api/")

move_service = MoveService()


@move_router.get("/moves")
def get_moves():
    moves_tmp: list[Move] = move_service.get_list()
    moves = [MoveCreate.model_validate(move, from_attributes=True).model_dump() for move in moves_tmp]
    return jsonify(moves)


