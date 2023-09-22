import json
import random
import aiohttp
import os
import asyncio
import time

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
                    value=f"{tank['Nation']}\n{tank['Rank']}", inline=False)
    embed.add_field(name="Battle Rating",
                    value=tank['BR'])
    embed.add_field(name="Class",
                    value=tank['Type'])
    
    embed.set_image(url=url)

    await ctx.send(msg, embed=embed)

@bot.command(name="guess")
async def guess_tank(ctx):

    await ctx.typing()

    tank = getRandomTank()

    async with aiohttp.ClientSession() as session:
        url = tank["Image"]

    embed = discord.Embed(title="Guess that Tank!")
    embed.set_image(url=url)

    await ctx.send(embed=embed)
    
    print("Starting quiz!")

    timer = 10
    guessers = ""
    while timer > 0:
        try:
            guess = await bot.wait_for('message', timeout=1.0)

            if guess.content in tank['Name']:
                guessers += guess.author.name + "\n"

        except asyncio.TimeoutError:
            pass

        time.sleep(1)
        timer -= 1

    if (guessers == ""):
        print("Incorrect or no guesses")
        return await ctx.send(embed=wrong_answer(tank))
    
    print("Correct guesses for " + tank['Name'])

    embed = discord.Embed(title="Guess that Tank!")
    embed.add_field(name=tank['Name'], 
                value=f"{tank['Nation']}\n{tank['Rank']}", inline=False)
    embed.add_field(name="Battle Rating",
                    value=tank['BR'])
    embed.add_field(name="Class",
                    value=tank['Type'])
        
    embed.add_field(name="Correct guesses",
                    value=guessers,
                    inline=False)
        
    await ctx.send(embed=embed)


def wrong_answer(tank):
    embed = discord.Embed(title="Guess that Tank!",
                            description="Time's up!")
    embed.add_field(name=tank['Name'], 
                value=f"{tank['Nation']}\n{tank['Rank']}", inline=False)
    embed.add_field(name="Battle Rating",
                    value=tank['BR'])
    embed.add_field(name="Class",
                    value=tank['Type'])
    
    return embed

def getRandomTank():
    return list[random.randint(0, len(list))]
    
bot.run(token)