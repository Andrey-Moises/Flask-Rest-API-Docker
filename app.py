
import os
from   db              import db
import models
import secrets
from   blocklist          import BLOCKLIST
from   flask              import Flask
from   flask_smorest      import Api
from   flask_jwt_extended import JWTManager
from   resources.items    import blp as items_blp
from   resources.store    import blp as store_blp
from   resources.tag      import blp as tag_blp
from   resources.user     import blp as user_blp
from   flask              import jsonify
from   flask_migrate      import Migrate
from   dotenv             import load_dotenv

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"]           = True
    app.config["API_TITLE"]                      = "Store REST API"
    app.config["API_VERSION"]                    = "1.0"
    app.config["OPENAPI_VERSION"]                = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"]             = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]        = "/"
    app.config["OPENAPI_SWAGGER_UI_URL"]         = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"]        = db_url or os.environ.get("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)
    
    app.config["JWT_SECRET_KEY"] = "235561265360160791118794708550328371846"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
       return jwt_payload["jti"] in BLOCKLIST # This function is used to check if a token is in the blocklist
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload): # This function is used to check if a token has been revoked
        return (jsonify({
            "description": "The token has been revoked",
            "error": "token_revoked"
        }), 401)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity): # This function is used to add extra data to the JWT token
        if identity == "10":
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(header, payload):
        return (jsonify({
            "description": "The token has expired",
            "error": "token_expired"
        }), 401)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({
            "description": "Signature verification failed",
            "error": "invalid_token"
        }), 401)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({
            "description": "Request does not contain an access token",
            "error": "authorization_required"
        }), 401)

    # with app.app_context():
    #     db.create_all() # para crear todo el esquema de la base de datos, diferente de flask_migration

    api.register_blueprint(items_blp)
    api.register_blueprint(store_blp)
    api.register_blueprint(tag_blp)
    api.register_blueprint(user_blp)

    return app

