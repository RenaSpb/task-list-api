from flask import Blueprint, request, abort, make_response
from ..db import db
from .route_utilities import validate_model, create_model_from_dict
from app.models.task import Task


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model_from_dict(Task, request_body)


