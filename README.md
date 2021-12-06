# MinnPost Who's Running 2022

Tracking Minnesota candidates for the 2022 election

## Google Sheets setup

For both local and remote environments, you'll need to make sure the application has access to the Google Sheets data. In version 4 of the Sheets API, this happens through Service Accounts.

### Creating a new authentication

If you are authenticating with the Sheets API for the first time, you'll need to create a new Google Cloud project. Start by following [this guide from Google](https://developers.google.com/workspace/guides/create-project). When you've finished Google's steps, you should have a new project.

Our specific Google Sheets integration uses the [Sheetfu library](https://github.com/socialpoint-labs/sheetfu), which has [an authentication guide](https://github.com/socialpoint-labs/sheetfu/blob/master/documentation/authentication.rst) to finish this process. The screenshots are not necessarily up to date with the names Google uses for things.

Between these resources, you should follow these steps to create and access the authentication credentials:

1. Create a new Google Cloud Platform project.
1. Enable the Sheets and Drive APIs in the APIs & Services section of the Google Cloud Platform settings.
1. Create a Service Account in the IAM & Admin section of the Google Cloud Platform settings.
1. Download the new JSON-formatted key for that Service Account. Only use this key for one environment.

This new Service account will have an automatically-created email address. For this application, that email address must have at least Viewer-level access on any Google Sheets that it needs to access. It's best to give it that level of access on the folder level.

If this user is new or it is being given new access, it can take a few minutes for the changes to propogate.

### Accessing an existing authentication

If the Service Account user already exists in the Google Cloud Platform, you can access it at https://console.cloud.google.com/home/dashboard?project=[application-name]. In MinnPost's case, this URL is [https://console.cloud.google.com/home/dashboard?project=minnpost-mn-election-results](https://console.cloud.google.com/home/dashboard?project=minnpost-mn-election-results).

If it hasn't been, you'll need your Google account added. An Administrator can do that at the correct dashboard URL by clicking "Add People to this Project."

Follow these steps to access the authentication credentials:

1. Once you have access to the project's dashboard, click "Go to project settings" in the Project info box.
1. Click Service Accounts in the IAM & Admin section of the Google Cloud Platform settings.
1. If there is more than one service account, find the correct one.
1. Click the Actions menu for that account and choose the Manage keys option.
1. Click Add Key, choose Create new key, and choose JSON as the Key type. Click the Create button and download the key for that Service Account. Only use this key for one environment.

## Local setup and development

1. Install `git`
1. Get the code: `git clone https://github.com/MinnPost/minnpost-whos-running-2022.git`
1. Change the directory: `cd minnpost-whos-running-2022`
1. Create a `.env` file based on the repository's `.env-example` file in the root of your project.
1. Run `pipenv install`.
1. Run `pipenv shell`
1. Run `flask run --host=0.0.0.0`. This creates a basic endpoint server at http://0.0.0.0:5000.

### Local authentication for Google Sheets

Enter the configuration values from the JSON key downloaded above into the `.env` file's values for these fields:

- `SHEETFU_CONFIG_TYPE`
- `SHEETFU_CONFIG_PROJECT_ID`
- `SHEETFU_CONFIG_PRIVATE_KEY_ID`
- `SHEETFU_CONFIG_PRIVATE_KEY`
- `SHEETFU_CONFIG_CLIENT_EMAIL`
- `SHEETFU_CONFIG_CLIENT_ID`
- `SHEETFU_CONFIG_AUTH_URI`
- `SHEETFU_CONFIG_TOKEN_URI`
- `SHEETFU_CONFIG_AUTH_PROVIDER_URL`
- `SHEETFU_CONFIG_CLIENT_CERT_URL`

## Production setup and deployment

### Code, Libraries and prerequisites

This application should be deployed to Heroku. If you are creating a new Heroku application, clone this repository with `git clone https://github.com/MinnPost/minnpost-whos-running-2022.git` and follow [Heroku's instructions](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote) to create a Heroku remote.

### Production authentication for Google Sheets

In the project's Heroku settings, enter the configuration values from the production-only JSON key downloaded above into the values for these fields:

- `SHEETFU_CONFIG_TYPE`
- `SHEETFU_CONFIG_PROJECT_ID`
- `SHEETFU_CONFIG_PRIVATE_KEY_ID`
- `SHEETFU_CONFIG_PRIVATE_KEY`
- `SHEETFU_CONFIG_CLIENT_EMAIL`
- `SHEETFU_CONFIG_CLIENT_ID`
- `SHEETFU_CONFIG_AUTH_URI`
- `SHEETFU_CONFIG_TOKEN_URI`
- `SHEETFU_CONFIG_AUTH_PROVIDER_URL`
- `SHEETFU_CONFIG_CLIENT_CERT_URL`

Run the scraper commands from the section below by following [Heroku's instructions](https://devcenter.heroku.com/articles/getting-started-with-python#start-a-console) for running Python commands. Generally, run commands on Heroku by adding `heroku run ` before the rest of the command listed below.
