from flask.views   import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash  import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, create_refresh_token, get_jwt_identity
from blocklist import BLOCKLIST

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="User operations")

@blp.route("/register")
class RegisterUser(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(201, example={"message": "User created successfully"})
    def post(self, user):
        if UserModel.query.filter(UserModel.username == user["username"]).first():
            abort(409, message="User already exists")

        user = UserModel(
            username = user["username"],
            password = pbkdf2_sha256.hash(user["password"])
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    
@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(401, message="Invalid username or password")

@blp.route("/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, fresh=False)
        return {"access_token": access_token}

@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}

@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.response(204)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return 204