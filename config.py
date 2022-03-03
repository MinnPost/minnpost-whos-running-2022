import os
import json
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    BASE_DIR = Path(__file__).parent.parent
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    API_CACHE_TIMEOUT = os.environ.get("API_CACHE_TIMEOUT", 500)
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "")
    PARSER_API_URL = os.environ.get("PARSER_API_URL", "")
    OVERWRITE_API_URL = os.environ.get("OVERWRITE_API_URL", "")
    WORKSHEET_NAMES = json.loads(os.environ.get("WORKSHEET_NAMES", '["Sheet1"]'))
