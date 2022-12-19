import asyncio
import urllib.request
import os
import configparser
import discord
from discord.ext import commands, tasks
from classes import Entry, Level, DataPoint

# read config and bot boilerplate
config = configparser.ConfigParser()
config.read('ramsay.conf')
bot_config = config['DISCORD BOT']
TEAM_NAME = bot_config['teamname']
CSV_DATA_URL = bot_config['dataurl']
BOT_Prefix=tuple(bot_config['prefix'].split(' '))
BOT_TOKEN = bot_config['token']
CHANNEL_ID = bot_config['channelid']

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=BOT_Prefix, intents=intents)
client.remove_command("help")

# bot events

@client.event
async def on_ready():
    watching = discord.Streaming(type=1, url="https://overcooked.greeny.dev",
                                 name=f"j.help") # this is the bots status
    await client.change_presence(status=discord.Status.online, activity=watching)
    print(f"connection established, logged in as: {client.user.name}")

@client.event
async def on_guild_join(guild):
    print(f"i was invited to and have joined {guild}!")

@tasks.loop(seconds=10.0)
async def send_message():
    print("sending message")

asyncio.run(send_message())
client.run(BOT_TOKEN)

# if __name__ == "__main__":
#     urllib.request.urlretrieve(CSV_DATA_URL, "data.csv")
#     """
#     Game,DLC,level,Player Count,Place,Player / Team,Score,Video URL
#     "Overcooked 2",Story,Tutorial,1,1,"bird man birdman",1616,https://youtu.be/IgjIvFxzbXQ
#     ...
#     """
#     current_dp = DataPoint("data.csv", TEAM_NAME)

#     # create datapoint from old csv. if it does not exist, just report current status
#     if not os.path.exists("old_data.csv"):
#         print("did not find old_data.csv, just printing state of current data")
#         print(current_dp.get_report())
#     else:
#         old_dp = DataPoint("old_data.csv", TEAM_NAME)
#         out = old_dp.diff(current_dp)
#         if out:
#             print(out)

#     os.rename("data.csv", "old_data.csv")