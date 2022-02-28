import json
import requests
from flask import current_app
from slugify import slugify
from src.extensions import cache

@cache.memoize(300)
def parser():
    output = {}
    data = {}

    spreadsheet_id = current_app.config["SPREADSHEET_ID"]
    if spreadsheet_id is not None:

        # make this an env variable
        url = 'http://192.168.1.6:5000/parser/'
        # worksheet names should maybe also be a variable, and we should account for when it's missing.
        params = {'spreadsheet_id': spreadsheet_id, 'worksheet_names': ["Races", "Candidates"]}

        headers = {'Content-Type': 'application/json'}
        result = requests.post(url, data=json.dumps(params), headers=headers)
        result_json = result.json()
    
        if result_json is not None:
            # this should be a variable maybe
            races = result_json["Races"]
            candidates = result_json["Candidates"]

            if races is not None:
                data["races"] = []
                for race in races:
                    # add the office id
                    if race["office"] != None:
                        race["office-id"] = slugify(race["office"], to_lower=True)
                    data["races"].append(race)

            if candidates is not None:
                data["candidates"] = []
                for candidate in candidates:
                    # only load approved candidates
                    if candidate["approved"] != None:
                        candidate["approved"] = True
                        # make an ID
                        candidate_id = candidate["office-sought"].replace(" ", "").lower() + "-" + candidate["name"].replace(" ", "").lower()
                        candidate["candidate-id"] = candidate_id
                        # add the party id
                        if candidate["party"] != None:
                            candidate["party-id"] = slugify(candidate["party"], to_lower=True)
                        # add the race for this candidate
                        race_key = [k for k, race in enumerate(data["races"]) if race["office"] == candidate["office-sought"]][0]
                        candidate["race-id"] = slugify(data["races"][race_key]["office"], to_lower=True)
                        # add to the returnable data
                        data["candidates"].append(candidate)

        output = json.dumps(data)
    else:
        output = {} # something for empty data
    return output
