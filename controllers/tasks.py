import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import db
from models.models import Task

tasks_blueprint = Blueprint('tasks', __name__)

@tasks_blueprint.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """Retrieve the list of all tasks for the current user."""
    user = get_jwt_identity()
    user_id = user.get("user_id")
    
    if user_id is None:
        return jsonify({"msg": "User not found"}), 404
    
    tasks = Task.query.filter_by(user_id=user_id).all()
    tasks_list = [{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks]
    return jsonify(tasks_list), 200

@tasks_blueprint.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    """Add a new task for the current user."""
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed', False)

    if not title or not description:
        return jsonify({"msg": "Title and description are required"}), 400

    user = get_jwt_identity()
    user_id = user.get("user_id")
    
    if user_id is None:
        return jsonify({"msg": "User not found"}), 404

    new_task = Task(title=title, description=description, completed=completed, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description, 'completed': new_task.completed}), 201

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Update an existing task."""
    data = request.get_json()
    task = Task.query.get_or_404(task_id)

    user = get_jwt_identity()
    user_id = user.get("user_id")
    
    if user_id is None:
        return jsonify({"msg": "User not found"}), 404

    if task.user_id != user_id:
        return jsonify({"msg": "Not authorized to update this task"}), 403

    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed')

    if title:
        task.title = title
    if description:
        task.description = description
    if completed is not None:
        task.completed = completed

    db.session.commit()

    return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}), 200

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Remove a task."""
    task = Task.query.get_or_404(task_id)

    user = get_jwt_identity()
    user_id = user.get("user_id")
    
    if user_id is None:
        return jsonify({"msg": "User not found"}), 404

    if task.user_id != user_id:
        return jsonify({"msg": "Not authorized to delete this task"}), 403

    db.session.delete(task)
    db.session.commit()

    return jsonify({"msg": "Task deleted successfully"}), 200

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Retrieve a task by id."""
    task = Task.query.get_or_404(task_id)

    user = get_jwt_identity()
    user_id = user.get("user_id")
    
    if user_id is None:
        return jsonify({"msg": "User not found"}), 404

    if task.user_id != user_id:
        return jsonify({"msg": "Not authorized to view this task"}), 403

    return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}), 200
