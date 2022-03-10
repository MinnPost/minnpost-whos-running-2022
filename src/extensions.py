from src.logger import TrackerLogger

def register_extensions(app):

    app.log = TrackerLogger('tracker_results').logger
