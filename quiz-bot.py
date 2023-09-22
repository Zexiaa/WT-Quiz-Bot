import json
import random
import aiohttp
import os#, io

import discord
from discord.ext import commands

# Prepare bot
token = input("Discord token:")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Load wiki data
file_dir = os.path.join(os.path.dirname(__file__), "wikiscraper/tankList.json")
with open(file_dir, 'r', encoding='UTF-8') as f:
    list = json.load(f)

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name="random")
async def random_tank(ctx):
    
    await ctx.typing()

    tank = getRandomTank()
    msg = ""

    async with aiohttp.ClientSession() as session:
        url = tank["Image"]

    embed = discord.Embed(title="Random Tank!")
    embed.add_field(name=tank['Name'], 
                    value=f"{tank['Nation']}\n{tank['Rank']}")
    embed.add_field(name="Battle Rating",
                    value=tank['BR'])
    embed.add_field(name="Class",
                    value=tank['Type'])
    
    embed.set_image(url=url)

    await ctx.send(msg, embed=embed)


def getRandomTank():
    return list[random.randint(0, len(list))]
    
bot.run(token)