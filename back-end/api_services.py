from flask import jsonify, request
from run_server import app

tasks = [
    {'id': 1, 'title': 'Learn Flask', 'done': False},
    {'id': 2, 'title': 'Build a REST API', 'done': False},
]

@app.route('/tasks', methods=['GET']) 
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task': task})

@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = request.json
    print(new_task)
    tasks.append(new_task)
    return jsonify({'task': new_task}), 201

@app.route('/operation', methods=['POST'])
def do_operation():
    new_operation = request.json