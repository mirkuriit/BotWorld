from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy.sql import func
from botworld.api.src.extensions import db

class Bot(db.Model):
    __tablename__ = "bots"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    llm_full_name = db.Column(db.String(200), nullable=False, unique=True)

    llm_api_link = db.Column(db.String(1000), nullable=False, unique=True)
    llm_source_link = db.Column(db.String(1000), nullable=False)
    # optional
    llm_api_token = db.Column(db.String(1000))

    moves = db.relationship("Move", back_populates="moves", cascade="all, delete")

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return self.llm_full_name

