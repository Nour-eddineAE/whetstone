"""Page (view) routes - serve the single-page frontend."""
from flask import Blueprint, current_app, send_from_directory

bp = Blueprint("pages", __name__)


@bp.get("/")
def index():
    return send_from_directory(current_app.static_folder, "index.html")
