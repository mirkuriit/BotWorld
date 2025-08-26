from flask import Blueprint
from flask import request, jsonify

from uuid import UUID

from botworld.botworld_api.src.services.bot_service import BotService
from botworld.botworld_api.src.db.tables import Bot
from botworld.botworld_api.src.schemas.bot_schema import BotCreate, BotGet, BotUpdate
from botworld.botworld_api.src.errors.errors import BotNotFoundError



bot_router = Blueprint('bot', import_name=__name__, url_prefix="/bot-api/")

bot_service = BotService()


@bot_router.get("/bots")
def get_bots():
    """
    Get all bots
    ---
    tags:
      - Bots
    responses:
      200:
        description: List of all bots
        schema:
          type: array
          items:
            properties:
              id:
                type: string
                format: uuid
              llm_full_name:
                type: string
              llm_api_link:
                type: string
              llm_source_link:
                type: string
              llm_api_token:
                type: string
                nullable: true
              created:
                type: string
                format: date-time
              updated:
                type: string
                format: date-time
    """
    bots_tmp: list[Bot] = bot_service.get_list()
    bots = [BotGet.model_validate(b, from_attributes=True).model_dump() for b in bots_tmp]
    return jsonify(bots)


@bot_router.get("/bots/<uuid:id>")
def get_bot(id: UUID):
    """
    Get a bot by ID
    ---
    tags:
      - Bots
    parameters:
      - name: id
        in: path
        type: string
        format: uuid
        required: true
        description: Bot UUID
    responses:
      200:
        description: Bot details
        schema:
          type: object
          properties:
            id: {type: string, format: uuid}
            llm_full_name: {type: string}
            llm_api_link: {type: string}
            llm_source_link: {type: string}
            llm_api_token: {type: string, nullable: true}
            created: {type: string, format: date-time}
            updated: {type: string, format: date-time}
      404:
        description: Bot not found
    """
    bot: Bot = bot_service.get(id=id)
    if bot is None:
        raise BotNotFoundError
    return jsonify(BotGet.model_validate(bot, from_attributes=True).model_dump())


@bot_router.post("/bots")
def create_bot():
    """
    Create a new bot
    ---
    tags:
      - Bots
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - llm_full_name
            - llm_api_link
            - llm_source_link
            - llm_api_token
          properties:
            llm_full_name: {type: string, example: "GPT-5 Bot"}
            llm_api_link: {type: string, example: "https://api.example.com/llm"}
            llm_source_link: {type: string, example: "https://github.com/org/bot"}
            llm_api_token: {type: string, example: "secret-token"}
    responses:
      200:
        description: Successfully created bot
    """
    data = request.json
    bot_schema = BotCreate(**data)
    bot = bot_service.create(bot_schema=bot_schema)
    return jsonify(BotGet.model_validate(bot).model_dump())


@bot_router.patch("/bots/<uuid:id>")
def update_bot(id):
    """
    Update a bot by ID
    ---
    tags:
      - Bots
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
          properties:
            llm_full_name: {type: string}
            llm_api_link: {type: string}
            llm_source_link: {type: string}
            llm_api_token: {type: string}
    responses:
      200:
        description: Successfully updated bot
      404:
        description: Bot not found
    """
    data = request.json
    bot_schema = BotUpdate(**data)
    bot_service.update(id=id, bot_schema=bot_schema)
    return jsonify(bot_schema.model_dump())


@bot_router.delete("/bots/<uuid:id>")
def delete_bot(id):
    """
    Delete a bot by ID
    ---
    tags:
      - Bots
    parameters:
      - name: id
        in: path
        type: string
        format: uuid
        required: true
        description: Bot UUID
    responses:
      200:
        description: Successfully deleted bot
        schema:
          type: object
          properties:
            id: {type: string, format: uuid}
            llm_full_name: {type: string}
            llm_api_link: {type: string}
            llm_source_link: {type: string}
            llm_api_token: {type: string}
      404:
        description: Bot not found
    """
    bot: Bot = bot_service.delete_by_id(id=id)
    return jsonify(bot.toDict())

