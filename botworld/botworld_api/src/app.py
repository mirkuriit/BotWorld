from flask import Flask
from flasgger import Swagger

from db.extensions import db
from db.extensions import migrate
from api.bot_api import bot_router
from api.move_api import move_router
from errors.errors import MoveNotFoundError, BotNotFoundError
from errors.errors import bot_not_found, move_not_found


def create_app():
    app = Flask(__name__)
    swagger = Swagger(app)
    app.config.from_object("config.DevConfig")

    db.init_app(app=app)
    migrate.init_app(app, db)

    app.register_blueprint(bot_router)
    app.register_blueprint(move_router)
    app.register_error_handler(BotNotFoundError, bot_not_found)
    app.register_error_handler(MoveNotFoundError, move_not_found)

    return app


if __name__ == "__main__":
    app = create_app()
    # with app.app_context():
    #     db.create_all()

    app.run(debug=True)
