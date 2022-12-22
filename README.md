# overcooked-wr-watcher

This bot is used to post changes in the leaderboard of Overcooked for a specific Team into a discord channel. The website that holds the record information is https://overcooked.greeny.dev

## Discord bot setup

Go to https://discord.com/developers/applications and create and Application. Also create a bot for this application, you will need the bots token for the `.conf` file. 

## Getting started 

Python 3.10 is required. Create a virtual environment:
```
python3.10 -m venv env
```
activate the env:
```
source env/bin/activate
```
install the requirements:
```
pip install -r requirements.txt
```

Copy the `ramsay.conf.template` to `ramsay.conf` and fill in the information. Start the bot:
```
python main.py
```

Invite your Application/Bot to any server you want.
