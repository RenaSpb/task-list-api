from flask import Blueprint, request, Response
from ..db import db
from .route_utilities import validate_model, create_model_from_dict
from app.models.goal import Goal
from app.models.task import Task


goals_bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model_from_dict(Goal, request_body)

@goals_bp.get("")
def get__all_goals():
    query = db.select(Goal)
    query = query.order_by(Goal.id)
    tasks = db.session.scalars(query).all()

    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response

@goals_bp.get("<goal_id>")
def get_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    return { "goal": goal.to_dict() }

@goals_bp.put("<goal_id>")
def update_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goals_bp.delete("<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goals_bp.post("<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    task_ids = request.get_json().get("task_ids", [])

    goal.tasks = [validate_model(Task, task_id) for task_id in task_ids]
    
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200

    
@goals_bp.get("<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]

    return goal_dict, 200
