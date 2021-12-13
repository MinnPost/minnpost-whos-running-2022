import json
from flask import jsonify, Response, current_app
from src.extensions import cache
from src import spreadsheet
from src.candidate_tracker import bp
#from src.candidate_tracker.errors import bad_request

@bp.route("/", methods=['GET'])
@cache.cached(timeout=30, query_string=True)
def index():
    data = []
    spreadsheet_id = current_app.config["SPREADSHEET_ID"]
    if spreadsheet_id is not None:
        races = spreadsheet.read_spreadsheet(spreadsheet_id, "Races")
        candidates = spreadsheet.read_spreadsheet(spreadsheet_id, "Candidates")

        if races is not None:
            for race in races:
                if candidates is not None:
                    race["candidates"] = {}
                    for candidate in candidates:
                        candidate_id = candidate["office-sought"].replace(" ", "").lower() + "-" + candidate["name"].replace(" ", "").lower()
                        candidate["candidate_id"] = candidate_id
                        if candidate["office-sought"] == race["office"]:
                            if candidate["party"] in race["candidates"]:
                                race["candidates"][candidate["party"]].append(candidate)
                            else:
                                race["candidates"][candidate["party"]] = [candidate]
                data.append(race)
        output = json.dumps(data)
    else:
        output = {} # something for empty data
    
    mime = 'application/json'
    ctype = 'application/json; charset=UTF-8'

    res = Response(response = output, status = 200, mimetype = mime)
    res.headers['Content-Type'] = ctype
    res.headers['Connection'] = 'keep-alive'
    return res