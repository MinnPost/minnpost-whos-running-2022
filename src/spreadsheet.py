import json
import datetime
from datetime import timedelta
import requests
from flask import current_app
from slugify import slugify

def parser():
    output = {}
    data = {}
    result_json = None

    spreadsheet_id = current_app.config["SPREADSHEET_ID"]
    worksheet_names = current_app.config["WORKSHEET_NAMES"]
    cache_timeout = int(current_app.config["API_CACHE_TIMEOUT"])
    store_in_s3 = current_app.config["STORE_IN_S3"]
    if spreadsheet_id is not None:
        api_key = current_app.config["API_KEY"]
        authorize_url = current_app.config["AUTHORIZE_API_URL"]
        url = current_app.config["PARSER_API_URL"]
        if authorize_url != "" and api_key != "" and url != "":
            token_params = {
                "api_key": api_key
            }
            token_headers = {'Content-Type': 'application/json'}
            token_result = requests.post(authorize_url, data=json.dumps(token_params), headers=token_headers)
            token_json = token_result.json()
            if token_json["token"]:
                token = token_json["token"]
                authorized_headers = {"Authorization": f"Bearer {token}"}
                worksheet_slug = '|'.join(worksheet_names)
                result = requests.get(f"{url}?spreadsheet_id={spreadsheet_id}&worksheet_names={worksheet_slug}&external_use_s3={store_in_s3}", headers=authorized_headers)
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
                if cache_timeout != 0:
                    data["cache_timeout"] = data["customized"] + timedelta(seconds=int(cache_timeout))
                else:
                    data["cache_timeout"] = 0
                output = json.dumps(data, default=str)
                
            if "customized" not in result_json or store_in_s3 == "true":
                overwrite_url = current_app.config["OVERWRITE_API_URL"]
                params = {
                    "spreadsheet_id": spreadsheet_id,
                    "worksheet_names": worksheet_names,
                    "output": output,
                    "cache_timeout": cache_timeout,
                    "bypass_cache": "true",
                    "external_use_s3": store_in_s3
                }

                headers = {'Content-Type': 'application/json'}
                if authorized_headers:
                    headers = headers | authorized_headers
                result = requests.post(overwrite_url, data=json.dumps(params), headers=headers)
                result_json = result.json()
                if result_json is not None:
                    output = json.dumps(result_json, default=str)

    else:
        output = {} # something for empty data
    return output
