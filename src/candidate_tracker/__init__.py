from flask import Blueprint

bp = Blueprint('candidate_tracker', __name__)

from src.candidate_tracker import routes
