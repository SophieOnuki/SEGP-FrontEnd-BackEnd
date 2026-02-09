from flask import Blueprint
from .BackEnd import bp as backend_bp
from .Predictions import bp as predictions_bp

def register_routes(app):
    app.register_blueprint(backend_bp, url_prefix='/api')
    app.register_blueprint(predictions_bp, url_prefix='/api')

