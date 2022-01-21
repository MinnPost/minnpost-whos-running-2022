import json
import datetime
from flask import current_app
from slugify import slugify
from src.extensions import cache

from sheetfu import SpreadsheetApp

@cache.memoize(300)
def parser():
    output = {}
    data = {}
    spreadsheet_id = current_app.config["SPREADSHEET_ID"]
    if spreadsheet_id is not None:
        races = read_spreadsheet(spreadsheet_id, "Races")
        candidates = read_spreadsheet(spreadsheet_id, "Candidates")

        if races is not None:
            data["races"] = []
            for race in races:
                # format the date
                if race["date-added"] != None:
                    race["date-added"] = convert_xls_datetime(race["date-added"])
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
                    candidate["race-key"] = race_key
                    # format the date fields
                    if candidate["date-added"] != None:
                        candidate["date-added"] = convert_xls_datetime(candidate["date-added"])
                    if candidate["date-dropped-out"] != None:
                        candidate["date-dropped-out"] = convert_xls_datetime(candidate["date-dropped-out"])
                    # format the boolean fields
                    candidate["incumbent"] = convert_xls_boolean(candidate["incumbent"])
                    candidate["endorsed"] = convert_xls_boolean(candidate["endorsed"])
                    candidate["dropped-out"] = convert_xls_boolean(candidate["dropped-out"])
                    # add to the returnable data
                    data["candidates"].append(candidate)

        output = json.dumps(data)
    else:
        output = {} # something for empty data
    return output


@cache.memoize(60)
def read_spreadsheet(spreadsheet_id, worksheet_name):
    """
    Connect to Google spreadsheet and return the data as a list of dicts with the header values as the keys.
    """
    # list that will be returned
    data = []
    try:
        # connect to and load the spreadsheet data
        client = SpreadsheetApp(from_env=True)
        spreadsheet = client.open_by_id(spreadsheet_id)
        sheet = spreadsheet.get_sheet_by_name(worksheet_name)
        data_range = sheet.get_data_range()
        rows = data_range.get_values()

        if rows is not None:
            
            # populate a list to parse
            csv_data = []
            for row in rows:
                csv_data.append(row)
            headings = []
            for cell in csv_data[0]:
                headings.append(cell)
            
            # parse each row in the list and set it up for returning
            for row in csv_data[1:]:
                this_row = {}
                for i in range(0, len(row)):
                    if row[i] == "":
                        row[i] = None
                    this_row[headings[i]] = row[i]
                data.append(this_row)

    except Exception as err:
        current_app.log.error('[%s] Unable to connect to spreadsheet source: %s. The error was %s' % ('spreadsheet', spreadsheet_id, err))
    return data


def convert_xls_datetime(xls_date):
    return (datetime.datetime(1899, 12, 30) + datetime.timedelta(days=xls_date)).isoformat()


def convert_xls_boolean(string):
    if string == None:
        value = False
    else:
        string = string.lower()
        if string == "yes" or string == "true":
            value = True
        elif string == "no" or string == "false":
            value = False
        else:
            value = bool(string)
    return value
