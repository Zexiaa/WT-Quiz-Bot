import json
import random
import aiohttp
import os, io

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
    
    tank = getRandomTank()
    msg = ""

    async with aiohttp.ClientSession() as session:
        url = tank["Image"]

        async with session.get(url) as resp:
            img = await resp.read()
            f = io.BytesIO(img)

    msg = f"Name: {tank['Name']}\nCountry: {tank['Nation']}\n"
    msg += f"{tank['Type']}\n"
    msg += f"{tank['Rank']} BR: {tank['BR']}"

    await ctx.send(f"```{msg}```", file=discord.File(f, url.split("/")[-1]))


def getRandomTank():
    return list[random.randint(0, len(list))]
    
bot.run(token)