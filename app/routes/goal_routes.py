from flask import Blueprint, request, Response
from ..db import db
from .route_utilities import validate_model, create_model_from_dict
from app.models.goal import Goal


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

    return {"goal": goal.to_dict()}

@goals_bp.put("<goal_id>")
def update_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goals_bp.delete("<goal_id>")
def delete_task(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")