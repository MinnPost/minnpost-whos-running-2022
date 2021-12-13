from src.cache import cache
from src.logger import ScraperLogger

def register_extensions(app, worker=False):

    cache.init_app(app)

    app.log = ScraperLogger('scraper_results').logger
