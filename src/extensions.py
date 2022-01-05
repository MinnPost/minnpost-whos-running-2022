from src.cache import cache
from src.logger import TrackerLogger

def register_extensions(app):

    cache.init_app(app)

    app.log = TrackerLogger('tracker_results').logger
