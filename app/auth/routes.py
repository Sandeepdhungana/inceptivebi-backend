from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity
)
from app.auth.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.get_user_by_email(data['email']):
        return jsonify({"message": "User already exists"}), 403

    hashed_password = User.hash_password(data['password'])
    new_user = User(
        first_name=data['firstName'], 
        last_name=data['lastName'], 
        email=data['email'], 
        password=hashed_password
    )
    token = create_access_token(identity=data['email'])
    refresh_token = create_refresh_token(identity=data['email'])
    user_status = new_user.save_to_db()
    if user_status:
        return jsonify({
            'token': token,
            'refresh_token': refresh_token
        }), 200

    return jsonify({"message": "Something went wrong while registering user"}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.get_user_by_email(data['email'])
    print("The email is ", data['email'])
    print("the password is ", data['password'])
    print("the user is ", user)

    if user and user.verify_password(data['password']):
        token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)
        return jsonify({
            'token': token,
            'refresh_token': refresh_token
        }), 200

    return jsonify({"message": "Invalid Credentials"}), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify({"token": access_token}), 200



@auth_bp.route('/get-user-details', methods=['GET'])
@jwt_required()
def get_user_details():
    user_identity = get_jwt_identity()
    user_details = User().get_user_by_email(user_identity)
    return {
        "name":user_details.first_name
    }