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
    bots_tmp: list[Bot] = bot_service.get_list()
    bots = [(BotGet.model_validate(b, from_attributes=True)).model_dump() for b in bots_tmp]
    return jsonify(bots)


@bot_router.get("/bots/<uuid:id>")
def get_bot(id: UUID):
    bot: Bot = bot_service.get(id=id)
    if bot is None:
        raise BotNotFoundError
    return jsonify(BotGet.model_validate(bot, from_attributes=True).model_dump())


@bot_router.post("/bots")
def create_bot():
    print(request)
    data = request.json
    bot_schema = BotCreate(**data)
    bot_service.create(bot_schema=bot_schema)
    return jsonify(bot_schema.model_dump())


@bot_router.patch("/bots/<uuid:id>")
def update_bot(id):
    print(request)
    data = request.json
    bot_schema = BotUpdate(**data, )
    bot_service.update(
        id=id,
        bot_schema=bot_schema)
    return jsonify(bot_schema.model_dump())


@bot_router.delete("/bots/<uuid:id>")
def delete_bot(id):
    bot: Bot = bot_service.delete_by_id(id=id)
    return jsonify(bot.toDict())
