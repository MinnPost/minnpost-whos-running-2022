# MinnPost Who's Running 2022

Tracking Minnesota candidates for the 2022 election

## Google Sheets API setup

For both local and remote environments, you'll need to have access to an instance of the [Google Sheets to JSON API](https://github.com/MinnPost/google-sheet-to-json-api) that itself has access to the Google Sheet(s) that you want to process. Follow all of the steps in that repository to make sure this is working first.

### Configuration

Use the following fields in your `.env` or in your Heroku settings.

- `PARSER_API_URL = "http://0.0.0.0:5000/parser/"` (wherever the API is running, it uses a `parser` endpoint)
- `OVERWRITE_API_URL = "http://0.0.0.0:5000/parser/custom-overwrite/"`  (wherever the API is running, it uses a `parser/custom-overwrite` endpoint)
- `SPREADSHEET_ID = "your google sheet ID"`
- `WORKSHEET_NAMES = '["Sheet1", "Sheet2"]'` (separate the names of the sheets with commas and surround each one with quotes)
- `API_CACHE_TIMEOUT = "500"` (this value is how many seconds the customized cache should last. `0` means it won't expire.)

## Amazon S3 setup

To push JSON data from this application to Amazon AWS, we use the `boto3` library.

### Configuration

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Fill in these values from the Amazon account.

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

This application should be deployed to Heroku. If you are creating a new Heroku application, clone this repository with `git clone https://github.com/MinnPost/minnpost-whos-running-2022.git` and follow [Heroku's instructions](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote) to create a Heroku remote.


## Application usage

Currently, this application has two endpoints:

- `/candidate-tracker/` is a cached version of the JSON data, parsed from the Google Sheet.
- `/candidate-tracker/push-s3` pushes the current JSON data, parsed from the Google Sheet, to Amazon S3.
