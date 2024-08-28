import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from db import db
from controllers.users import user_blueprint
from controllers.tasks import tasks_blueprint

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    app.register_blueprint(user_blueprint, url_prefix="/api")
    app.register_blueprint(tasks_blueprint, url_prefix="/api")

    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy"
        })

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)