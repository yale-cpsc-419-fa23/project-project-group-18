from flask import Flask, jsonify, request
from flask_cors import CORS
from api_services import socketio, app



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
