import uuid

from datetime import datetime
from sqlalchemy.sql import func
from botworld.api.src.extensions import db
from sqlalchemy.dialects.postgresql import UUID

from flask_sqlalchemy import SQLAlchemy

class Move(db.Model):
    __tablename__ = "moves"


    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    bot_id = db.Column(UUID(as_uuid=True), db.ForeignKey("bots.id"), nullable=False)
    bot = db.relationship("Bot", back_populates="moves")
