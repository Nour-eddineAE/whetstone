"""Flask web app: a thin UI over pengine. Application factory."""
from flask import Flask


def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="")
    from .routes.pages import bp as pages_bp
    from .routes.api import bp as api_bp
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    return app
