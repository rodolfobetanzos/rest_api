from flask import request, jsonify, Blueprint
from datetime import datetime
from database import tasks

tasks_bp = Blueprint('routes-tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
def add_tasks():
    title = request.json['title']
    created_date = datetime.now().strftime("%x")
    data = (title, created_date)
    task_id = tasks.insert_task(data)
    if task_id:
        task = tasks.select_task_by_id(task_id)
        return jsonify({'task': task})
    return jsonify({'Message': 'Internal error'})


@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    data = tasks.select_all_tasks()
    if data:
        return jsonify({'tasks': data})
    elif data == False:
        return jsonify({'Message': 'Internal error'})

    else:
        return jsonify({'tasks': {}})


@tasks_bp.route('/tasks', methods=['PUT'])
def update_task():
    title = request.json['title']
    id_arg = request.args.get('id')
    if tasks.update_task(id_arg, (title,)):
        task = tasks.select_task_by_id(id_arg)
        return jsonify(task)
    return jsonify({'Message': 'Internal error'})


@tasks_bp.route('/tasks', methods=['DELETE'])
def delete_task():
    id_arg = request.args.get('id')

    if tasks.delete_task(id_arg):
        return jsonify({'Message': 'Task deleted'})
    return jsonify({'Message': 'Internal error'})


@tasks_bp.route('/tasks/completed', methods=['PUT'])
def complete_task():
    id_arg = request.args.get('id')
    completed = request.args.get('completed')

    if tasks.complete_task(id_arg, completed):
        return jsonify({'Message': 'Sucesfully'})
    return jsonify({'Message': 'Internal error'})