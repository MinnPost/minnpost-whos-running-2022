import os
from flask import Flask, jsonify, current_app

from src.extensions import register_extensions

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)

    #from src.errors import bp as errors_bp
    #app.register_blueprint(errors_bp)

    from src.candidate_tracker import bp as candidate_tracker_bp
    app.register_blueprint(candidate_tracker_bp, url_prefix='/candidate-tracker')

    return app

from src import spreadsheet
