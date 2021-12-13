from flask import current_app
from src.extensions import cache

from sheetfu import SpreadsheetApp

@cache.memoize(300)
def read_spreadsheet(spreadsheet_id, worksheet_name):
    """
    Connect to Google spreadsheet and return the data as a list of dicts with the header values as the keys.
    """
    data = []
    try:
        client = SpreadsheetApp(from_env=True)
        spreadsheet = client.open_by_id(spreadsheet_id)
        sheet = spreadsheet.get_sheet_by_name(worksheet_name)
        data_range = sheet.get_data_range()
        rows = data_range.get_values()
        if rows is not None:
            csv_data = []
            for row in rows:
                csv_data.append(row)
            headings = []
            for cell in csv_data[0]:
                headings.append(cell)
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