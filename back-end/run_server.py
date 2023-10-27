from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
