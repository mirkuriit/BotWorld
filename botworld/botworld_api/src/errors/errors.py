from werkzeug.exceptions import HTTPException
from flask import jsonify

class BotNotFoundError(HTTPException):
    code = 404
    description = "Bot not found"

    @staticmethod
    def to_dict(self):
        return {"code": self.code, "description": self.description}


class MoveNotFoundError(HTTPException):
    code = 404
    description = "Move not found"

    @staticmethod
    def to_dict(self):
        return {"code": self.code, "description": self.description}


def bot_not_found(e: BotNotFoundError):
    data = e.to_dict()
    return jsonify(data), e.code

def move_not_found(e: MoveNotFoundError):
    print(e)
    data = e.to_dict()
    return jsonify(data), e.code


not_found_errors = [move_not_found, bot_not_found]