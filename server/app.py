from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([msg.to_dict() for msg in messages])

@app.route('/messages/<int:id>', methods=['GET'])
def get_message(id):
    message = Message.query.get(id)
    if message:
        return jsonify(message.to_dict())
    else:
        return jsonify({'error': 'Message not found'}), 404

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    message = Message(body=data.get('body'), username=data.get('username'))
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PUT'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    data = request.get_json()
    if 'body' in data:
        message.body = data['body']

    db.session.commit()
    return jsonify(message.to_dict())


@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted'}), 204

if __name__ == '__main__':
    app.run(port=5555)