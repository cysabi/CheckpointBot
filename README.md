# Checkpoint Bot
> The bot for [Checkpoint 1](https://discord.com/invite/ZybuvgP)

This is a bot to help with tournament and verification season management for [Checkpoint 1](https://discord.com/invite/ZybuvgP). It is partially derived from my rewrite of [Radia](https://github.com/IPLSplatoon/Radia), however, there are still many custom-built cogs.

## Usage
This is for staff members, for non-staff members, type `!help`.

### Season cog
Players are verified based on their ranks, and will recieve a rank role. Seasons are used to avoid outdated ranks, at the start of each new season, all of the rank roles are replaced.

Additionally, a Verified role is used to handle channel permissions and channel access. This role is not replaced each season. However, it may be pruned every couple of seasons.

Here is how the verification process works.
1. A user makes a role request in the respective channel, showing proof of their rank and asking for the correct role.
2. A Barista verifies the user and gives them the `Verified` role and their respective rank role.

The `!season` command group is used to manage season rank roles.

- `!season` List the season roles. The command will also tell you the **index of each tournament**, this is important.
  - Alternatively, as an alias, you can use `!season roles` for the same result.
- `!season delete` Removes the old season roles.
  - If you are afraid it will delete the wrong roles, you can double-check what roles it will be deleting by doing `!season` or `!season list`.
- `!season new <name> [delete=False]` Creates new season roles, you are required to specify the name of the season.
  - `<name>`: Any name works, but if you specify a literal season (such as 'winter'), it will automatically convert it into an emoji.
  - `[delete=False]`: Additionally, you can specify to automatically call delete old season roles before creating new roles (`!season new spring true`).
- `!season prune` Removes the Verified role from anyone without a season rank role.
  - This is helpful every couple of seasons when you want to remove the verified role from those who have neglected to request a role for a while.

### Tourney cog
- `!whatis` is used to quickly look up glossary terms, such as "swiss" and "glossary" (yes, the glossary includes a glossary). Requires the `google.json` file (see [Google Setup](#google-setup)).
- `!rules` is used to send sections of the checkpoint tournament rules for easy reference. Requires the `google.json` file (see [Google Setup](#google-setup)).

These commands are used like `!whatis battlefy`, if you omit the argument, the bot will automatically list all the possible options.

### Final words
Thanks for reading, I hope this documentation section was helpful to you. If you have any questions, feel free to ask me [@LeptoFlare](https://github.com/LeptoFlare).

## Contributing
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
