import os
import sys
import hashlib
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db import db
from models.models import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"msg": "Username already exists"}), 400

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@user_blueprint.route('/login', methods=['POST'])
def login():
    """Login a user and return a JWT."""
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"msg": "Invalid username or password"}), 401

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    if hashed_password != user.password:
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(
        user={
            "username": username,
            "user_id": user.id
        }
    )

    return jsonify(access_token=access_token), 200
