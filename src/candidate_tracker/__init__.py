from flask import Blueprint, render_template

bp = Blueprint('candidate_tracker', __name__, template_folder="templates")

from src.candidate_tracker import routes
