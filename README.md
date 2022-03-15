# MinnPost Who's Running 2022

Tracking Minnesota candidates for the 2022 election

## Google Sheets to JSON API setup

For both local and remote environments, you'll need to have access to an instance of the [Google Sheets to JSON API](https://github.com/MinnPost/google-sheet-to-json-api) that itself has access to the Google Sheet(s) that you want to process. If you don't already have access to a working instance of that API, set it up and ensure it's working first.

### Credentials

To access the Google Sheets to JSON API you'll need to have two configuration values in your `.env` or in your Heroku settings.

- `AUTHORIZE_API_URL = "http://0.0.0.0:5000/authorize/"` (wherever the API is running, it uses an `authorize` endpoint)
- `API_KEY = ""` (a valid API key that is accepted by the installation of the API that you're accessing)

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

This application can be run locally, but it can also be deployed to Heroku. If you are creating a new Heroku application, clone this repository with `git clone https://github.com/MinnPost/minnpost-whos-running-2022.git` and follow [Heroku's instructions](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote) to create a Heroku remote.

### Configuration

Use the following additional fields in your `.env` or in your Heroku settings.

- `PARSER_API_URL = "http://0.0.0.0:5000/parser/"` (wherever the API is running, it uses a `parser` endpoint)
- `OVERWRITE_API_URL = "http://0.0.0.0:5000/parser/custom-overwrite/"` (wherever the API is running, it uses a `parser/custom-overwrite` endpoint)
- `SPREADSHEET_ID = "your google sheet ID"`
- `WORKSHEET_NAMES = '["Sheet1", "Sheet2"]'` (if you want to use multiple worksheets, or only one sheet that is not the first worksheet, separate the names of the sheets with commas and surround each one with quotes. If you leave it blank, the API will use the first worksheet in the spreadsheet.)
- `API_CACHE_TIMEOUT = "500"` (this value is how many seconds the customized cache should last. `0` means it won't expire. This value is ignored if `STORE_IN_S3` is set to "true".)
- `STORE_IN_S3` (provide a "true" or "false" value to set whether the API should send the JSON to S3. If you leave this blank, it will follow the API's settings.)

## Application usage

Currently, this application has one endpoint:

- `/candidate-tracker/` returns the current data parsed from the Google spreadsheet based on the configuration options above as they define caching, S3 storage, etc.

### Data parameters

In addition to the configuration options defined for the application, you can use `bypass_cache` with a value of `true` or `false` on the URL to set whether the application should try to load data from the API's cache. If this value is `false`, the application might load an older version of the spreadsheet. If it's `true`, it will bypass any cached data and reload it from the spreadsheet. This is the default behavior *if* S3 storage is enabled.

#### Parameter examples

- `0.0.0.0/candidate-tracker/?bypass_cache=true` will *always* skip data that is cached by the API and load fresh data from the spreadsheet.
- `0.0.0.0/candidate-tracker/?bypass_cache=false` will *never* skip data that is cached by the API, but there may not be any. If there is none, it will load fresh data from the spreadsheet.
- `0.0.0.0/candidate-tracker/` will skip cached data from the API *if* S3 storage is enabled.
- `0.0.0.0/candidate-tracker/` will try to retrieve cached data from the API *if* S3 storage is *not* enabled.

## Data update example

The TL;DR for non-technical users is that they can go to `/candidate-tracker` to trigger an update of the stored data, as long as it is configured in the desired way.

### More detail

To use this application strictly to store data in S3 and update it manually by calling the `candidate-tracker` endpoint, run it like this:

1. Set the `STORE_IN_S3` config value to "true"
1. Load the `candidate-tracker` endpoint
1. If successful, the endpoint will return a success message and show the URL of the updated JSON in S3.
