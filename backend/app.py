import os
from flask import Flask
from flask_smorest import Api
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from dotenv import load_dotenv



# laod env
load_dotenv()

app = Flask(__name__)

app.config.from_object(Config)

port = int(os.getenv("WEB_PORT", 5000))
server = str(os.getenv("SERVER", "127.0.0.1"))
# allow cors
# CORS(
#     app,
#     #resources={r"/*": {"origins": f"http://{server}:{port}"}},
#     resources={r"/*": {"origins": "*"}},
#     supports_credentials=True,
#     expose_headers=["Authorization"],
#     allow_headers=["Content-Type", "Authorization"]
# )
CORS(
    app,
    # resources={r"/*": {"origins": "http://localhost:3000"}},
    resources={r"/*": {"origins": "*"}},
    # supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)
# Swagger config
app.config["API_TITLE"] = "Task API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["OPENAPI_SPEC_OPTIONS"] = {
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
    "security": [{"BearerAuth": []}]
}

db.init_app(app)
jwt = JWTManager(app)
api = Api(app)

api.register_blueprint(auth_bp)
api.register_blueprint(tasks_bp)

# Define JWT bearer security scheme for Swagger
api.spec.components.security_scheme("BearerAuth", {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
})
# api.spec.security = [{"BearerAuth": []}]

@app.route("/")
def home():
    return {"msg": "Task Manager API running"}

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", 7000))
    host = os.getenv("SERVER", "127.0.0.1")

    with app.app_context():
        db.create_all()

    app.run(debug=True, host=host, port=port)