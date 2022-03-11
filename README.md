# MinnPost Who's Running 2022

Tracking Minnesota candidates for the 2022 election

## Google Sheets to JSON API setup

For both local and remote environments, you'll need to have access to an instance of the [Google Sheets to JSON API](https://github.com/MinnPost/google-sheet-to-json-api) that itself has access to the Google Sheet(s) that you want to process. If you don't already have access to a working instance of that API, set it up and ensure it's working first.

### Credentials

To access the Google Sheets to JSON API you'll need to have two configuration values in your `.env` or in your Heroku settings.

- `AUTHORIZE_API_URL = "http://0.0.0.0:5000/authorize/"` (wherever the API is running, it uses an `authorize` endpoint)
- `API_KEY = ""` (a valid API key that is accepted by the installation of the API that you're accessing)

### Configuration

Use the following additional fields in your `.env` or in your Heroku settings.

- `PARSER_API_URL = "http://0.0.0.0:5000/parser/"` (wherever the API is running, it uses a `parser` endpoint)
- `OVERWRITE_API_URL = "http://0.0.0.0:5000/parser/custom-overwrite/"` (wherever the API is running, it uses a `parser/custom-overwrite` endpoint)
- `SPREADSHEET_ID = "your google sheet ID"`
- `WORKSHEET_NAMES = '["Sheet1", "Sheet2"]'` (if you want to use multiple worksheets, or only one sheet that is not the first worksheet, separate the names of the sheets with commas and surround each one with quotes. If you leave it blank, the API will use the first worksheet in the spreadsheet.)
- `API_CACHE_TIMEOUT = "500"` (this value is how many seconds the customized cache should last. `0` means it won't expire.)
- `STORE_IN_S3` (provide a "true" or "false" value to set whether the API should send the JSON to S3. If you leave this blank, it will follow the API's settings.)

## Application setup

### Local setup and development

1. Install `git`
1. Get the code: `git clone https://github.com/MinnPost/minnpost-whos-running-2022.git`
1. Change the directory: `cd minnpost-whos-running-2022`
1. Create a `.env` file based on the repository's `.env-example` file in the root of your project.
1. Run `pipenv install`.
1. Run `pipenv shell`
1. Run `flask run --host=0.0.0.0`. This creates a basic endpoint server at http://0.0.0.0:5000.

### Production setup and deployment

#### Code, Libraries and prerequisites

This application can be run locally, but it can also be deployed to Heroku. If you are creating a new Heroku application, clone this repository with `git clone https://github.com/MinnPost/minnpost-whos-running-2022.git` and follow [Heroku's instructions](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote) to create a Heroku remote.

## Application usage

Currently, this application has one endpoint:

- `/candidate-tracker/` is a cached version of the JSON data, parsed from the Google Sheet and other settings specified in the configuration.
