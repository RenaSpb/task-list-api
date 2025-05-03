from flask import Blueprint, request, abort, make_response, Response
from ..db import db
from .route_utilities import validate_model, create_model_from_dict
from app.models.task import Task
from datetime import datetime


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model_from_dict(Task, request_body)


@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    sort_param = request.args.get("sort")

    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    
    if sort_param == "desc":
        query = query.order_by(Task.title.desc())

    query = query.order_by(Task.id)
    tasks = db.session.scalars(query).all()

    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response

@tasks_bp.get("<task_id>")
def get_task_by_id(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}

@tasks_bp.put("<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("<task_id>/mark_complete")
def mark_complete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.today()
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("<task_id>/mark_incomplete")
def mark_incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")
