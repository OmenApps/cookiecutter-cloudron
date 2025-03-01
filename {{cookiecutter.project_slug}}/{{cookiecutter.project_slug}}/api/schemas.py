# Import all API routes
from datetime import datetime
from typing import Optional

from ninja import Schema

from . import api, errors, health  # noqa


class ErrorSchema(Schema):
    message: str
    code: Optional[str] = None
    details: Optional[dict] = None


class MessageSchema(Schema):
    message: str


class HealthSchema(Schema):
    status: str
    version: str
    timestamp: datetime


class DetailedHealthSchema(HealthSchema):
    database: bool
    cache: bool
    {% if cookiecutter.use_redis == "yes" %}redis: bool{% endif %}
    storage: bool
