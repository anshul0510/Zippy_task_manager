from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())
    
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    completed_filter = request.args.get("completed")  

    query = Task.query.filter_by(user_id=user_id)
    
    if completed_filter is not None:
        if completed_filter.lower() == "true":
            query = query.filter_by(completed=True)
        elif completed_filter.lower() == "false":
            query = query.filter_by(completed=False)
        else:
            return jsonify({"error": "Invalid value for completed filter. Use 'true' or 'false'."}), 400

    pagination = query.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    tasks = pagination.items

    result = {
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "created_at": t.created_at.isoformat(),
                "updated_at": t.updated_at.isoformat()
            } for t in tasks
        ],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "total_tasks": pagination.total
    }
    
    return jsonify(result)

@task_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_task(id):
    task = db.session.get(Task, id)
    if not task:
        abort(404, description="Task not found")
    return jsonify({"id": task.id, "title": task.title, "completed": task.completed})

@task_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    new_task = Task(title=data["title"], description=data.get("description"), user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created"}), 201

@task_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    task = db.session.get(Task, id)
    if not task:
        abort(404, description="Task not found")
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)
    db.session.commit()
    return jsonify({"message": "Task updated"})

@task_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    task = db.session.get(Task, id)
    if not task:
        abort(404, description="Task not found")
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
