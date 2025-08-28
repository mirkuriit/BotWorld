from flask import Blueprint
from flask import request, jsonify

from uuid import UUID

from services.move_service import MoveService
from db.tables import Move
from schemas.move_schema import MoveGet, MoveCreate
from errors.errors import MoveNotFoundError



move_router = Blueprint('move', import_name=__name__, url_prefix="/bot-api/")

move_service = MoveService()


@move_router.get("/moves")
def get_moves():
    """
    Get all moves
    ---
    tags:
      - Moves
    responses:
      200:
        description: List of all moves
        schema:
          type: array
          items:
            properties:
              bot_id: {type: string, format: uuid}
              move: {type: string}
              created: {type: string, format: date-time}
    """
    moves_tmp: list[Move] = move_service.get_list()
    moves = [MoveGet.model_validate(move, from_attributes=True).model_dump() for move in moves_tmp]
    return jsonify(moves)


@move_router.get("/bots/<uuid:id>/moves")
def get_moves_by_bot_id(id):
    """
    Get moves by bot ID
    ---
    tags:
      - Moves
    parameters:
      - name: id
        in: path
        type: string
        format: uuid
        required: true
        description: Bot UUID
    responses:
      200:
        description: List of moves for the bot
        schema:
          type: array
          items:
            properties:
              bot_id: {type: string, format: uuid}
              move: {type: string}
              created: {type: string, format: date-time}
      404:
        description: Bot or moves not found
    """
    moves_tmp: list[Move] = move_service.get_by_bot_id(id=id)
    moves = [MoveGet.model_validate(move, from_attributes=True).model_dump() for move in moves_tmp]
    return jsonify(moves)


@move_router.post("/bots/<uuid:id>/moves")
def create_move(id):
    """
    Create a new move for a bot
    ---
    tags:
      - Moves
    parameters:
      - name: id
        in: path
        type: string
        format: uuid
        required: true
        description: Bot UUID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - move
          properties:
            move:
              type: string
              minLength: 1
              maxLength: 200
              example: "attack_left"
    responses:
      200:
        description: Successfully created move
        schema:
          type: object
          properties:
            bot_id: {type: string, format: uuid}
            move: {type: string}
      400:
        description: Invalid input data
    """
    data = request.json
    move_schema = MoveCreate(bot_id=id, move=data["move"])
    move_service.create(move_schema)
    return jsonify(move_schema.model_dump())






