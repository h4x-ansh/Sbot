# SBot

SBot is a Discord server utility bot made in Python.

It is mainly used for moderation and server management.

## What this bot can do

- Basic moderation commands like warn, kick, ban, purge, and slowmode
- Invite tracking and invite leaderboards
- AFK system
- Message leaderboards
- Ticket panel commands
- Temporary voice channel handling
- Reminder command to DM a user
- Basic info commands like avatar, banner, server info, and user info

## Files

- `bot.py` = main bot code
- `main.py` = small launcher for the bot
- `requirements.txt` = Python packages needed
- `.env` = your local bot token file
- `data/` = saved bot data

## How to run

1. Install Python.
2. Install the packages:

```powershell
py -m pip install -r requirements.txt
```

3. Create a `.env` file in the project folder.
4. Put your bot token inside it like this:

```env
DISCORD_TOKEN=your_token_here
```

5. Start the bot:

```powershell
py main.py
```

If `py` does not work on your PC, use your Python path or virtual environment instead.

## Notes

- Do not upload your real `.env` file to GitHub
- The bot stores some data locally inside the `data` folder
- Some old commands may still exist in the code, but the main use is server utility and moderation
