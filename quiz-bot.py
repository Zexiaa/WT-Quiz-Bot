import json
import random
import aiohttp
import os
import asyncio
from threading import Timer

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

@bot.command(name="testscore")
async def test_score(ctx):
    await ctx.send("[TEST] Start sending messages")

    replies = []
    while True:
        tasks = [
            asyncio.create_task(bot.wait_for(
                'message',
                timeout=10.0
            ))
        ]

        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        finished: asyncio.Task = list(done)[0]

        for task in pending:
            try:
                task.cancel()
            except asyncio.CancelledError:
                pass

        try:
            result = finished.result()
        except asyncio.TimeoutError:
            return await ctx.send("Timeout!")
        
        msg: discord.Message = result
        replies.append(msg)
        break
            
    embed = discord.Embed(title="TEST")
    
    for reply in replies:
        embed.add_field(name=reply.author.name,
                        value=reply.content,
            inline=False)

    await ctx.send(embed=embed)

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
    
    try:
        guess = await bot.wait_for('message', timeout=10.0)

        if guess.content in tank['Name']:
            embed = discord.Embed(title="Guess that Tank!",
                          description="Score + 1")
            embed.add_field(name=tank['Name'], 
                        value=f"{tank['Nation']}\n{tank['Rank']}")
            embed.add_field(name="Battle Rating",
                            value=tank['BR'])
            embed.add_field(name="Class",
                            value=tank['Type'])
            return await ctx.send(embed=embed)
        else:
            return await ctx.send(embed=wrong_answer(tank))

    except asyncio.TimeoutError:
        return await ctx.send(embed=wrong_answer(tank))
    

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