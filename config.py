import os
import json
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    BASE_DIR = Path(__file__).parent.parent
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    API_CACHE_TIMEOUT = os.environ.get("API_CACHE_TIMEOUT", 500)
    API_KEY = os.environ.get("API_KEY", "")
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "")
    AUTHORIZE_API_URL = os.environ.get("AUTHORIZE_API_URL", "")
    PARSER_API_URL = os.environ.get("PARSER_API_URL", "")
    OVERWRITE_API_URL = os.environ.get("OVERWRITE_API_URL", "")
    WORKSHEET_NAMES = json.loads(os.environ.get("WORKSHEET_NAMES", '["Sheet1"]'))
    STORE_IN_S3 = os.environ.get("STORE_IN_S3", "")
