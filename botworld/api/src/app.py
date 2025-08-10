import os
from typing import Literal
from flask import Flask

from botworld.api.src.extensions import db
from botworld.api.src.extensions import migrate
from config import config

from models.bot_model import Bot


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    db.init_app(app)
    # migrate.init_app(app, db)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
