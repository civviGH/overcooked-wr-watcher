import urllib.request
import os
import configparser
import discord
from discord.ext import tasks
from classes import DataPoint

# read config and bot boilerplate
config = configparser.ConfigParser()
config.read('ramsay.conf')
bot_config = config['DISCORD BOT']

TEAM_NAME = bot_config['teamname']
CSV_DATA_URL = bot_config['dataurl']
BOT_PREFIX=tuple(bot_config['prefix'].split(' '))
BOT_TOKEN = bot_config['token']
CHANNEL_ID = int(bot_config['channelid'])

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(command_prefix=BOT_PREFIX, intents=intents)

@client.event
async def on_ready():
    watching = discord.Streaming(type=1, url="https://overcooked.greeny.dev",
                                 name=f"twitch.tv/ueberkochen") # this is the bots status
    await client.change_presence(status=discord.Status.online, activity=watching)
    print(f"connection established, logged in as: {client.user.name}")
    report_loop.start()

@client.event
async def on_guild_join(guild):
    print(f"i was invited to and have joined {guild}!")

@tasks.loop(seconds=3600) # the dava.csv is updated once every hour on the wr site
async def report_loop():
    channel = client.get_channel(CHANNEL_ID)

    urllib.request.urlretrieve(CSV_DATA_URL, "data.csv")
    current_dp = DataPoint("data.csv", TEAM_NAME)
    # create datapoint from old csv. if it does not exist, just report current status
    if not os.path.exists("old_data.csv"):
        out = current_dp.get_report()
        if out:
            for l in out:
                await channel.send(l)
    else:
        old_dp = DataPoint("old_data.csv", TEAM_NAME)
        out = old_dp.diff(current_dp)
        if out:
            for l in out:
                await channel.send(l)
    os.rename("data.csv", "old_data.csv")

client.run(BOT_TOKEN)