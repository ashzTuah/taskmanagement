#from flask import Blueprint, request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from marshmallow import Schema, fields

from models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

#auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

auth_bp = Blueprint("Auth", "auth", url_prefix="/auth", description="Auth APIs")

class AuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class TokenSchema(Schema):
    access_token = fields.Str()

class MessageSchema(Schema):
    msg = fields.Str()

@auth_bp.route("/register")
class RegisterResource(MethodView):
    #@auth_bp.route("/auth/register", methods=["POST"])
    #def register():
    #    data = request.get_json()

    #    if not data.get("email") or not data.get("password"):
    #        return jsonify({"msg": "Missing email or password"}), 400
    @auth_bp.arguments(AuthSchema)
    @auth_bp.response(201, MessageSchema)
    def post(self, data):

        if User.query.filter_by(email=data["email"]).first():
            #return jsonify({"msg": "User already exists"}), 400
            return {"msg": "User already exists"}, 400

        hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

        user = User(email=data["email"], password_hash=hashed)
        db.session.add(user)
        db.session.commit()

        #return jsonify({"msg": "User registered"}), 201
        return {"msg": "User registered"}

@auth_bp.route("/login")
class LoginResource(MethodView):
# @auth_bp.route("/auth/login", methods=["POST"])
# def login():
#     data = request.get_json()
    @auth_bp.arguments(AuthSchema)
    @auth_bp.response(200, TokenSchema)
    def post(self, data):
        user = User.query.filter_by(email=data.get("email")).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, data.get("password")):
            #return jsonify({"msg": "Invalid credentials"}), 401
            return {"msg": "Invalid credentials"}, 401

        token = create_access_token(identity=user.id)

        # return jsonify({"access_token": token})
        return {"access_token": token}