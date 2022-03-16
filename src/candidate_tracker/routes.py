import json
from flask import Response, render_template
from src import spreadsheet
from src.candidate_tracker import bp
#from src.candidate_tracker.errors import bad_request

@bp.route("/", methods=['GET'])
def index():
    output = spreadsheet.parser()
    output = json.loads(output)
    return render_template('summary.html', output=output)


@bp.route("/json/", methods=['GET'])
def index_json():
    output = spreadsheet.parser()
    mime = 'application/json'
    ctype = 'application/json; charset=UTF-8'
    res = Response(response = output, status = 200, mimetype = mime)
    res.headers["Content-Type"] = ctype
    res.headers["Connection"] = "keep-alive"
    res.headers["Access-Control-Allow-Origin"] = "*"
    return res
