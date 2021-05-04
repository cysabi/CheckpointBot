# Checkpoint Bot
> The bot for [Checkpoint 1](https://discord.com/invite/ZybuvgP)

This is a bot to help with tournament and verification season management for [Checkpoint 1](https://discord.com/invite/ZybuvgP). It is partially derived from my rewrite of [Radia](https://github.com/IPLSplatoon/Radia), however, there are still many custom-built cogs.

### Running locally
#### Prerequisites
1. Make sure you have Docker installed.
1. A Google API project for the bot.

#### Google setup
1. Enable the following API
   - [Google Sheets API](https://console.developers.google.com/apis/api/sheets.googleapis.com)
   - [Google Drive API](https://console.developers.google.com/apis/api/drive.googleapis.com)
1. Go to the [API & Services](https://console.developers.google.com/apis/credentials) and navigate to `credentials` tab
1. Click on `+ create credentials` and create a new `Service Accounts` fill in the necessary field.
   - When you get to **Role** give it `editor`.
1. Download the `credentials` files and rename it `google.json`
1. Share the Google Sheet with the `client_email` from the json file.
1. Copy the gsheet key from the url at `https://docs.google.com/spreadsheets/d/`**`{key}`**`/edit`, you will use this in the `.env`

#### Bot Setup
1. Create a `.env` in the repository root:

   ```py
   TOKEN = discord.bot.token
   GSHEET = gsheet_key
   SENTRY = "System Environment"  # Optional
   DEBUG = 1  # Optional
   ```

   Please know that there are no `true` or `false` values in `.env` files. If you want to set a key to false, set it to `0`

1. Run `docker-compose up` in the repository root.

---

Contact me · [**@LeptoFlare**](https://github.com/LeptoFlare) · [lepto.tech](https://lepto.tech)

As always, distributed under the MIT license. See `LICENSE` for more information.

_[https://github.com/LeptoFlare/CheckpointBot](https://github.com/LeptoFlare/CheckpointBot)_
