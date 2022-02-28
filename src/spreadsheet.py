import json
import datetime
import requests
from flask import current_app
from slugify import slugify

def parser():
    output = {}
    data = {}
    result_json = None

    spreadsheet_id = current_app.config["SPREADSHEET_ID"]
    worksheet_names = current_app.config["WORKSHEET_NAMES"]
    if spreadsheet_id is not None:
        url = current_app.config["PARSER_API_URL"]
        if url != "":
            params = {"spreadsheet_id": spreadsheet_id, "worksheet_names": worksheet_names}
            headers = {'Content-Type': 'application/json'}
            result = requests.post(url, data=json.dumps(params), headers=headers)
            result_json = result.json()
    
        if result_json is not None:
            if "customized" in result_json:
                output = json.dumps(result_json, default=str)
            else:
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
                
                # set metadata and send the customized json output to the api
                if "generated" in result_json:
                    data["generated"] = result_json["generated"]
                data["customized"] = datetime.datetime.now()
                output = json.dumps(data, default=str)
                
                overwrite_url = current_app.config["OVERWRITE_API_URL"]
                params = {"spreadsheet_id": spreadsheet_id, "worksheet_names": worksheet_names, "output": output}

                headers = {'Content-Type': 'application/json'}
                result = requests.post(overwrite_url, data=json.dumps(params), headers=headers)
                result_json = result.json()
                if result_json is not None:
                    output = json.dumps(result_json, default=str)

    else:
        output = {} # something for empty data
    return output
